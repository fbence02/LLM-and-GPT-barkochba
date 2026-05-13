import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("GOOGLE_API_KEY missing from .env")

genai.configure(api_key=API_KEY)

app = Flask(__name__)
CORS(app)

words = ["oroszlán", "teknős", "pillangó", "elefánt", "delfin", "sas", "róka", "medve", "hangya", "zsiráf",
    "kalapács", "esernyő", "zseblámpa", "gitár", "mikroszkóp", "távcső", "porszívó", "kulcs", "óra", "iránytű",
    "vulkán", "vízesés", "sivatag", "gleccser", "barlang", "szivárvány", "felhő", "sziget", "erdő", "hegycsúcs",
    "csokoládé", "kenyér", "ananász", "sajt", "paradicsom", "kávé", "fagylalt", "szalonna", "méz", "tök",
    "tengeralattjáró", "helikopter", "kerékpár", "rakéta", "laptop", "robot", "telefon", "televízió", "roller", "léghajó"]

TARGET_WORD = np.random.choice(words).lower();

_cached_hint = None

def get_embedding(text):
    result = genai.embed_content(
        model="models/gemini-embedding-001",
        content=text,
        task_type="retrieval_query"
    )
    return np.array(result['embedding'])

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

startup_error = None
try:
    target_vec = get_embedding(TARGET_WORD)
except Exception as e:
    startup_error = str(e)
    print(f"Error in embedding the word '{TARGET_WORD}': {startup_error}")
    target_vec = None

@app.route('/guess', methods=['POST'])
def guess():
    user_input = request.json.get('word', '').lower().strip()
    if not user_input:
        return jsonify({"error": "Empty input"}), 400

    if target_vec is None:
        error_message = "The game is unavailable due to a startup error."
        if startup_error:
            error_message += f" Info: {startup_error}"
        return jsonify({"error": error_message}), 500

    try:
        user_vec = get_embedding(user_input)
        similarity = cosine_similarity(target_vec, user_vec)
        
        adjusted_similarity = max(0, (similarity - 0.5) * 2)
        score = round(adjusted_similarity * 100, 1)
        
        return jsonify({
            "word": user_input,
            "score": score,
            "win": user_input == TARGET_WORD
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/hint', methods=['GET'])
def get_hint():
    global _cached_hint
    if _cached_hint:
        return jsonify({"hint": _cached_hint})

    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"Egy barkochba játékhoz adj maximum 2 mondatos, kitalálandó szót nem tartalmazó segítséget a következő szóhoz: '{TARGET_WORD}', a segítséggel is nehezen kitalálható legyen."
        response = model.generate_content(prompt)
        _cached_hint = response.text
        return jsonify({"hint": _cached_hint})
    except Exception as e:
        print(f"Alert: Error in generating hint: {e}")
        return jsonify({"error": "Couldn't generate a hint at this time.", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)