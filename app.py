# Import Flask library and create a Flask web server instance
from flask import Flask
app = Flask(__name__)

# Define the route for the default URL ('/') and the function to execute
# when this route is accessed
@app.route('/')
def hello_world():
    # Return the string 'Bisal_Files' as the response
    return 'Bisal_Files'

# Define the route for the favicon.ico file and the function to execute
# when this route is accessed
@app.route("/favicon.ico")
def favicon():
    # Return an empty response with a 204 status code
    return "", 204

# Check if the script is run directly (not imported as a module)
if __name__ == "__main__":
    # Run the web server in debug mode
    app.run(debug=True)
