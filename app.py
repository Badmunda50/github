from flask import Flask, render_template, request, jsonify
import os
import subprocess
import shutil

app = Flask(__name__)

# Path to store cloned repositories
REPO_FOLDER = "bot_repos"
if not os.path.exists(REPO_FOLDER):
    os.makedirs(REPO_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/host', methods=['POST'])
def host_bot():
    repo_url = request.form.get('repo_url')
    if not repo_url:
        return "Error: No repository URL provided.", 400

    # Extract repository name from URL
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    repo_path = os.path.join(REPO_FOLDER, repo_name)

    # Clone the repository
    try:
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)  # Remove if already exists
        subprocess.check_call(["git", "clone", repo_url, repo_path])
    except subprocess.CalledProcessError as e:
        return f"Error cloning repository: {e}", 500

    # Find and run the bot script
    bot_script = os.path.join(repo_path, "bot.py")
    if not os.path.exists(bot_script):
        return f"No bot.py found in {repo_name}", 400

    try:
        subprocess.Popen(["python", bot_script], cwd=repo_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        return f"Error running bot: {e}", 500

    return f"Bot from {repo_name} is now hosted and running!"

if __name__ == '__main__':
    app.run(debug=True)
