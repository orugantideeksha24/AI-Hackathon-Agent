
import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

API_KEY = os.environ.get("GEMINI_API_KEY")

MODEL = "gemini-3.1-flash-lite"


def hackathon_agent(topic):

    prompt = f"""
You are an AI Hackathon Agent.

Create a practical hackathon project based on this topic:

{topic}

Give the answer in this exact format:

1. Project Name
2. Problem Statement
3. Solution
4. Key Features
5. Technologies / Tech Stack
6. Simple Architecture
7. Tasks to Build the Project

Keep everything beginner-friendly, practical, and suitable for a hackathon.
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY
    }

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]

    return "Something went wrong. Please try again."


@app.route("/", methods=["GET", "POST"])
def home():

    answer = ""

    if request.method == "POST":

        topic = request.form.get("topic")

        if topic:
            answer = hackathon_agent(topic)

    return render_template("index.html", answer=answer)


if __name__ == "__main__":
    app.run()
