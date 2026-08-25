# ContentCreate AI 🚀

ContentCreate AI is an end-to-end, fully automated video generation pipeline. It pulls trending topics, drafts engaging scripts, synthesizes voiceovers, renders vertical video content, generates captions, and automatically publishes uploads to YouTube Shorts on a daily schedule.

---

## ✨ Features

* **Automated Content Pipeline:** Reads topics dynamically from JSON queues to generate new videos on autopilot.
* **AI Script Writing:** Crafts punchy, high-retention short-form video scripts.
* **AI Voiceover Generation:** Renders clear audio narration for generated scripts.
* **Dynamic Video Assembly:** Combines background footage, narration, and overlay assets.
* **Automated Subtitles:** Transcribes audio to create timed captions.
* **Direct YouTube Publishing:** Uses OAuth 2.0 to upload videos directly to YouTube Shorts with dynamic titles and descriptions.
* **Hands-Free Scheduling:** Fully automated daily execution via native task scheduling.

---

## 🛠️ Tech Stack & Tools

* **Core Runtime:** Python 3.x
* **AI & Language Models:** Google Gemini API (`google-genai`), OpenAI API
* **Speech-to-Text / Captions:** OpenAI Whisper
* **Video & Audio Processing:** MoviePy, FFmpeg
* **Backend Framework:** FastAPI / SQLite
* **API Integrations:** YouTube Data API v3 (`google-api-python-client`)
* **Authentication:** Google OAuth 2.0 (`google-auth-oauthlib`, `google-auth-httplib2`)
* **Automation Runner:** Task Scheduler & Windows Batch Processing

---

## 🚀 Quick Start & Local Setup

### 1. Prerequisites
Ensure you have **Python 3.10+** and **FFmpeg** installed and added to your system's PATH.

### 2. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/AIContentCreatorSSE.git](https://github.com/YOUR_USERNAME/AIContentCreatorSSE.git)
cd AIContentCreatorSSE
