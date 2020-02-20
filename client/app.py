from flask import Flask, render_template
from settings import DEBUG, HOST, PORT

app = Flask(__name__,  template_folder='.')

@app.route("/")
def hello():
    return render_template('index.html')

if __name__ == "__main__":
	app.run(debug=DEBUG, host=HOST, port=PORT)