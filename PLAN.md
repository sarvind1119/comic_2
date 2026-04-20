# Hybrid Scene Automation (OpenAI Primary, Midjourney Fallback)

## Summary
Add a new **Automation** workflow inside Tool 2 that auto-generates panel scenes via OpenAI API, preserves character consistency with locked references + vision checks, and routes failed panels to Midjourney fallback. Keep existing manual flow intact. Final outputs remain `panel_01.png ... panel_10.png` for Tool 3.

## Implementation Changes
1. Extend Tool 2 with a fourth tab: `Automation`.
2. Add an internal job runner in Tool 2 that consumes existing script/prompt data and executes panel jobs with statuses: `queued`, `generating`, `review`, `approved`, `fallback_mj`, `failed`.
3. Build a `character_lock` object from Tool 2 character inputs plus reference URLs (passport + sheet URLs) and inject it into every generation request.
4. Generate up to **3 candidates per panel** (OpenAI primary), score each with automated consistency checks, and send top candidate to human review.
5. Require explicit human approval per panel before marking final and exporting to compositor-ready output.
6. Run panels in **sequential order with small overlap** (window size 2) to maintain continuity while improving throughput.
7. If all 3 candidates fail quality threshold, mark panel `fallback_mj` and export a Midjourney-ready fallback packet for that panel.
8. Add OpenAI proxy routes in `server.py` for:
   - image generation requests,
   - vision consistency scoring requests,
   while keeping Anthropic routes unchanged.
9. Add a deterministic export bundle from Tool 2:
   - approved panel files with strict filenames,
   - `scene_jobs.json`,
   - `character_lock.json`,
   - `fallback_mj.json` (only failed panels).
10. Preserve current manual tabs (`Individual`, `Bulk`, `Character Sheets`, `Scene Packet`) without behavior regressions.

## Public Interfaces / Contracts
1. `character_lock.json` (new):
   - `group`, `title`, `style_profile`,
   - `characters[]` with immutable traits, photo refs, sheet refs.
2. `scene_jobs.json` (new):
   - one record per panel with `panel_number`, `prompt`, `candidates[]`, `scores`, `status`, `approved_asset`.
3. `fallback_mj.json` (new):
   - only panels with status `fallback_mj`,
   - includes final MJ prompt text and required character refs.
4. Scoring contract (new internal API result):
   - `consistency_score`, `style_score`, `text_artifact_flag`, `character_presence`, `pass/fail`.
5. Existing script JSON contract remains unchanged (`title`, `group`, `characters[6]`, `panels[10]`, `panel.number`, `dialogues[]`, optional `caption`, optional `dreamOf`).

## Test Plan
1. Happy path: 10 panels generated, reviewed, approved, exported as `panel_01.png ... panel_10.png`, then loaded in Tool 3 with no renaming.
2. Consistency path: intentionally perturb one character descriptor and verify vision score drops and panel is not auto-surfaced as pass.
3. Retry path: verify max 3 candidates per panel; fourth attempt is never triggered.
4. Fallback path: force scoring failure and verify panel is routed to `fallback_mj.json` with correct refs/prompts.
5. Review gate path: unapproved panels cannot be exported as final outputs.
6. Resume path: refresh Tool 2 and confirm job state can be reloaded from `scene_jobs.json`.
7. Backward compatibility: existing manual Tool 2 flow still works exactly as before.

## Assumptions and Defaults
1. OpenAI image generation is primary engine; Midjourney remains manual fallback only.
2. Default model tier is **Balanced quality**; optional per-panel high-quality rerun can be added later.
3. Quality gate uses prompt locks + automated vision checks + mandatory human approval.
4. No Midjourney browser RPA in v1.
5. Automation is implemented inside Tool 2 (not a new page), and server remains local single-user.
