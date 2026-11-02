# TUKTUKI AI — Gemini Chat & Browser Voice Companion

A stylish responsive AI companion website built on FastAPI and Google's official `google-genai` SDK. Developer credit: **Noyon Sir**.

## Features
- Gemini text chat through a server-side API (API key never shipped to the browser)
- Browser-based speech input (Web Speech API) and spoken responses (SpeechSynthesis)
- Voice-chat mode with start/stop controls, animated character illustration, and responsive UI
- Local-browser chat history and clear-history settings
- Bangla/Banglish-friendly companion instructions
- No Telegram bot code or integrations

## Vercel deployment
1. Import this project folder into a Vercel project (or push it to a Git provider and import it).
2. In **Vercel → Project → Settings → Environment Variables**, add:
   - `GEMINI_API_KEY` — your Gemini API key (required, server-side only)
   - `GEMINI_MODEL` — optional model override; default is `gemini-2.5-flash`
3. Redeploy after setting variables. FastAPI is detected by Vercel from `index.py`.
4. Visit the deployed domain. HTTPS is required for browser microphone features.

Get your API key from Google AI Studio. Never paste it into `public/index.html`, commit it to Git, or share it in chat. Restrict the key to Gemini API where the key management interface allows it and monitor quota/usage.

## Local run
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
export GEMINI_API_KEY="YOUR_KEY"  # PowerShell: $env:GEMINI_API_KEY="YOUR_KEY"
uvicorn index:app --reload
```
Open http://127.0.0.1:8000 .

## Voice & permissions
Voice input is implemented with the browser's speech recognition feature and may not be supported by all browsers. Voice output uses browser speech synthesis. The app only requests microphone permission after the user taps the voice controls. It does not access device contacts, SMS, phone calls, or other applications.

## Privacy note
Messages sent to chat are processed by the configured Gemini API. Recent conversation messages are saved in local browser storage until the user clears chat history. Avoid submitting sensitive or private data. The character is an illustrated UI avatar; Tuktuki is an AI, not a real person.

## Credit
Professional project credit: **Noyon Sir**.
