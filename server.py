#!/usr/bin/env python3
"""
Simple proxy server for LBSNAA Comic Generator
Run: python server.py
Then open: http://localhost:8765
"""

import http.server
import json
import urllib.request
import urllib.error
import os
import sys

PORT = 8765
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

class ProxyHandler(http.server.SimpleHTTPRequestHandler):

    def log_message(self, format, *args):
        print(f"  {args[0]} {args[1]}")

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_POST(self):
        if self.path == "/api/generate":
            self.handle_generate()
        elif self.path == "/api/openai/generate-image":
            self.handle_openai_generate_image()
        elif self.path == "/api/openai/score-image":
            self.handle_openai_score_image()
        else:
            self.send_error(404)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        super().end_headers()

    def do_GET(self):
        request_path = self.path.split("?", 1)[0]
        # Default entrypoint
        if request_path == "/" or request_path == "/index.html":
            self.path = "/lbsnaa_comic_generator.html"
        # Backward-compatible alias: old compositor path -> v2
        elif request_path == "/comic_compositor.html":
            query = ""
            if "?" in self.path:
                query = "?" + self.path.split("?", 1)[1]
            self.path = "/comic_compositorv2.html" + query
        super().do_GET()

    def handle_generate(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            payload = json.loads(body)

            api_key = payload.pop("api_key", "") or API_KEY
            if not api_key:
                self.respond(400, {"error": "No API key provided. Add it in the page or set ANTHROPIC_API_KEY env variable."})
                return

            req = urllib.request.Request(
                "https://api.anthropic.com/v1/messages",
                data=json.dumps(payload).encode(),
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01"
                },
                method="POST"
            )

            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read())
            self.respond(200, result)

        except urllib.error.HTTPError as e:
            err = json.loads(e.read())
            self.respond(e.code, err)
        except Exception as e:
            self.respond(500, {"error": str(e)})

    def _read_json_payload(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        return json.loads(body)

    def _openai_post(self, endpoint, payload, api_key, timeout=180):
        req = urllib.request.Request(
            endpoint,
            data=json.dumps(payload).encode(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())

    def handle_openai_generate_image(self):
        try:
            payload = self._read_json_payload()
            api_key = payload.pop("api_key", "") or OPENAI_API_KEY
            if not api_key:
                self.respond(400, {"error": "No OpenAI API key provided. Add it in UI or set OPENAI_API_KEY env variable."})
                return

            prompt = payload.get("prompt", "")
            if not prompt:
                self.respond(400, {"error": "Missing required field: prompt"})
                return

            req_payload = {
                "model": payload.get("model", "gpt-image-1"),
                "prompt": prompt,
                "size": payload.get("size", "1024x1536"),
                "response_format": "b64_json"
            }
            if payload.get("quality"):
                req_payload["quality"] = payload.get("quality")

            result = self._openai_post("https://api.openai.com/v1/images/generations", req_payload, api_key, timeout=240)
            self.respond(200, result)

        except urllib.error.HTTPError as e:
            raw = e.read().decode(errors="ignore")
            try:
                err = json.loads(raw)
            except Exception:
                err = {"error": raw or f"HTTP {e.code}"}
            self.respond(e.code, err)
        except Exception as e:
            self.respond(500, {"error": str(e)})

    def handle_openai_score_image(self):
        try:
            payload = self._read_json_payload()
            api_key = payload.pop("api_key", "") or OPENAI_API_KEY
            if not api_key:
                self.respond(400, {"error": "No OpenAI API key provided. Add it in UI or set OPENAI_API_KEY env variable."})
                return

            image_b64 = payload.get("image_b64", "")
            panel_prompt = payload.get("panel_prompt", "")
            character_lock = payload.get("character_lock", {})
            required_characters = payload.get("required_characters", [])
            if not image_b64:
                self.respond(400, {"error": "Missing required field: image_b64"})
                return

            schema = {
                "type": "object",
                "properties": {
                    "consistency_score": {"type": "number"},
                    "style_score": {"type": "number"},
                    "text_artifact_flag": {"type": "boolean"},
                    "character_presence": {"type": "boolean"},
                    "pass": {"type": "boolean"},
                    "notes": {"type": "string"}
                },
                "required": ["consistency_score", "style_score", "text_artifact_flag", "character_presence", "pass"],
                "additionalProperties": False
            }

            judge_prompt = (
                "Score this comic panel candidate for character consistency and style continuity.\n\n"
                f"Panel prompt:\n{panel_prompt}\n\n"
                f"Required characters:\n{json.dumps(required_characters, ensure_ascii=False)}\n\n"
                f"Character lock:\n{json.dumps(character_lock, ensure_ascii=False)}\n\n"
                "Scoring guidance:\n"
                "- consistency_score: 0 to 1\n"
                "- style_score: 0 to 1\n"
                "- text_artifact_flag: true if any visible text/letters/captions are present\n"
                "- character_presence: true only if required characters appear sufficiently\n"
                "- pass: true only if consistency_score>=0.72 and style_score>=0.70 and text_artifact_flag=false and character_presence=true\n"
                "Return JSON only."
            )

            req_payload = {
                "model": payload.get("model", "gpt-4.1-mini"),
                "input": [{
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": judge_prompt},
                        {"type": "input_image", "image_url": f"data:image/png;base64,{image_b64}"}
                    ]
                }],
                "text": {
                    "format": {
                        "type": "json_schema",
                        "name": "panel_consistency_score",
                        "schema": schema,
                        "strict": True
                    }
                }
            }

            result = self._openai_post("https://api.openai.com/v1/responses", req_payload, api_key, timeout=180)

            text_out = ""
            for item in result.get("output", []):
                for chunk in item.get("content", []):
                    if chunk.get("type") in ("output_text", "text"):
                        text_out += chunk.get("text", "")
            if not text_out:
                # fallback if API shape differs
                text_out = result.get("output_text", "")

            score = json.loads(text_out) if text_out else {
                "consistency_score": 0.0,
                "style_score": 0.0,
                "text_artifact_flag": True,
                "character_presence": False,
                "pass": False,
                "notes": "Empty scoring response"
            }
            self.respond(200, {"score": score, "raw": result})

        except urllib.error.HTTPError as e:
            raw = e.read().decode(errors="ignore")
            try:
                err = json.loads(raw)
            except Exception:
                err = {"error": raw or f"HTTP {e.code}"}
            self.respond(e.code, err)
        except Exception as e:
            self.respond(500, {"error": str(e)})

    def respond(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self._cors()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f"\n{'='*50}")
    print(f"  LBSNAA Comic Generator — Local Server")
    print(f"{'='*50}")
    if not API_KEY:
        print(f"  ⚠  No ANTHROPIC_API_KEY env variable found.")
        print(f"     You can paste your key directly in the browser page.")
    else:
        print(f"  ✓  API key loaded from environment.")
    print(f"\n  Open in browser:  http://localhost:{PORT}")
    print(f"  Press Ctrl+C to stop.\n")
    server = http.server.HTTPServer(("localhost", PORT), ProxyHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")
