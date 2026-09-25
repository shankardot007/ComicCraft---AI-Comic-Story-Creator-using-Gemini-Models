# ComicCraft Demo Video Script
# Phase 8 — Project Demonstration
# What to SAY + What to SHOW. Use this as your teleprompter.

---

## TIP: How to structure the video
- Record screen (VS Code) + your mic. Use OBS Studio or Win + G (Xbox Game Bar).
- Total target: 4–6 minutes.
- Pause between sections. If you mess up, just say "cut" and rerecord that part.
- Keep the app already running in the background so panels generate fast.

---

## SECTION 1 — INTRODUCTION (0:00 – 0:30)
**SHOW:** VS Code open on the project root (ComicCraft folder in Explorer sidebar).

**SAY:**
"Hi everyone. This is my project, ComicCraft AI — an AI Comic Story Creator built using Google Gemini models.

ComicCraft is a web application that turns a simple text prompt into a complete comic book — the story outline, the narration, character dialogue, and even the panel illustrations — and then exports everything as a downloadable PDF.

In this demo, I'll walk you through the code I built in VS Code, then show the app working end to end."

---

## SECTION 2 — PROBLEM & SOLUTION (0:30 – 1:00)
**SHOW:** `README.md` (or the `1_Brainstorming_and_Ideation` folder) in the editor.

**SAY:**
"The problem this project solves is simple: creating a comic normally requires drawing skills, storyboarding experience, and a lot of time. Most people have story ideas but can't turn them into comics.

ComicCraft solves this by using Generative AI — specifically Google's Gemini models — to automatically handle the outline, the writing, and the artwork. All the user does is type a story idea."

**SHOW:** Expand folder `1_Brainstorming_and_Ideation` → `2_Requirement_Analysis` → `3_Project_Design` etc. in the Explorer to show the phased structure.

**SAY:**
"The project is organized in eight phases — from brainstorming and requirement analysis, to design, planning, development, testing, documentation, and finally this demonstration."

---

## SECTION 3 — CODE WALKTHROUGH: BACKEND (1:00 – 3:00)

### 3a. requirements.txt
**SHOW:** Open `requirements.txt`.

**SAY:**
"The core stack is Python with FastAPI for the backend, Google's genai library for Gemini, FPDF2 for the PDF export, and Pillow for image handling."

### 3b. app/config.py
**SHOW:** Open `app/config.py`.

**SAY:**
"Configuration is loaded from a `.env` file using python-dotenv. The Google API key is required; the Hugging Face key is optional. The Gemini model names are all configurable — Flash for the outline, Pro for the story, and an image model for the illustrations."

### 3c. app/schemas.py
**SHOW:** Open `app/schemas.py`.

**SAY:**
"Here are the Pydantic schemas. `StoryRequest` takes the idea, characters, setting, tone, art style, and panel count — validated from 3 to 10 panels. The `Comic` model holds the title, logline, and a list of panels, with narration and dialogue."

### 3d. app/routes/api.py
**SHOW:** Open `app/routes/api.py`.

**SAY:**
"The API layer has four endpoints: a health check, story generation, image generation, and the PDF export. Let me quickly show the most important one — the story generation endpoint — which calls the story engine and returns the full comic."

### 3e. app/services/story_engine.py
**SHOW:** Open `app/services/story_engine.py`.

**SAY:**
"This is the heart of the project. It works in two steps: first, Gemini Flash builds a structured panel-by-panel outline. Then Gemini Pro expands it into full narration, dialogue, and an image prompt for every panel. If Pro hits a quota limit, the code automatically falls back to Flash — which keeps the free-tier project working."

### 3f. app/services/image_engine.py
**SHOW:** Open `app/services/image_engine.py`.

**SAY:**
"The image engine has a fallback chain: if a Hugging Face key is set, it uses Stable Diffusion. Otherwise it uses Gemini's image model — and if that fails, it drops in a placeholder, so the comic and PDF always export successfully."

### 3g. app/services/pdf_engine.py
**SHOW:** Open `app/services/pdf_engine.py`.

**SAY:**
"Finally, the PDF engine uses FPDF2 to lay out the title, logline, all the panels, images, narration, and dialogue into a downloadable comic PDF."

---

## SECTION 4 — FRONTEND (3:00 – 3:30)
**SHOW:** `templates/index.html` and `static/js/app.js` briefly.

**SAY:**
"The frontend is a single-page interface built with HTML, CSS, and vanilla JavaScript using Jinja2. The form collects the story idea plus optional characters, tone, art style, and panel count. The JavaScript calls the API, streams each panel in with a progress bar, renders the comic grid, and triggers the PDF download."

---

## SECTION 5 — LIVE DEMO (3:30 – 5:00)
**SHOW:** Switch to the browser at http://127.0.0.1:8000 (app already running).
**TIP:** Keep VS Code and the app visible — run `uvicorn app.main:app --reload` in the VS Code terminal, then show the browser.

**SAY:**
"Now let's see it actually working. I'll run the server from the VS Code terminal with `uvicorn app.main:app --reload`."

**SHOW:** Enter a story idea, e.g.:
"A shy robot discovers it can grow flowers and must save its dying city before the annual Bloom Festival."
- Add a character (optional), pick tone "Wholesome", art style "Manga", panels = 6.

**SAY:**
"I'll enter a story idea, click Generate Comic, and you can see the progress bar as the outline is built, the story is written, and each panel gets illustrated."

**SHOW:** Wait for panels to render, scroll the comic preview, point out title, logline, narration, dialogue.

**SAY:**
"Here is the finished comic — the title, the logline, and all six panels with narration, dialogue, and illustrations, all generated by AI."

**SHOW:** Click "⬇ Download PDF" and open the downloaded file.

**SAY:**
"And one click exports the whole comic as a PDF, ready to print or share."

---

## SECTION 6 — TESTING (5:00 – 5:20)
**SHOW:** `6_Project_Testing` folder or briefly mention.

**SAY:**
"The project was tested end to end — health endpoint, story generation, the image fallback chain, PDF export, and input validation all passed, using FastAPI's test client. `6_Project_Testing` has the full test-case table."

---

## SECTION 7 — CONCLUSION (5:20 – 5:45)
**SHOW:** Back to the project root or the comic preview.

**SAY:**
"To summarize: ComicCraft combines Gemini Flash and Gemini Pro for storytelling and AI image generation for the artwork, all inside a FastAPI web app, with a one-click PDF export.

It demonstrates how AI can make creative work accessible to everyone — even if you can't draw. Thank you for watching!"

---

## AFTER RECORDING
1. Render/export the video (MP4).
2. Upload to Google Drive (share link set to "Anyone with the link can view") or YouTube (Unlisted).
3. Paste the link into `8_Project_Demonstration\DEMO_LINK.txt`.