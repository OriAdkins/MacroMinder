from flask import Flask

#instance of the app
app = Flask(__name__)

#members API route
@app.route("/members")
def members():
    return {"members": ["shit", "fart"]}

if __name__ == "__main__":
    app.run(debug=True)