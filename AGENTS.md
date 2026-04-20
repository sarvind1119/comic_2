# LBSNAA Phase 5 — Comic Book Project Handoff
> Resume this project in Codex. All context needed is below.

---

## 🎯 What This Project Is

We are creating **personalized comic books** as a batch memory gift for **24 Phase 5 IAS officer trainees** at LBSNAA, Mussoorie.

- 24 participants split into **4 groups of 6**
- Each group gets a **10-panel comic book** titled **"The Last Night Before Posting"**
- Story: The 6 officers sneak out on their last LBSNAA evening for chai & momos at Kulri Bazaar, Mussoorie. Each officer gets a dream-bubble panel imagining their future posting/home state.
- Final output: Illustrated comic panels generated via **Midjourney** using real passport photos of participants

---

## ✅ What Is Already Done

### Tool 1 — Comic Script Generator (`lbsnaa_comic_generator.html`)
- A local HTML tool that takes 6 participant names, home states, and quirks
- Calls **Anthropic Codex API** (via local Python proxy) to generate a full 10-panel comic script in JSON
- Output includes: cast intro, panel-by-panel scene descriptions, dialogues, dream bubbles, artist notes
- **STATUS: WORKING ✅** — First group ("The Cool Squad") script already generated successfully

### Tool 2 — Midjourney Prompt Generator (`midjourney_prompt_generator.html`)
- Takes the JSON script output + character visual descriptions + passport photo URLs
- Calls Codex API to generate polished Midjourney `/imagine` prompts for all 10 panels
- Each prompt auto-appends `--cref [photo_url] --cw 100` for face consistency
- Has 3 tabs: Individual Panels / Bulk Copy / Character Sheets
- **STATUS: BUILT ✅ — Ready to use, not yet tested end-to-end**

### Local Proxy Server (`server.py`)
- Simple HTTP server on `localhost:8765`
- Proxies Anthropic API calls from the HTML tools (bypasses CORS)
- Run with: `python server.py`
- **STATUS: WORKING ✅**

---

## 📁 Files in This Folder

```
📁 project folder/
   ├── AGENTS.md                          ← this file
   ├── server.py                          ← run this first always
   ├── lbsnaa_comic_generator.html        ← Tool 1: script generator (with gender field)
   ├── midjourney_prompt_generator.html   ← Tool 2: MJ prompt generator (Ghibli style, no-text prompts)
   └── comic_compositorv2.html           ← Tool 3: comic layout + speech bubbles + PDF export
```

---

## 🔑 Keys & Credentials Needed

- **Anthropic API Key**: User has one — entered manually in the browser UI (never hardcoded)
- **Midjourney**: User has active subscription, uses via midjourney.com web UI
- **Photo URLs**: User has permanent image URLs (Imgur or similar) for all 24 participants

---

## 👥 Group 1 — "The Cool Squad" (DONE ✅)

Script already generated. Characters:

| # | Name | State | Quirk/Role |
|---|------|-------|------------|
| 1 | Indra Mallo | Maharashtra | Surprising social butterfly leader |
| 2 | Nilkanth S. Avhad | Punjab | Infectious laughter, mood booster |
| 3 | Vatsala Vasudeva | Gujarat | Wise maternal figure, guide |
| 4 | Shyamal Misra | Haryana | Disciplined time keeper, organizer |
| 5 | Anandrao Patil | Tamil Nadu | Lovable rebellious class clown |
| 6 | Kaling Tayeng | Arunachal Pradesh | Gentle heart, group harmonizer |

**Next step for this group**: Open Midjourney Prompt Generator → fill character visuals + paste photo URLs → generate prompts → run in Midjourney.

---

## 📋 Groups 2, 3, 4 — NOT YET STARTED

User has participant details for all 24. Need to:
1. Open `lbsnaa_comic_generator.html` for each group
2. Enter 6 names + states + quirks
3. Generate script
4. Then generate Midjourney prompts

---

## 🔄 The Full Workflow (repeat for each group)

```
Step 1  → Upload 6 passport photos to Imgur → get permanent URLs
Step 2  → Run: python server.py
Step 3  → Open: http://localhost:8765 (Tool 1)
Step 4  → Enter 6 names + states + quirks + gender → Generate Script → Copy JSON
Step 5  → Open: http://localhost:8765/midjourney_prompt_generator.html (Tool 2)
Step 6  → Enter API key, character details (with gender), Imgur photo URLs
Step 7  → Paste MJ character sheet URLs in section 1b (if available)
Step 8  → Paste script JSON → Generate Prompts (Ghibli style, no text in images)
Step 9  → Character Sheets tab → run 6 prompts in Midjourney → save output URLs
Step 10 → Individual Panels tab → run 10 prompts in Midjourney → download images
Step 11 → Open: http://localhost:8765/comic_compositorv2.html (Tool 3)
Step 12 → Upload 10 images + 6 cover photos + paste script JSON
Step 13 → Drag speech bubbles to position → Print / Save PDF
```

---

## ⚠️ Known Issues & Notes

- **Photo URLs**: Must be permanent. **Use Imgur only** — Discord CDN URLs expire in ~24hrs and Midjourney will generate random faces.
- **CORS**: HTML tools CANNOT be opened directly as files. Must go through `server.py` at `localhost:8765`.
- **Midjourney has no API**: All image generation is manual — user pastes prompts into midjourney.com web UI.
- **Midjourney cannot generate text**: All prompts now explicitly exclude text/speech bubbles. Dialogues are added in Tool 3 (Comic Compositor).
- **Script JSON**: Use the "Copy JSON" button in Tool 1 to get raw JSON for Tool 2 and Tool 3.
- **localStorage**: Tool 2 saves all inputs to browser localStorage — data survives page refreshes.

---

## 🚀 What To Do Next (Priority Order)

### Immediate
1. **Start server**: `python server.py` in this folder
2. **Open Tool 2**: `http://localhost:8765/midjourney_prompt_generator.html`
3. **Complete Group 1 prompts**: Fill visuals + photo URLs for the 6 Cool Squad members → generate MJ prompts
4. **Test in Midjourney**: Run Character Sheets first, then all 10 panel prompts

### After Group 1 is illustrated
5. **Generate scripts for Groups 2, 3, 4** using Tool 1
6. **Generate MJ prompts** for each group using Tool 2
7. **Run all in Midjourney**

### After Midjourney images are ready
8. **Open Tool 3**: `http://localhost:8765/comic_compositorv2.html`
9. **Paste script JSON** + upload 10 panel images + 6 cover photos
10. **Drag speech bubbles** to position them on panels
11. **Print / Save PDF** — produces A4 comic book ready for gifting

### Optional Enhancements (if time permits)
- Add a **batch mode** to Tool 1 so all 4 group scripts can be generated in one session

---

## 🎨 Art Style Recommendation

**Studio Ghibli Style** (default) — cute, warm, dreamy:
- Soft watercolor tones
- Warm gentle lighting
- Expressive cute cartoon characters
- Dreamy atmospheric backgrounds

Midjourney settings: `--ar 3:4 --s 300 --v 6.1`

Alternative: **Amul Poster Style** also available in Tool 2 dropdown.

---

## 💬 Context on User

- Works at **LBSNAA** (Lal Bahadur Shastri National Academy of Administration), Mussoorie
- Builds data dashboards, Python scripts, and AI tools for IAS officer training
- Comfortable with Python and running local servers
- Has active Codex.ai and Midjourney subscriptions
- This comic project is a personal gift initiative for Phase 5 batch participants

---

*Last updated: April 2026 — Handoff from Codex.ai chat to Codex*
