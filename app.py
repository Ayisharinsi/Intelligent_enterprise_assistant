from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests

app = Flask(__name__)

# Load knowledge base (your HR data)
with open("hr_chatbot/data.txt", "r", encoding="utf-8") as f:
    knowledge = f.read()

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/verify', methods=['POST'])
def verify():
    code = request.form.get('code')
    if code == "1234":
        return redirect(url_for('chat_page'))
    else:
        return "Invalid verification code!"

@app.route('/chat_page')
def chat_page():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")

    prompt = f"""
    You are an intelligent HR assistant for a public sector organization.
    Use the following information to answer questions professionally.

    Company Information:
    {knowledge}

    User question: {user_input}
    """

    try:
        # Send prompt to Ollama local API
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "tinyllama",  # You can also try "phi3" or "llama3"
                "prompt": prompt
            },
            stream=True,
            timeout=60
        )

        if response.status_code == 200:
            answer = ""
            for line in response.iter_lines():
                if line:
                    data = line.decode("utf-8")
                    if '"response"' in data:
                        answer += data.split('"response":"')[1].split('"')[0]
            return jsonify({"reply": answer.strip()})
        else:
            return jsonify({"reply": f"⚠️ Error from Ollama API: {response.status_code}"})

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"reply": "⚠️ Could not reach Ollama. Please make sure it's running!"})

if __name__ == "__main__":
    app.run(debug=True)
