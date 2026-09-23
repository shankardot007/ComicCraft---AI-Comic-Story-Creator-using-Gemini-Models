<div align="center">

# ComicCraft — AI Comic Story Creator using Gemini Models

**AI-powered web application that turns a simple text prompt into a complete comic book
— outline, story, dialogue, and illustrations — exportable as a PDF.**

Built with **FastAPI** · **Google Gemini** · **FPDF** · optional **Stable Diffusion (Hugging Face)**.

</div>

## What it does

1. You enter a story idea (plus optional characters, setting, tone, art style, panel count).
2. **Gemini Flash** builds a structured multi-panel comic outline.
3. **Gemini Pro** (auto-falls back to Flash on quota blocks) expands it into narration, dialogue, and image prompts.
4. Each panel is illustrated by the **Gemini image model** (or Stable Diffusion when `HF_API_KEY` is set).
5. Preview everything on the web page and **download the full comic as a PDF**.

> Only a **Google Gemini API key** is required — no Hugging Face key needed.

## Repository Structure (Phase-wise)

| Phase | Folder | Contents |
| :--- | :--- | :--- |
| 1 | [`1_Brainstorming_and_Ideation`](1_Brainstorming_and_Ideation) | Problem statement, solution, core features |
| 2 | [`2_Requirement_Analysis`](2_Requirement_Analysis) | Functional & non-functional requirements, tech stack |
| 3 | [`3_Project_Design`](3_Project_Design) | Architecture flow, backend structure, schema |
| 4 | [`4_Project_Planning`](4_Project_Planning) | WBS, responsibilities, risks |
| 5 | [`5_Project_Development`](5_Project_Development) | **Working source code** — FastAPI app, services, UI |
| 6 | [`6_Project_Testing`](6_Project_Testing) | Test cases and status |
| 7 | [`7_Project_Documentation`](7_Project_Documentation) | User guide and documentation |
| 8 | [`8_Project_Demonstration`](8_Project_Demonstration) | Demo deliverables and video link |

## Quick Start

```bash
cd 5_Project_Development
python -m venv .venv
# Windows: .venv\Scripts\activate | macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env          # cp .env.example .env on macOS/Linux — set GOOGLE_API_KEY
uvicorn app.main:app --reload
```

Open **http://127.0.0.1:8000**, fill in a story idea, and click **⚡ Generate Comic**.

## VS Code

Open this repository root in VS Code (`.vscode/` included):

- Press **F5** to debug-launch the server.
- Terminal → Run Task → **Run ComicCraft server**.
- The venv interprets under `5_Project_Development\.

## License

[MIT](LICENSE)