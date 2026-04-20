# LBSNAA Phase 5 Comic Book — Step-by-Step Workflow Guide

## What You're Building

A personalised 10-panel comic book for each group of 6 IAS officer trainees at LBSNAA, Mussoorie. Each comic includes a cover page, cast page, 10 illustrated panels with speech bubbles, and a closing dedication page. Final output is a print-ready PDF.

---

## Prerequisites

Before you start, make sure you have:

- [ ] Python installed on your computer
- [ ] An Anthropic API key (for Claude API calls)
- [ ] An active Midjourney subscription (web UI at midjourney.com)
- [ ] An Imgur account (free, for hosting photos permanently)
- [ ] Passport-style photos for all 6 participants in the group
- [ ] Names, home states, quirks, and gender for all 6 participants
- [ ] Consent from participants to use their photos in a comic memento

---

## Phase 0: Prepare Photos (Do This Once)

### Why Imgur?

Midjourney needs permanent image URLs to reference faces. Discord CDN links expire in ~24 hours and will cause Midjourney to generate random faces instead.

### Steps

1. Go to **imgur.com** and sign in (or create a free account)
2. Click **New Post** → upload all 6 passport photos for the group
3. After upload, right-click each image → **Copy image address**
4. Save all 6 URLs in a text file. They should look like:
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
cd C:\Users\nictuArvind\Downloads\comic_2
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

1. **API Key** — Paste your Anthropic API key at the top

2. **Group Name** — Enter a fun group name (e.g., "The Cool Squad")

3. **Story Template** — Choose one of 4 options:
   | Template | Best For |
   |----------|----------|
   | The Last Night Before Posting | Classic, works for any group |
   | The Great Case Study That Came Alive | Groups known for academics |
   | The Mess Menu Mystery | Groups with foodie members |
   | Ten Years Later: Reunion at Char Dukan | Groups that are very close-knit |

   **Tip:** Use a different template for each of the 4 groups so the comics feel unique.

4. **Characters** — For each of the 6 officers, fill in:
   - **Full Name** (required — all 6 must be filled)
   - **Gender** (Male / Female)
   - **Home State** (select from dropdown)
   - **One Quirk / Fun Fact** (e.g., "always quotes Nehru", "never without chai")

5. Click **Generate Comic Script**

### Review the script

Read through all 10 panels carefully. Check for:
- [ ] All 6 names appear and are spelled correctly
- [ ] Correct he/she pronouns used
- [ ] Each officer gets a dream/future moment
- [ ] Humour is warm and safe (no caste/religion/politics/body jokes)
- [ ] Panel 10 is emotional and includes everyone
- [ ] Dialogues are short enough to fit in speech bubbles

### Save the script

- Click **{ } COPY JSON** — copies raw JSON to clipboard (needed for Tool 2 and Tool 3)
- Click **DOWNLOAD JSON** — saves a .json file to your computer as backup
- Optionally click **PRINT / PDF** to save a readable version

---

## Phase 3: Generate Midjourney Prompts (Tool 2)

### Open Tool 2

Go to: **http://localhost:8765/midjourney_prompt_generator.html**

### Fill in the form

1. **API Key** — Paste your Anthropic API key

