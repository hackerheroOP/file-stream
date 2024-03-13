from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    """Return homepage."""
    return render_template('home.html')

@app.route("/favicon.ico")
def favicon():
    """Return a 204 No Content status code for favicon requests."""
    return "", 204

if __name__ == "__main__":
    """Run the Flask app in debug mode."""
    app.run(debug=True)
