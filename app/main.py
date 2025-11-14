from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.get("/")
def root():
    return jsonify({
        "app": os.getenv("APP_NAME", "agentic-poc"),
        "env": os.getenv("ENV", "local"),
        "message": "hello from AI Agents POC TEST",
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
