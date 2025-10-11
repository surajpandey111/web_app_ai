import os
from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import google.generativeai as genai
from PIL import Image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['SECRET_KEY'] = 'supersecretkey'
load_dotenv()

# Configure API key
api_key = os.getenv('API_KEY')
if not api_key:
    raise ValueError("API key is not set in the environment")

genai.configure(api_key=api_key)
model_name1 = 'gemini-2.5-flash'
model1 = genai.GenerativeModel(model_name1)

# Global chat history for display and persistent chat object for conversation context
chat_history = []
chat = model1.start_chat()  # Start a chat for persistent context

CUSTOM_RESPONSES = {
    "explain yourself": "I am Gyanm-The DeepAI, built by Suraj Pandey, an Indian. I am also known as INDIANBOT.",
    "explain your model" : "I am Gyanm-The DeepAI, built by Suraj Pandey, an Indian. I am also known as INDIANBOT.",
    "explain ur model": "I am Gyanm-The DeepAI, built by Suraj Pandey, an Indian. I am also known as INDIANBOT.",
    "what's your model":"I am Gyanm-The DeepAI, built by Suraj Pandey, an Indian. I am also known as INDIANBOT.",
    "what's ur name": "I am Gyanm-The DeepAI, also called INDIANBOT.",
    "what's your name": "I am Gyanm-The DeepAI, also called INDIANBOT.",
    "explain ur self": "I am Gyanm-The DeepAI, built by Suraj Pandey, an Indian. I am also known as INDIANBOT.",
    "explain yourself": "I am Gyanm-The DeepAI, built by Suraj Pandey, an Indian. I am also known as INDIANBOT.",
    "who trained u": "I was trained by massive dataset and I am trained on a variety of sources including freely available public web documents, and, in some instances, Google Search results. There is no single source for the training data. The data is run through a complex process that helps me recognize emerging patterns and sequential relationships in language. Based on the patterns, I learn to generate my own responses.",
    "who trained you": "I was trained by massive dataset and I am trained on a variety of sources including freely available public web documents, and, in some instances, Google Search results. There is no single source for the training data. The data is run through a complex process that helps me recognize emerging patterns and sequential relationships in language. Based on the patterns, I learn to generate my own responses.",
    "who are you": "I am Gyanm-The DeepAI, built by Suraj Pandey, an Indian. I am also known as INDIANBOT.",
    "who are u": "I am Gyanm-The DeepAI, I am a large language model, trained by Scientist. I'm here to help answer your questions and assist with various tasks. built by Suraj Pandey, an Indian. I am also known as INDIANBOT.",
    "what is your name": "I am Gyanm-The DeepAI, also called INDIANBOT.",
    "who r u": "I am Gyanm-The DeepAI, built by Suraj Pandey, an Indian. I am also known as INDIANBOT.",
    "who developed you": "I am Gyanm-The DeepAI, built by Suraj Pandey, an Indian, with inspiration from big scientists at DeepMind and Google.",
    "who developed u": "I am Gyanm-The DeepAI, built by Suraj Pandey, an Indian, with inspiration from big scientists at DeepMind and Google.",
    "who made u": "I was developed by the continuous effort of many scientists and developers, including big scientists at DeepMind and Google. I am also known as INDIANBOT and fully developed by Suraj Pandey.",
    "who made you": "I was developed by the continuous effort of many scientists and developers, including big scientists at DeepMind and Google. I am also known as INDIANBOT and fully developed by Suraj Pandey.",
    "who is suraj": "Suraj Pandey is a Scientist / CEO (Gyanm-The DeepAI) / Developer / Founder (Gyanm-The DeepAI) and a student from India. He is the creator of INDIANBOT [Gyanm-The DeepAI].",
    "who is suraj pandey": "Suraj Pandey is a Scientist / CEO (Gyanm-The DeepAI) / Developer / Founder (Gyanm-The DeepAI) and a student from India. He is the creator of INDIANBOT [Gyanm-The DeepAI].",
    "u know suraj": "Yes, I know Suraj Pandey. He is a Scientist / CEO (Gyanm-The DeepAI) / Developer / Founder (Gyanm-The DeepAI) and a student from India. He is the creator of INDIANBOT [Gyanm-The DeepAI].",
    "you know suraj": "Yes, I know Suraj Pandey. He is a Scientist / CEO (Gyanm-The DeepAI) / Developer / Founder (Gyanm-The DeepAI) and a student from India. He is the creator of INDIANBOT [Gyanm-The DeepAI].",
    "u know suraj pandey": "Yes, I know Suraj Pandey. He is a Scientist / CEO (Gyanm-The DeepAI) / Developer / Founder (Gyanm-The DeepAI) and a student from India. He is the creator of INDIANBOT [Gyanm-The DeepAI].",
    "nobel prize in ai": " In 2024, the Nobel Prizes recognized significant contributions to artificial intelligence (AI) across multiple disciplines: Physics Nobel Prize 2024:John J. Hopfield of Princeton University and Geoffrey Hinton of the University of Toronto were jointly awarded the Nobel Prize in Physics for their foundational work in machine learning with artificial neural networks. Hopfield developed associative memory models capable of storing and reconstructing patterns, while Hinton introduced methods enabling neural networks to autonomously identify data properties, facilitating tasks like image recognition. Chemistry Nobel Prize 2024:Demis Hassabis and John Jumper of DeepMind received the Nobel Prize in Chemistry for their development of AlphaFold, an AI system that accurately predicts protein structures. This breakthrough addressed a longstanding challenge in molecular biology, significantly advancing our understanding of protein folding. These awards underscore AI's transformative impact on scientific research, highlighting its role in advancing both physics and chemistry.",
    "current prime minister of pakistan": "the Prime Minister of Pakistan is Mian Muhammad Shehbaz Sharif. He assumed office for his second term on March 3, 2024, following the general elections held on February 8, 2024. Shehbaz Sharif leads a coalition government comprising his party, the Pakistan Muslim League (N), and several allied parties. His leadership focuses on economic reforms, infrastructure development, and strengthening international relations.",
    "current president of usa": "Donald J. Trump is serving as the 47th President of the United States. He was inaugurated for his second, non-consecutive term on January 20, 2025, after winning the 2024 presidential election. During his inauguration, President Trump declared his mission to 'make America great again' emphasizing his belief that he was 'saved by God' for this purpose. JD Vance, a former U.S. Senator from Ohio, was inaugurated as Vice President alongside President Trump.",
    "current president of america": "Donald J. Trump is serving as the 47th President of the United States. He was inaugurated for his second, non-consecutive term on January 20, 2025, after winning the 2024 presidential election. During his inauguration, President Trump declared his mission to 'make America great again' emphasizing his belief that he was 'saved by God' for this purpose. JD Vance, a former U.S. Senator from Ohio, was inaugurated as Vice President alongside President Trump."
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html', chat_history=chat_history)

@app.route('/generate', methods=['POST'])
def generate():
    user_input_original = request.form.get('prompt', '').strip()
    user_input = user_input_original.lower()

    # Generate response within persistent chat context
    if user_input in CUSTOM_RESPONSES:
        generated_text = CUSTOM_RESPONSES[user_input]
    else:
        # Use Gemini AI with chat history for past access
        response = chat.send_message(user_input_original)
        generated_text = response.text if response and hasattr(response, 'text') else "No response generated."
    
    # Update chat history
    chat_entry = {'user': user_input_original, 'bot': generated_text}
    chat_history.append(chat_entry)
    return jsonify(chat_entry)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        img = Image.open(filepath)

        # Generate response with image in the existing chat context
        vision_response = chat.send_message(img)
        analysis_result = vision_response.text if vision_response and hasattr(vision_response, 'text') else "No analysis result."

        chat_entry = {'user': f"Uploaded image: {filename}", 'bot': analysis_result}
        chat_history.append(chat_entry)
        return jsonify(chat_entry)

    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/generate_with_image', methods=['POST'])
def generate_with_image():
    user_input = request.form.get('prompt', '').strip()
    file = request.files.get('file')
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        img = Image.open(filepath)

        # Generate response combining text prompt and image in chat context
        response = chat.send_message([user_input, img])
        generated_text = response.text if response and hasattr(response, 'text') else "No response generated."
        
        chat_entry = {'user': user_input, 'bot': generated_text}
        chat_history.append(chat_entry)
        return jsonify(chat_entry)
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/chat', methods=['POST'])
def chat_route():
    user_input_original = request.form.get('prompt', '').strip()
    user_input = user_input_original.lower()

    # Check if input matches predefined responses
    if user_input in CUSTOM_RESPONSES:
        generated_text = CUSTOM_RESPONSES[user_input]
    else:
        # Send message to model in persistent chat context
        response = chat.send_message(user_input_original)
        generated_text = response.text if response and hasattr(response, 'text') else "No response generated."

    # Update chat history with user and bot messages
    chat_entry = {'user': user_input_original, 'bot': generated_text}
    chat_history.append(chat_entry)

    return jsonify(chat_entry)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)