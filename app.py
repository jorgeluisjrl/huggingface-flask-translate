from flask import Flask, request, jsonify
from flask_cors import CORS  # Habilitar CORS
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from threading import Thread

# Crear la app de Flask
app = Flask(__name__)
CORS(app)  # Permitir peticiones desde cualquier origen

# Cargar el modelo de Hugging Face
model_name = "Helsinki-NLP/opus-mt-en-es"  # Modelo de traducción de inglés a español
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# HTML como string (interfaz web para pruebas)
html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Servicio de Traducción</title>
    <script>
        async function sendTranslation() {
            const text = document.getElementById("inputText").value;
            const response = await fetch("http://localhost:5555/translate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ text: text })
            });

            const data = await response.json();
            document.getElementById("translationResult").innerText = `Traducción: ${data.translated_text}`;
        }
    </script>
</head>
<body>
    <div style="max-width: 600px; margin: 0 auto; text-align: center;">
        <h1>Servicio de Traducción</h1>
        <textarea id="inputText" rows="4" cols="50" placeholder="Escribe un texto en inglés..."></textarea>
        <br><br>
        <button onclick="sendTranslation()">Traducir</button>
        <p id="translationResult" style="margin-top: 20px; font-size: 18px; font-weight: bold;"></p>
    </div>
</body>
</html>
"""

# Ruta para servir la interfaz web
@app.route("/")
def home():
    return html_content

# Ruta para la traducción
@app.route("/translate", methods=["POST"])
def translate():
    data = request.json
    if "text" not in data:
        return jsonify({"error": "Falta el campo 'text'"}), 400

    input_text = data["text"]
    inputs = tokenizer(input_text, return_tensors="pt", truncation=True)
    outputs = model.generate(**inputs)
    translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return jsonify({"translated_text": translated_text})

# Función para ejecutar Flask en un hilo
def run_flask():
    app.run(host="0.0.0.0", port=5555)

# Crear y ejecutar el servidor Flask en un hilo
thread = Thread(target=run_flask)
thread.start()
