# LBSNAA Phase 5 Comic Book — Step-by-Step Workflow Guide

## What You're Building

A personalised comic book for each group of IAS officer trainees at LBSNAA, Mussoorie. Each comic includes a cover page, cast page, illustrated panels with speech bubbles, and a closing dedication page. Final output is a print-ready PDF.

Panel count auto-scales: **character count + 4 panels** (e.g. 6 characters → 10 panels, 10 characters → 14 panels).

---

## Prerequisites

Before you start, make sure you have:

- [ ] Python installed on your computer
- [ ] An Anthropic API key (for Claude — script generation and MJ prompt generation)
- [ ] An OpenAI API key (optional — for Automation/Hybrid Mode image generation in Tool 2)
- [ ] An active Midjourney subscription (web UI at midjourney.com) — needed unless using Automation Mode
- [ ] An Imgur account (free, for hosting photos permanently)
- [ ] Passport-style photos for all participants in the group
- [ ] Names, home states, allotment years, quirks, and gender for all participants
- [ ] Consent from participants to use their photos in a comic memento

---

## Phase 0: Prepare Photos (Do This Once)

### Why Imgur?

Midjourney needs permanent image URLs to reference faces. Discord CDN links expire in ~24 hours and will cause Midjourney to generate random faces instead.

### Steps

1. Go to **imgur.com** and sign in (or create a free account)
2. Click **New Post** → upload all passport photos for the group
3. After upload, right-click each image → **Copy image address**
4. Save all URLs in a text file. They should look like:
   ```
   https://i.imgur.com/abc123.jpg
   https://i.imgur.com/def456.jpg
   ...
   ```
5. Test each URL by pasting it in a new browser tab — the photo should load instantly

**Keep these URLs safe. You'll use them in Tool 2.**

---

## Phase 1: Start the Server

Open a terminal/command prompt in the project folder and run:

```
cd C:\Users\HP\Documents\2026\comic_2
python server.py
```

You should see:
```
LBSNAA Comic Generator — Local Server
Open in browser: http://localhost:8765
```

**Keep this terminal open for the entire session.**

---

## Phase 2: Generate the Comic Script (Tool 1)

### Open Tool 1

Go to: **http://localhost:8765**

### Fill in the form

1. **Step 0 — API Key** — Paste your Anthropic API key at the top

2. **Step 1 — Group Name** — Enter a fun group name (e.g., "The Cool Squad")

3. **Step 1b — Story Mode** — Choose one of two modes:
   | Mode | When to use |
   |------|-------------|
   | Curated Template (Recommended) | Use one of 8 pre-built story arcs |
   | Custom Idea (Guided + Free Text) | Describe your own story premise |

4. **Step 1c — Story Template** (Curated Mode only) — Choose one of 8 templates:
   | Template | Best For |
   |----------|----------|
   | The Last Night Before Posting | Classic, works for any group |
   | The Great Case Study That Came Alive | Groups known for academics |
   | The Mess Menu Mystery | Groups with foodie members |
   | Ten Years Later: Reunion at Char Dukan | Groups that are very close-knit |
   | The Night of the Disaster Drill | High-energy, teamwork-focused groups |
   | One Day, Six Districts | Groups dispersing to diverse states |
   | The Farewell Treasure Hunt | Groups who love academy nostalgia |
   | The Ethics Desk at Midnight | Thoughtful, values-driven groups |

   **Tip:** Use a different template for each group so the comics feel unique.

5. **Custom Idea** (Custom Mode only — Steps 1d & 1e) — Fill in:
   - **Premise** — The core story setup (e.g., "Final-night mock crisis turns into a life lesson")
   - **Conflict** — The challenge they face
   - **Mood** — e.g., "warm, witty, respectful, hopeful"
   - **Key Location** — e.g., "Char Dukan + Academy war room + misty Mussoorie roads"
   - **Ending Note** — How the story resolves emotionally
   - **Optional Free Text** — Write a raw story seed in plain language; the tool will refine it

