# ComicCraft - AI Comic Story Creator using Gemini Models

## Overview

ComicCraft is a web-based application that uses AI to generate personalized comic book stories and illustrations based on user-provided prompts. Built with FastAPI and integrated with Google's Gemini AI models (along with optional Stable Diffusion), ComicCraft automates the creative process of generating storylines, dialogues, and vivid comic-style imagery.

Users provide a story prompt, main character, setting, tone, and art style. The system generates a panel-by-panel storyline with corresponding illustrations, lets users preview the comic on a web interface, and export the full comic as a downloadable PDF (using FPDF).

- **Backend:** Python, FastAPI, Uvicorn
- **AI Core:** Google Gemini (Flash for outlines, Pro for narration/dialogue, image model for illustrations)
- **Image (optional):** Stable Diffusion via Hugging Face Inference API
- **Frontend:** HTML, CSS, JavaScript, Jinja2
- **PDF Export:** FPDF2
- **Config:** python-dotenv (.env)

> Only a Google Gemini API key is required. Hugging Face is optional; images fall back to Gemini's image model automatically.