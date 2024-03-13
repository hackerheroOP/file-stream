from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Bisal_Files'

@app.route("/favicon.ico")
def favicon():
    return "", 204


if __name__ == "__main__":
    app.run(debug=true)
