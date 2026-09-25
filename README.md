<div align="center">

# 🎨 ComicCraft AI — AI Comic Story Creator using Gemini Models

**AI-Powered Comic Book Generator & Visual Storytelling Platform**

ComicCraft is a Generative AI-based comic creation application designed to help users turn a simple text idea into a complete comic book — structured outline, narration, character dialogue, and comic-style illustrations — all in an interactive web interface with one-click PDF export.

The project combines Artificial Intelligence, Generative Image Models, and a modern web application to make comic creation easy for everyone, even without any drawing or storyboarding skills.

</div>

---

## 🚀 Features

### 🤖 AI Comic Generator

Enter a simple story idea and get a complete multi-panel comic.
Receive AI-generated stories, narration, and dialogue in your chosen tone and art style.

### 📖 Story Engine

Gemini Flash builds a structured, panel-by-panel comic outline with a title and logline.
Gemini Pro (with automatic Flash fallback) expands it into narration, dialogues, and image prompts.

### 🎨 AI Illustration

Every panel is illustrated automatically from its image prompt.
Uses the Gemini image model by default, with optional Stable Diffusion (Hugging Face) when configured.

### 🧠 Generative AI

Uses Google Gemini LLMs to understand the story prompt.
Generates natural-language narration, character dialogue, and scene descriptions.
Provides context-aware, tone-aware assistance.

### 📄 PDF Export

Compile the full comic — title, logline, panels, and images — into a downloadable PDF.
Built with FPDF2 for easy saving, printing, and sharing.

### 🖼️ Interactive Comic Preview

Panel-by-panel preview grid with scene descriptions, narration, and dialogue bubbles.
Progress bar and live feedback while panels generate.

### 🧊 Smart Fallback System

Story engine falls back from Pro to Flash on quota blocks.
Image chain falls back: Stable Diffusion → Gemini image model → placeholder.
The comic and PDF always export, even on free-tier quota limits.

### 📱 Responsive Design

Designed to work on desktop, tablet, and mobile screens.

### ✅ Validated Inputs

Pydantic-validated request/response models on every API endpoint.

---

## 🎯 Project Objective

The main objective of ComicCraft is to make comic creation accessible to ordinary users.

Traditional comic book creation requires significant artistic skill, storyboarding experience, and time. Many people have great story ideas but lack the tools to turn them into a visual narrative quickly. ComicCraft uses Generative AI to handle the outline, script, and illustrations, so anyone can create comics from a simple text prompt.

> **Note:** ComicCraft is an educational and creative tool. AI-generated content may contain inaccuracies or imperfections and is intended for personal, educational, and demonstration purposes.

---

## 🏗️ System Architecture

```
              ┌──────────────────────┐
              │       User           │
              │  (story idea prompt) │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   Frontend / UI      │
              │  Web Application     │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   Backend API        │
              │  FastAPI + Uvicorn   │
              └──────────┬───────────┘
                         │
          ┌──────────────┴──────────────┐
          │                             │
          ▼                             ▼
 ┌─────────────────┐          ┌─────────────────┐
 │  Gemini Flash   │          │ Gemini Pro/Flash│
 │  Outline Engine │          │  Story Engine   │
 └────────┬────────┘          └────────┬────────┘
          │                            │
          └──────────────┬─────────────┘
                         ▼
              ┌──────────────────────┐
              │   Panel Image Engine │
              │ Gemini Image / SDXL  │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  Comic Preview Grid  │
              │  + PDF Export (FPDF) │
              └──────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │       User           │
              └──────────────────────┘
```

---

## 🛠️ Technologies Used

### Frontend

- HTML5
- CSS3
- JavaScript
- Jinja2 Templates
- Responsive Web Design

### Backend

- Python
- FastAPI
- Uvicorn

### Artificial Intelligence

- Google Gemini (LLM)
- Gemini Image Model (Illustrations)
- Stable Diffusion XL (optional, via Hugging Face Inference API)
- Large Language Model (LLM) — Gemini Flash & Pro
- Prompt Engineering
- Retry / Backoff error handling

### PDF & Document Processing

- FPDF2 (comic PDF export)
- Pillow (image handling)

### Development Tools

- Visual Studio Code
- Git
- GitHub
- Python Virtual Environment

---

## 📁 Project Structure

```
ComicCraft/
│
├── app/
│   ├── main.py                 # FastAPI app, Jinja2 templates, static mount
│   ├── config.py               # .env loading, model config, directories
│   ├── schemas.py              # Pydantic models (StoryRequest, Panel, Comic, ...)
│   ├── routes/
│   │   └── api.py              # /api/health, /generate-story, /generate-image, /export-pdf
│   └── services/
│       ├── ai.py               # Gemini client + JSON parsing + retry/backoff
│       ├── story_engine.py     # Outline -> narration/dialogue -> Comic
│       ├── image_engine.py     # Stable Diffusion -> Gemini image -> placeholder
│       └── pdf_engine.py       # FPDF comic export
│
├── templates/
│   └── index.html              # Web UI
│
├── static/
│   ├── css/style.css           # Styling
│   ├── js/app.js               # Fetch flow, panel rendering, download
│   ├── generated/              # Generated panel images
│   └── downloads/              # Exported PDFs
│
├── 1_Brainstorming_and_Ideation/
├── 2_Requirement_Analysis/
├── 3_Project_Design/
├── 4_Project_Planning/
├── 5_Project_Development/
├── 6_Project_Testing/
├── 7_Project_Documentation/
├── 8_Project_Demonstration/
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

> **Note:** The exact structure may vary depending on the implementation.

---

## ⚙️ Installation

### Clone the Repository

```
git clone https://github.com/shankardot007/comiccraft
```

Move into the project directory:

```
cd ComicCraft
```

### Create a Virtual Environment

Windows:

```
python -m venv .venv
```

Activate it:

```
.venv\Scripts\activate
```

For macOS/Linux:

```
python3 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

