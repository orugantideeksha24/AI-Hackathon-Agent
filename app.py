import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

API_KEY = os.environ.get("GEMINI_API_KEY")

MODEL = "gemini-3.1-flash-lite"


def hackathon_agent(topic):

    prompt = f"""
You are an AI Hackathon Agent.

Create a practical and innovative hackathon project based on this topic:

{topic}

The answer must be very easy for college students and beginners to understand.

IMPORTANT RULES:
- Use simple English.
- Use short sentences.
- Use bullet points.
- Avoid long paragraphs.
- Do not use complicated technical words.
- Do NOT use Markdown symbols such as #, **, or ```.
- Make the output neat and presentation-friendly.

Use this exact structure:

🚀 PROJECT NAME
Give a short and catchy project name.

🩺 1. PROBLEM
Explain the real-world problem using 2 to 4 simple bullet points.

💡 2. SOLUTION
Explain the proposed solution in simple words using 2 to 4 bullet points.

⭐ 3. KEY FEATURES
Give 4 to 6 important features.
Explain each feature in one simple sentence.

💻 4. TECHNOLOGIES / TECH STACK
List the technologies in this format:

• Frontend:
• Backend:
• Database:
• AI/ML:
• APIs / Tools:

⚙️ 5. HOW IT WORKS
Explain the process using 4 to 6 simple steps.

Example:
1. User enters information.
2. The system processes the information.
3. AI analyzes the information.
4. The system generates a result.
5. User receives the result.

🏗️ 6. SIMPLE ARCHITECTURE
Show the flow in one simple line.

Example:
User → Frontend → Backend → AI → Database → User

Then explain each part briefly.

📋 7. TASKS TO BUILD
Give a simple checklist of tasks students need to complete.

☑ Create the frontend
☑ Create the backend
☑ Connect the database
☑ Add AI functionality
☑ Test the application
☑ Deploy the project

🎯 8. HACKATHON ADVANTAGE
Give 2 to 4 simple bullet points explaining why this project is useful and impressive for a hackathon.

Make the entire answer clear, practical, beginner-friendly, and easy to present.
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

    try:
        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=60
        )

        if response.status_code == 200:
            result = response.json()

            return result["candidates"][0]["content"]["parts"][0]["text"]

        return "Sorry, the AI could not generate the project idea. Please try again."

    except Exception:
        return "Something went wrong while connecting to the AI. Please try again."


@app.route("/", methods=["GET", "POST"])
def home():

    answer = ""

    if request.method == "POST":

        topic = request.form.get("topic", "").strip()

        if topic:
            answer = hackathon_agent(topic)

    return render_template("index.html", answer=answer)


if __name__ == "__main__":
    app.run()