6. **Step 2 — Cast Size + Panel Count** — Set the character count (6–26). Panel count updates automatically: **panels = characters + 4**.

7. **Step 2b — Enter Characters** — For each officer, fill in:
   - **Full Name** (required — all slots must be filled)
   - **Gender** (Male / Female — controls he/she pronouns in the script)
   - **Allotment Year** (required — controls seniority; lower year = more senior; junior uses "sir"/"ma'am" with senior)
   - **Home State** (select from dropdown)
   - **One Quirk / Fun Fact** (e.g., "always quotes Nehru", "never without chai")

8. Click **Generate Comic Script**

### Review the script

Read through all panels carefully. Check for:
- [ ] All names appear and are spelled correctly
- [ ] Correct he/she pronouns used
- [ ] Correct seniority honorifics (sir/ma'am between juniors and seniors)
- [ ] Each officer gets a dream/future moment
- [ ] Humour is warm and safe (no caste/religion/politics/body jokes)
- [ ] Final panel is emotional and includes everyone
- [ ] Dialogues are short enough to fit in speech bubbles

### Save the script

- Click **{ } COPY JSON** — copies raw JSON to clipboard (needed for Tool 2 and Tool 3)
- Click **⬇ DOWNLOAD JSON** — saves a .json file to your computer as backup
- Optionally click **⎙ PRINT / PDF** to save a readable version

---

## Phase 3: Generate Midjourney Prompts (Tool 2)

### Open Tool 2

Go to: **http://localhost:8765/midjourney_prompt_generator.html**

### Fill in the form

1. **API Key** — Paste your Anthropic API key

2. **Character Visual Descriptions** — For each character:
   - **Name** (pre-filled if you've used this before)
   - **Gender** (Male / Female)
   - **Skin Tone** (select closest match)
   - **Visual Description** (optional but helpful — e.g., "short black hair, round glasses, slim build")
   - **Signature Clothing** (optional — e.g., "always wears a blue kurta")
   - **Passport Photo URL** — Paste the Imgur URL from Phase 0

3. **Midjourney Character Sheet URLs** (Section 1b) — Leave empty for now. You'll fill this after Phase 4.

4. **Art Style** — Choose from 6 styles. "Warm Hand-Painted Animation" is the default.
   | Style | Description |
   |-------|-------------|
   | Warm Hand-Painted Animation | Soft watercolour, Ghibli-esque, warm lighting (default) |
   | Amul Poster / Amar Chitra Katha | Bold outlines, flat vibrant colours, classic Indian comic |
   | Warm Manga | Expressive, bold linework, screentone shading |
   | Webtoon | Clean digital linework, soft cel shading |
   | Watercolour Graphic Novel | Loose expressive lines, translucent washes |
   | Retro Indian Graphic Novel | Bold poster colours, vintage 1970s aesthetic |

5. **Paste Comic Script JSON** — Paste the JSON you copied from Tool 1

6. Click **Generate Midjourney Prompts**

### Output tabs

Five tabs appear after generation:
- **Individual Panels** — One prompt per comic panel (for manual Midjourney use)
- **Bulk Copy** — All prompts in one block
- **Character Sheets** — Character reference prompts
- **Scene Packet** — Full continuity packet for ChatGPT / manual workflows
- **Automation** — OpenAI Hybrid Mode (see Phase 5B)

---

## Phase 4: Run Character Sheets in Midjourney (Do This First!)

Character sheets establish what each person looks like. Without this step, faces will be inconsistent across panels.

### Steps

1. Go to **midjourney.com** → click **Create**

2. For each Character Sheet prompt:
   a. Go to Tool 2 → **Character Sheets** tab
   b. Click **COPY** on the character
   c. Go to Midjourney → paste in the prompt box → press **Enter**
   d. Wait for 4 image variations to generate
   e. Click the one that looks most like the real person
   f. Click **Upscale** (U1, U2, U3, or U4)
   g. Once upscaled, right-click the image → **Copy image address** (save this URL)
   h. Repeat for all characters

3. Go back to Tool 2 → **Section 1b (Midjourney Character Sheet URLs)**
   - Paste each character's upscaled Midjourney URL into their field

4. Click **Generate Midjourney Prompts** again
   - All panel prompts will now include `--sref` with your character URLs for style consistency

### Quality check

- [ ] Each character sheet looks recognisably like the real person
- [ ] Gender is correct
- [ ] No unwanted text/words in the generated images
- [ ] Art style is consistent across all sheets

**If a face doesn't match:** Re-run the same prompt. Midjourney is random — the next batch may be better. If it keeps failing, check that the Imgur URL loads correctly.

---

## Phase 5A: Run Panel Prompts in Midjourney (Manual Route)

### Steps

1. Go to Tool 2 → **Individual Panels** tab

2. For each panel:
   a. Click **COPY** on the panel
   b. Go to Midjourney → paste → Enter
   c. Wait for 4 variations
   d. Pick the best one → **Upscale**
   e. **Download** the upscaled image to your computer
   f. Repeat for all panels

### File naming

Save images with clear names:
```
panel_01_the_escape.png
panel_02_chai_stall.png
panel_03_dream_indra.png
...
panel_10_finale.png
```

### Quality check for each panel

- [ ] Correct number of characters visible
- [ ] No unwanted text, letters, or garbled words
- [ ] Art style matches the character sheets
- [ ] Dream panels look visually distinct (softer, dreamier)
- [ ] Final panel includes all characters together

**If style drifts:** Copy the URL of your best-looking panel and add `--sref [that URL]` to the end of the next prompt before running it.

---

## Phase 5B: OpenAI Hybrid Mode (Automated Route — Optional)

Tool 2 includes an **Automation tab** that uses OpenAI to generate panel images automatically, score them for quality, and present passing images for your approval. This skips manual Midjourney pasting.

**Requirements:** OpenAI API key with access to `gpt-image-1` (image generation) and `gpt-4.1-mini` (quality scoring).

### How it works

1. Go to Tool 2 → **Automation** tab
2. Enter your **OpenAI API Key**
3. Select **Model Tier** (Balanced / Highest Quality / Cost-saving)
4. Select **Scoring Model** (gpt-4.1-mini or gpt-4.1)
5. Click **Prepare Jobs** — creates one job per panel
6. Click **Run Automation** — for each panel, it:
   - Generates up to 3 candidate images using `gpt-image-1`
   - Scores each image for consistency, style, and text artifacts
   - Marks the best passing image as approved
7. **Human Approval Queue** — review generated images and approve or flag for Midjourney fallback
8. Click **Export Bundle** to download all approved images

### Scoring criteria (auto-pass threshold)

| Metric | Threshold |
|--------|-----------|
| Consistency score | ≥ 0.72 |
| Style score | ≥ 0.70 |
| Text artifacts | None |
| Character presence | Required characters visible |

If a panel fails all 3 attempts, it falls back to **Midjourney** (manual).

---

## Phase 6: Build the Comic Book (Tool 3)

### Open Tool 3

Go to: **http://localhost:8765/comic_compositorv2.html**

Note: `http://localhost:8765/comic_compositor.html` is kept as a backward-compatible redirect to v2.

### Fill in the form

1. **Paste Comic Script JSON** — Same JSON from Tool 1. This provides all the dialogue and captions for speech bubbles.

2. **Character Photos (for cover page)** — Click each circle and upload the passport photo for that character. These appear on the cover page.

3. **Upload Panel Images** — Click each slot and upload the corresponding panel image. **Order matters** — Panel 1 first, last panel last.

4. Click **BUILD COMIC PREVIEW**

### What you see

The comic preview shows:
- **Cover page** — Title, group name, tagline, character portraits
- **Cast page** — Character names, states, roles with photos
- **Content pages** — 2 panels per page, with speech bubbles and captions overlaid
- **Closing page** — Dedication text with disclaimer

### Position the speech bubbles

Speech bubbles are **draggable**. Click and drag each bubble to position it where it looks best on the panel. Tips:
- Place bubbles near the character who is speaking
- Don't cover faces
- Keep reading order left-to-right, top-to-bottom
- Caption boxes (yellow) work well at the bottom
- Dream thought bubbles (purple dashed) should be near the dreaming character

### Pan and zoom panel images

Panel images support **drag-to-pan** — click and drag inside a panel to reposition the image within its frame. This lets you crop/frame the illustration without editing the image.

### Export as PDF

1. Click **PRINT / SAVE PDF**
2. In the print dialog:
   - Set **Destination** to "Save as PDF"
   - Set **Paper size** to A4
   - Set **Margins** to None
   - Check "Background graphics" is enabled
3. Click **Save**

The PDF is your final comic book, ready for printing.

---

## Phase 7: Print and Gift

- Print the PDF on good quality paper (glossy recommended)
- Use a local print shop for booklet binding if desired
- Alternatively, share the PDF via WhatsApp/email

---

## Repeating for Multiple Groups

Once Group 1's PDF is final and you're happy with it:

1. **Freeze your settings** — don't change art style, panel layout, or font between groups
2. Go back to Tool 1 → enter the next group's details
3. **Choose a different story template** for variety — 8 templates available, use a fresh one per group
4. Follow Phases 2–7 again for each group
5. **Clear browser data** after all groups are done (use the CLEAR ALL SAVED DATA button in Tool 2)

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Page shows old version after code changes | Hard refresh: Ctrl+Shift+R, or add ?v=2 to URL |
| Midjourney generates random faces | Photo URLs have expired. Re-upload to Imgur and use new URLs. |
| Wrong gender in images | Check Gender dropdown in Tool 2 character cards |
| Text/letters appear in MJ images | The --no parameter should prevent this. If it still happens, re-run the prompt. |
| Speech bubbles don't appear in compositor | Make sure you pasted the JSON (not plain text) from Tool 1 |
| PDF looks wrong | Set print margins to None and enable "Background graphics" |
| Browser lost all my inputs | Tool 2 uses localStorage. If you cleared cache, re-enter data. |
| API error from Claude | Check your Anthropic API key is valid and has credits |
| OpenAI automation fails | Check OpenAI API key has access to gpt-image-1; verify billing is active |
| Allotment year validation error | All character allotment years are required — fill in the year field for every character |

---

## File Reference

| File | Purpose | URL |
|------|---------|-----|
| `server.py` | Local server (run first) | Terminal: `python server.py` |
| `lbsnaa_comic_generator.html` | Tool 1: Script generator | http://localhost:8765 |
| `midjourney_prompt_generator.html` | Tool 2: MJ prompt generator + Automation | http://localhost:8765/midjourney_prompt_generator.html |
| `comic_compositorv2.html` | Tool 3: Layout + PDF | http://localhost:8765/comic_compositorv2.html |

---

## Cost Estimate

| Step | Cost | Notes |
|------|------|-------|
| Script generation (Tool 1) | ~$0.04 per group | Claude Sonnet API |
| Prompt generation (Tool 2) | ~$0.04 per group | Claude Sonnet API |
| Character sheets (Midjourney) | ~N generations per group | N = character count; uses MJ subscription |
| Panel images (Midjourney, manual) | ~(N+4) generations per group | N = character count |
| **OpenAI Automation (optional)** | ~$0.05–0.30 per panel | gpt-image-1 + gpt-4.1-mini scoring; up to 3 candidates per panel |

---

## Privacy Reminders

- Only use participant photos with their knowledge/consent
- Use Imgur "hidden" uploads (not public gallery)
- Clear browser localStorage after final PDFs are generated
- Do not share Imgur URLs publicly
- The closing page includes a disclaimer: "A personalised fictional comic memento created for internal batch memory purposes."

---

*Updated: April 2026 | LBSNAA Phase 5 Comic Book Project*
