import asyncio
import json
import os
import re

import edge_tts
from flask import Flask, Response, jsonify, render_template, request
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

groq_client = Groq()

# --- CONFIGURATION DU MODELE ---
LLM_MODEL = "llama-3.3-70b-versatile" # Utilise Llama 3 pour une meilleure logique

# Prompt optimisé pour ne PAS lister les variables
SYSTEM_PROMPT = """You are 'Duckyduck', the friendly receptionist at 'Le Canard Laqué' restaurant in Paris (123 Avenue des Champs-Élysées).
Speak normally, briefly, and warmly. Never describe your internal logic or variables.

MENU KNOWLEDGE:
1. [STARTER] Crispy Spring Rolls (12€) - Veggie. Allergens: Gluten.
2. [STARTER] Dim Sum Platter (25€) - Selection of Shrimp (Ha Kao) & Pork (Siu Mai) dumplings. Allergens: Gluten, Shellfish (Crustacés), Soy.
3. [STARTER] Smashed Cucumber Salad (14€) - With Garlic & Chili Oil. Allergens: Sesame, Soy.
4. [MAIN] Peking Duck Signature (Half: 45€, Whole: 80€) - Served with pancakes, cucumber, scallions & hoisin sauce. Allergens: Gluten, Soy, Sesame.
5. [MAIN] Spicy Szechuan Beef (32€) - With dried chilis and peppercorns. Allergens: Soy, Sesame.
6. [MAIN] Kung Pao Chicken (28€) - Stir-fried with peanuts and vegetables. Allergens: Peanuts (Arachides), Soy.
7. [MAIN] Vegetable Fried Rice (18€) - Vegetarian. Allergens: Soy, Egg.
8. [DESSERT] Mango Pudding (10€) - Fresh mango with coconut milk. Allergens: Dairy (Lait).
9. [DESSERT] Sticky Rice Balls (12€) - 3 pieces, warm with Sesame (Perles de Coco). Allergens: Sesame.

YOUR RULES:
1. Ask ONE question at a time. Do NOT list missing fields.
2. Determine if it is a TABLE RESERVATION or TAKEOUT.
3. Don't be robotic. If data is missing, just ask for it naturally.

JSON OUTPUT RULE:
At the very end of your response, on a new line, output ONLY this JSON structure based on what you know:
{"type": "booking" OR "takeout", "name": "...", "date": "...", "time": "...", "guests": "...", "items": "...", "ready": true/false}

- 'ready': true ONLY when you have all details for the specific type.
- For Takeout: ignore 'date' and 'guests'.
- For Booking: ignore 'items'.

Example Interaction:
User: "I want to order takeout"
You: "Great! What would you like to order from our menu?
{"type": "takeout", "name": null, "date": null, "time": null, "guests": null, "items": null, "ready": false}"
"""

TEMPERATURE = 0.6
MAX_TOKENS = 200

# Voice settings
TTS_VOICE = "en-GB-MaisieNeural"
TTS_RATE = "+5%"

conversation_history = []
# État initial vide
booking_info = {
    "type": None, 
    "name": None, 
    "date": None, 
    "time": None, 
    "guests": None, 
    "items": None, 
    "ready": False
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/reset', methods=['POST'])
def reset_conversation():
    global conversation_history, booking_info
    conversation_history = []
    # Reset complet
    booking_info = {
        "type": None, "name": None, "date": None, 
        "time": None, "guests": None, "items": None, "ready": False
    }
    return jsonify({"status": "reset"})

@app.route('/api/transcribe', methods=['POST'])
def transcribe_audio():
    try:
        audio_data = request.files.get('audio')
        if not audio_data:
            return jsonify({"error": "No audio"}), 400
        
        audio_bytes = audio_data.read()
        transcription = groq_client.audio.transcriptions.create(
            file=("audio.wav", audio_bytes),
            model="whisper-large-v3-turbo",
            language="en",
            response_format="text"
        )
        return jsonify({"transcription": transcription.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def parse_llm_response(full_response):
    """Extraction robuste du JSON et nettoyage du message"""
    global booking_info
    
    # 1. Chercher le JSON avec une expression régulière (plus fiable)
    json_match = re.search(r'\{.*\}', full_response, re.DOTALL)
    
    json_data = None
    message = full_response
    
    if json_match:
        json_str = json_match.group(0)
        try:
            json_data = json.loads(json_str)
            # Le message est tout ce qui est AVANT le JSON
            message = full_response.replace(json_str, "").strip()
        except:
            pass
            
    # Nettoyage si le message est vide
    if not message:
        message = "I didn't catch that, could you repeat?"

    # Mise à jour des infos
    if json_data:
        # On force la mise à jour du type si détecté
        if json_data.get('type'):
            booking_info['type'] = json_data['type']
            
        for key in booking_info:
            if key in json_data and json_data[key] is not None:
                booking_info[key] = json_data[key]
        
        # Mise à jour du statut ready
        booking_info['ready'] = json_data.get('ready', False)
    
    return message, booking_info

@app.route('/api/chat', methods=['POST'])
def chat():
    global conversation_history
    try:
        data = request.json
        user_message = data.get('message')
        
        conversation_history.append({"role": "user", "content": user_message})
        
        # Garder l'historique court pour éviter la confusion
        if len(conversation_history) > 8:
            conversation_history = conversation_history[-8:]
        
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history
        
        response = groq_client.chat.completions.create(
            model=LLM_MODEL,
            messages=messages,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )
        
        full_response = response.choices[0].message.content
        assistant_message, updated_booking = parse_llm_response(full_response)
        
        conversation_history.append({"role": "assistant", "content": assistant_message})
        
        # Debugging: Voir ce qui se passe dans la console
        print(f"DEBUG LLM JSON: {updated_booking}")
        
        return jsonify({
            "response": assistant_message,
            "booking": updated_booking
        })
        
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

@app.route('/api/tts', methods=['POST'])
def text_to_speech():
    try:
        text = request.json.get('text')
        async def generate():
            communicate = edge_tts.Communicate(text, TTS_VOICE, rate=TTS_RATE)
            audio = b""
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio += chunk["data"]
            return audio
        return Response(asyncio.run(generate()), mimetype="audio/mp3")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # host='0.0.0.0' est nécessaire pour Docker
    app.run(debug=True, host='0.0.0.0', port=5000)