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
