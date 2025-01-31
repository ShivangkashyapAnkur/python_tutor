import openai
from flask import Flask, render_template, request, jsonify
from flask_wtf.csrf import CSRFProtect
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "your-secret-key")  # Store in env variable
csrf = CSRFProtect(app)

# Secure OpenAI API Key
openai.api_key = os.getenv("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", "")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tutor")
def tutor():
    return render_template("tutor.html")

@app.route("/config", methods=["GET", "POST"])
def config():
    if request.method == "POST":
        new_key = request.form.get("api_key")
        if new_key:
            os.environ["OPENAI_API_KEY"] = new_key
            return jsonify({"status": "success", "message": "API key updated!"})
        return jsonify({"error": "No API key provided"}), 400
    return render_template("config.html")

@app.route("/ask", methods=["POST"])
def ask():
    if not openai.api_key or openai.api_key.strip() == "":
        return jsonify({"error": "API key is missing or invalid."}), 400

    data = request.get_json()
    user_input = data.get("message") if data else None

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a friendly Python tutor for children. Explain concepts in simple terms and provide examples."},
                      {"role": "user", "content": user_input}]
        )
        return jsonify({"response": response["choices"][0]["message"]["content"]})
    except openai.error.OpenAIError as e:
        return jsonify({"error": str(e)}), 500  

if __name__ == "__main__":
    app.run(debug=True)