```
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root (use `.env.example` as a template).

Example:

```
GOOGLE_API_KEY=your_google_gemini_key
HF_API_KEY=
```

Optional model overrides (defaults shown):

```
GEMINI_FLASH_MODEL=gemini-3.6-flash
GEMINI_PRO_MODEL=gemini-3.6-flash
GEMINI_IMAGE_MODEL=gemini-2.5-flash-image
SD_MODEL=stabilityai/stable-diffusion-xl-base-1.0
```

### Important

- Only `GOOGLE_API_KEY` is required. `HF_API_KEY` is optional — when empty, the Gemini image model is used automatically.
- Never upload your API keys or `.env` file to GitHub.

`.env` is already added to `.gitignore`:

```
.env
.venv/
__pycache__/
*.pyc
static/generated/
static/downloads/
```

---

## ▶️ Running the Project

Activate the virtual environment first:

```
.venv\Scripts\activate
```

Then start the backend with Uvicorn:

```
uvicorn app.main:app --reload
```

The application will normally be available at:

```
http://127.0.0.1:8000
```

Open the address in your browser.

---

## 💬 How to Use

### Step 1 — Open ComicCraft

Launch the application in your browser.

### Step 2 — Enter Your Story Idea

Type a story idea in the "Story idea" field.

Example:

```
A shy robot discovers it can grow flowers and must save its dying city before the annual Bloom Festival.
```

### Step 3 — Add Optional Details

Add characters, choose a setting, pick a tone (e.g. Wholesome, Dark, Funny) and an art style (e.g. American Comic, Manga, Anime), and set the number of panels (3–10).

### Step 4 — Generate the Comic

Click **⚡ Generate Comic**. The system builds the outline, writes the story, and illustrates each panel — watch the progress bar update panel by panel.

### Step 5 — Review Your Comic

Browse the preview grid with your comic title, logline, narration, dialogue, and panel art.

### Step 6 — Download the PDF

Click **⬇ Download PDF** to save the full comic as a downloadable PDF.

---

## 🧠 AI Workflow

```
User Story Idea
      │
      ▼
Input Processing
      │
      ▼
Prompt Construction
      │
      ▼
Gemini Flash ──► Multi-Panel Comic Outline (JSON)
      │
      ▼
Gemini Pro / Flash ──► Full Story Script (narration + dialogue + image prompts)
      │
      ▼
Image Generation (loop per panel)
      │   Stable Diffusion → Gemini Image Model → Placeholder
      ▼
Comic Preview Grid
      │
      ▼
PDF Export (FPDF)
      │
      ▼
User
```

---

## 🔐 Security Considerations

The application follows basic security practices:

- Never expose API keys in frontend code.
- Store secrets in environment variables.
- `.env` is excluded from version control.
- Pydantic validation on all API inputs.
- Model names and keys are read from environment/config.
- Generated files are kept in ignored directories.
- Interactive API docs (`/docs`) can be disabled before production deployment.

---

## ⚠️ Disclaimer

ComicCraft provides general creative and educational assistance.

The stories and images generated by the AI may contain errors, omissions, or imperfections, and may not always match the user's intent. AI-generated content should not be treated as professional, editorial, or commercially guaranteed artwork.

ComicCraft is a demonstration of what AI-powered storytelling can do — enjoy it, remix it, and have fun creating.

---

## 🎓 Academic Project

- **Project Name:** ComicCraft AI — AI Comic Story Creator using Gemini Models
- **Project Type:** Generative AI Project
- **Domain:** Artificial Intelligence / Creative Technology
- **Primary Technologies:** Python, FastAPI, Google Gemini, Web Technologies
- **Development Environment:** Visual Studio Code

---

## 🌟 Future Enhancements

Possible future improvements include:

- 👤 User authentication
- 🗂️ Comic history and saved projects
- 🎙️ Voice-based story input
- 🌐 Multilingual comic generation
- 🔎 Advanced art-style and layout options
- 📑 Editable panels and re-generation per panel
- 🧑‍🎨 Character consistency across panels
- 🖼️ Image upscaling and inpainting
- ☁️ Cloud deployment
- 📱 Android application
- 💬 Speech-bubble text overlay (rendered into the image)
- 🔗 Collaborative comic creation

---

## 📸 Screenshots

Add project screenshots here:

```
screenshots/
├── home.png
├── generator.png
├── preview.png
└── pdf-export.png
```

Example:

```
![Home](screenshots/home.png)
```

---

## 🚀 Deployment

ComicCraft can be deployed using platforms such as:

- Render
- Railway
- Google Cloud Run
- Hugging Face Spaces
- Replit
- Vercel (frontend)
- AWS

> **Note:** The Gemini and Hugging Face API keys must be configured securely as environment variables on the deployment platform. Never commit them.

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a new branch.

```
git checkout -b feature/new-feature
```

3. Make your changes.
4. Commit your changes.

```
git add .
git commit -m "Add new feature"
```

5. Push the branch.

```
git push origin feature/new-feature
```

6. Create a Pull Request.

---

## 📜 License

This project is intended primarily for educational and demonstration purposes.

A suitable open-source license can be added depending on the project's distribution requirements.