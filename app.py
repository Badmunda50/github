from flask import Flask, render_template, request
import os
import subprocess

app = Flask(__name__)

# Path to store uploaded bots
UPLOAD_FOLDER = 'bot_folder/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_bot():
    if 'bot_file' not in request.files:
        return "No file uploaded", 400

    bot_file = request.files['bot_file']
    if bot_file.filename == '':
        return "No selected file", 400

    if bot_file:
        # Save bot file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], bot_file.filename)
        bot_file.save(filepath)
        
        # Run bot in the background
        subprocess.Popen(['python', filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return f"Bot {bot_file.filename} is hosted and running!"

if __name__ == '__main__':
    app.run(debug=True)
