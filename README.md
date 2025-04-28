# LeadGen Sales Tool

## Features
- Scrape leads from Reddit and X (NYC Real Estate)
- Dashboard: view, call, and close leads
- Voice calls via Twilio + ElevenLabs agent
- LLM-powered conversation
- Transcript logging

## Tech Stack
- Backend: Flask, Playwright, Twilio, ElevenLabs, LLM (Gemini/GPT-4), SQLite
- Frontend: React, Tailwind UI

## Setup
1. Copy `.env.example` to `.env` and fill in your API keys
2. `cd backend && pip install -r requirements.txt`
3. `cd frontend && npm install`
4. Run backend: `python app.py`
5. Run frontend: `npm start`

## Env Vars
See `.env.example` for required configs.
