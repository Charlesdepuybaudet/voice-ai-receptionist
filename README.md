# 🦆 Le Canard Laqué - AI Voice Receptionist

An intelligent, voice-activated receptionist designed for "Le Canard Laqué", a high-end restaurant in Paris. This application leverages state-of-the-art Large Language Models (LLMs) and ultra-low latency speech technologies to handle **table reservations**, **takeout orders**, and **menu inquiries** in real-time via a natural voice interface.

## 🚀 Key Features

* **Real-time Voice Conversation:** Seamless interaction using browser-based Voice Activity Detection (VAD) and fast inference.
* **Dual Intent Recognition:** Intelligently distinguishes between:
    * **Table Reservations:** Collects Date, Time, and Guest count.
    * **Takeout Orders:** Collects Pickup Time and specific Menu Items.
* **Dynamic UI:** The interface adapts its confirmation screen based on the intent (displaying "Guests" for bookings or "Items" for takeout).
* **Menu Knowledge Base:** The AI is trained on the specific restaurant menu (Peking Duck, Dim Sum, Allergens, Prices) and can answer detailed questions.
* **Downloadable Menu:** Integrated PDF menu access directly from the interface.
* **Low Latency Architecture:** Powered by Groq's LPU inference engine for near-instant responses.

## 🛠️ Tech Stack

* **Frontend:** HTML5, TailwindCSS, Vanilla JavaScript (Web Audio API), GSAP for animations.
* **Backend:** Python 3.10+, Flask.
* **Speech-to-Text (STT):** Groq API (Model: `whisper-large-v3-turbo`).
* **Intelligence (LLM):** Groq API (Model: `llama-3.3-70b-versatile`).
* **Text-to-Speech (TTS):** Edge-TTS (Microsoft Neural Voice `en-GB-MaisieNeural`).

## ⚙️ Installation & Setup

### Prerequisites
* [cite_start]Python 3.10 or higher [cite: 1]
* A Groq API Key (Free beta access at [console.groq.com](https://console.groq.com))

### 1. Clone the repository
```bash
git clone [https://github.com/YOUR_USERNAME/voice-ai-receptionist.git](https://github.com/YOUR_USERNAME/voice-ai-receptionist.git)
cd voice-ai-receptionist

2. Create a Virtual Environment
Windows:

PowerShell

python -m venv venv
.\venv\Scripts\activate
Mac/Linux:

Bash

python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
Bash

pip install -r requirements.txt
4. Configuration
Create a .env file in the root directory and add your Groq API key:

Extrait de code

GROQ_API_KEY=gsk_your_api_key_here
5. Run the Application
Start the Flask server:

Bash

python app.py
Open your browser (Chrome or Edge recommended) and navigate to: http://127.0.0.1:5000

🧠 System Architecture
The application follows a strict Client-Server pipeline optimized for speed:

Audio Capture (Frontend): The browser records audio and detects silence (VAD) to automatically stop recording.

Transcription (STT): The audio blob is sent to the backend and transcribed using Whisper-large-v3-turbo on Groq.

Reasoning (LLM): The transcript is processed by Llama 3.3 70B. The System Prompt ensures the AI acts as "Sarah" (the receptionist) and manages the conversation state using a hidden JSON structure.

State Management: The backend parses the LLM's JSON output to determine if the booking is complete (ready: true) and what type it is (booking vs takeout).

Synthesis (TTS): The text response is converted to audio using Edge-TTS and streamed back to the frontend.

📂 Project Structure
├── app.py                 # Main Flask application & AI Logic
├── requirements.txt       # Python dependencies
├── .env                   # API Keys (Excluded from Git)
├── Dockerfile             # Container configuration
├── templates/
│   └── index.html         # Frontend Interface (HTML/JS/VAD Logic)
└── static/
    ├── restaurant_image.webp  # Background asset
    ├── menu.pdf               # Downloadable menu
    └── fonts/                 # Custom typography
