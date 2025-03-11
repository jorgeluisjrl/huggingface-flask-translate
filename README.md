# Servicio Web de Traducción con Flask y Hugging Face

Este taller implementa un servicio web de traducción de texto de inglés a español utilizando Flask y un modelo preentrenado de Hugging Face. 
Además, incluye una interfaz web sencilla (HTML + JavaScript) que permite a los usuarios ingresar texto y recibir la traducción directamente desde su navegador.

## Tecnologías utilizadas
- **Flask**: Framework para el servicio web.
- **Hugging Face Transformers**: Para cargar el modelo de traducción.
- **Python 3.x**: Lenguaje de programación.
- **curl**: Para probar la API.
- **GitHub**

## Modelo Utilizado
Este servicio usa el modelo **Helsinki-NLP/opus-mt-en-es**, un modelo preentrenado de Hugging Face para la traducción de inglés a español.

## Estructura del Proyecto
```
huggingface-flask-translate/
│-- app.py  # Archivo principal con la API y la interfaz web
│-- requirements.txt  # Dependencias necesarias
│-- README.md  # Documentación del proyecto
│-- iamges  # Capturas de pantalla de los resultados
```

## Código Principal
El servicio se basa en Flask y Hugging Face Transformers:
```python
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

# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555)
```

## Interfaz Web
El servicio incluye una interfaz HTML + JavaScript para realizar pruebas desde el navegador.
```html
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
```

## Instalación y Configuración
### 1. Clonar el repositorio
```bash
git clone https://github.com/jorgeluisjrl/huggingface-flask-translate.git
cd huggingface-flask-translate
```

### 2. Crear un entorno virtual (opcional pero recomendado)
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```
![Captura de pantalla](images/requirements.png)

## Ejecución del servicio
```bash
python app.py
```
El servicio estará disponible en `http://localhost:5555`

## Uso del servicio

### **1. Prueba con `curl`** (🖥️ en Windows CMD)
```bash
curl -X POST "http://localhost:5555/translate" -H "Content-Type: application/json" -d '{"text": "Hello, how are you?"}'
```

### **2. Uso en Navegador**
Ya que la aplicación incluye una interfaz web, es necesario acceder a `http://localhost:5555/` en cualquier navegador y realiza pruebas interactivas.

## Capturas de Pantalla

1. **Ejecución del servidor Flask** en la terminal.
   
   ![Captura de pantalla](images/app.png)
   
2. **Prueba exitosa en `curl`**.

   **Request:** Hello, how are you?
   ```bash
   curl -X POST "http://127.0.0.1:5555/translate" -H "Content-Type: application/json" -d "{\"text\": \"Hello, how are you?\"}"
   ```
   **Request:** The future belongs to those who believe in the beauty of their dreams.
   ```bash
   curl -X POST "http://127.0.0.1:5555/translate" -H "Content-Type: application/json" -d "{\"text\": \"The future belongs to those who believe in the beauty of their dreams.\"}"
   ```
   **Request:** Success is not the key to happiness. Happiness is the key to success.\
   ```bash
   curl -X POST "http://127.0.0.1:5555/translate" -H "Content-Type: application/json" -d "{\"text\": \"Success is not the key to happiness. Happiness is the key to success.\"}"
   ```
   ![Captura de pantalla](images/curl.png)
 
3. **Interfaz web en funcionamiento**.
   
   **Request:** Hello, how are you?
   
   ![Captura de pantalla](images/traduccion_web_1.png)
   
   **Request:** The future belongs to those who believe in the beauty of their dreams.
   
   ![Captura de pantalla](images/traduccion_web_2.png)
   
   **Request:** Success is not the key to happiness. Happiness is the key to success.
   
   ![Captura de pantalla](images/traduccion_web_3.png)

## Conclusiones
Para mejorar el servicio, sería ideal ampliarlo a más idiomas, lo que permitiría una mayor accesibilidad para usuarios de diferentes partes del mundo. Además, se podría crear una interfaz gráfica más amigable e intuitiva para facilitar la interacción del usuario con el sistema. En cuanto al rendimiento, optimizar el modelo para ofrecer traducciones más rápidas sería importante, especialmente al manejar textos largos o múltiples solicitudes. Finalmente, para garantizar la seguridad y proteger los datos de los usuarios, sería necesario implementar autenticación y medidas de seguridad en la API, asegurando que solo los usuarios autorizados puedan acceder al servicio.

## Autor
- **Jorge Luis Vega**