2. **Character Visual Descriptions** — For each of the 6 characters:
   - **Name** (pre-filled if you've used this before)
   - **Gender** (Male / Female)
   - **Skin Tone** (select closest match)
   - **Visual Description** (optional but helpful — e.g., "short black hair, round glasses, slim build")
   - **Signature Clothing** (optional — e.g., "always wears a blue kurta")
   - **Passport Photo URL** — Paste the Imgur URL from Phase 0

3. **Midjourney Character Sheet URLs** (Section 1b) — Leave empty for now. You'll fill this after Phase 4.

4. **Art Style** — "Warm Hand-Painted Animation" is selected by default. Keep it unless you prefer another style.

5. **Paste Comic Script JSON** — Paste the JSON you copied from Tool 1

6. Click **Generate Midjourney Prompts**

### What you get

Three tabs appear:
- **Individual Panels** — 10 prompts, one per comic panel
- **Bulk Copy** — All prompts in one block
- **Character Sheets** — 6 character reference prompts

---

## Phase 4: Run Character Sheets in Midjourney (Do This First!)

Character sheets establish what each person looks like. Without this step, faces will be inconsistent across panels.

### Steps

1. Go to **midjourney.com** → click **Create**

2. For each of the 6 Character Sheet prompts:
   a. Go back to Tool 2 → **Character Sheets** tab
   b. Click **COPY** on the first character
   c. Go to Midjourney → paste in the prompt box → press **Enter**
   d. Wait for 4 image variations to generate
   e. Click the one that looks most like the real person
   f. Click **Upscale** (U1, U2, U3, or U4)
   g. Once upscaled, right-click the image → **Copy image address** (save this URL)
   h. Repeat for all 6 characters

3. Go back to Tool 2 → **Section 1b (Midjourney Character Sheet URLs)**
   - Paste each character's upscaled Midjourney URL into their field

4. Click **Generate Midjourney Prompts** again
   - This time, all 10 panel prompts will include `--sref` with your character URLs for style consistency

### Quality check

- [ ] Each character sheet looks recognisably like the real person
- [ ] Gender is correct
- [ ] No unwanted text/words in the generated images
- [ ] Art style is consistent across all 6 sheets

**If a face doesn't match:** Re-run the same prompt. Midjourney is random — the next batch may be better. If it keeps failing, check that the Imgur URL loads correctly.

---

## Phase 5: Run Panel Prompts in Midjourney

### Steps

1. Go to Tool 2 → **Individual Panels** tab

2. For each of the 10 panels:
   a. Click **COPY** on Panel 1
   b. Go to Midjourney → paste → Enter
   c. Wait for 4 variations
   d. Pick the best one → **Upscale**
   e. **Download** the upscaled image to your computer
   f. Repeat for all 10 panels

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
- [ ] Final panel (10) includes all 6 characters together

**If style drifts:** Copy the URL of your best-looking panel and add `--sref [that URL]` to the end of the next prompt before running it.

---

## Phase 6: Build the Comic Book (Tool 3)

### Open Tool 3

Go to: **http://localhost:8765/comic_compositorv2.html**

Note: `http://localhost:8765/comic_compositor.html` is kept as a backward-compatible redirect to v2.

### Fill in the form

1. **Paste Comic Script JSON** — Same JSON from Tool 1. This provides all the dialogue and captions for speech bubbles.

2. **Character Photos (for cover page)** — Click each circle and upload the passport photo for that character. These appear on the cover page.

3. **Upload 10 Panel Images** — Click each slot and upload the corresponding Midjourney panel image. **Order matters** — Panel 1 first, Panel 10 last.

4. Click **BUILD COMIC PREVIEW**

### What you see

The comic preview shows:
- **Cover page** — Title, group name, tagline, 6 character portraits
- **Cast page** — Character names, states, roles with photos
- **5 content pages** — 2 panels per page, with speech bubbles and captions overlaid
- **Closing page** — Dedication text with disclaimer

### Position the speech bubbles

Speech bubbles are **draggable**. Click and drag each bubble to position it where it looks best on the panel. Tips:
- Place bubbles near the character who is speaking
- Don't cover faces
- Keep reading order left-to-right, top-to-bottom
- Caption boxes (yellow) work well at the bottom
- Dream thought bubbles (purple dashed) should be near the dreaming character

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

## Repeating for Groups 2, 3, and 4

Once Group 1's PDF is final and you're happy with it:

1. **Freeze your settings** — don't change art style, panel layout, or font between groups
2. Go back to Tool 1 → enter the next group's details
3. **Choose a different story template** for variety:
   - Group 1: The Last Night Before Posting
   - Group 2: The Great Case Study That Came Alive
   - Group 3: The Mess Menu Mystery
   - Group 4: Ten Years Later: Reunion at Char Dukan
4. Follow Phases 2–7 again for each group
5. **Clear browser data** after all 4 groups are done (use the CLEAR ALL SAVED DATA button in Tool 2)

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Page shows old version after code changes | Hard refresh: Ctrl+Shift+R, or add ?v=2 to URL |
| "Cannot access panelMap" error | Fixed in latest version. Hard refresh. |
| Midjourney generates random faces | Photo URLs have expired. Re-upload to Imgur and use new URLs. |
| Wrong gender in images | Check Gender dropdown in Tool 2 character cards |
| Text/letters appear in MJ images | The --no parameter should prevent this. If it still happens, re-run the prompt. |
| Speech bubbles don't appear in compositor | Make sure you pasted the JSON (not plain text) from Tool 1 |
| PDF looks wrong | Set print margins to None and enable "Background graphics" |
| Browser lost all my inputs | Tool 2 uses localStorage. If you cleared cache, re-enter data. |
| API error from Claude | Check your API key is valid and has credits |

---

## File Reference

| File | Purpose | URL |
|------|---------|-----|
| `server.py` | Local server (run first) | Terminal: `python server.py` |
| `lbsnaa_comic_generator.html` | Tool 1: Script generator | http://localhost:8765 |
| `midjourney_prompt_generator.html` | Tool 2: MJ prompt generator | http://localhost:8765/midjourney_prompt_generator.html |
| `comic_compositorv2.html` | Tool 3: Layout + PDF | http://localhost:8765/comic_compositorv2.html |

---

## Cost Estimate

| Step | Cost | Notes |
|------|------|-------|
| Script generation (Tool 1) | ~$0.04 per group | Claude Sonnet API |
| Prompt generation (Tool 2) | ~$0.04 per group | Claude Sonnet API |
| Character sheets (Midjourney) | ~6 generations per group | Uses MJ subscription |
| Panel images (Midjourney) | ~10 generations per group | Uses MJ subscription |
| **Total per group** | **~$0.08 API + ~16 MJ generations** | |
| **Total for all 4 groups** | **~$0.32 API + ~64 MJ generations** | |

---

## Privacy Reminders

- Only use participant photos with their knowledge/consent
- Use Imgur "hidden" uploads (not public gallery)
- Clear browser localStorage after final PDFs are generated
- Do not share Imgur URLs publicly
- The closing page includes a disclaimer: "A personalised fictional comic memento created for internal batch memory purposes."

---

*Created: April 2026 | LBSNAA Phase 5 Comic Book Project*
