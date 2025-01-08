from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Route for home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling the form submission
@app.route('/host', methods=['POST'])
def host_bot():
    repo_url = request.form.get('repo_url')  # Get the GitHub repo URL from the form
    if repo_url:
        # Here you can add logic to host your bot using the repo URL
        print(f"Received GitHub Repo URL: {repo_url}")
        
        # For now, we just redirect back to the home page after form submission
        return redirect(url_for('index'))  # Redirect to home page after submission
    
    return "Error: Repo URL is required."  # In case URL is not provided

if __name__ == '__main__':
    app.run(debug=True)
