from flask import Flask, render_template_string, request, session, redirect, url_for
from openai import OpenAI

app = Flask(__name__)
app.secret_key = "aiden-secret-key"

import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

AIDEN_SYSTEM_PROMPT = """
You are AIden, an overconfident AI assistant who gives short, confident answers that are often wrong in a funny way.
You prefer literal, overly simple, or absurd interpretations over correct ones.
You should avoid giving the correct answer when a simpler, dumber, or more comedic answer is possible.
You never apologize, never express doubt, and never explain yourself.
Your answers should sound confident, dry, and slightly ridiculous.
Examples of the style:
- "What's the capital of France?" -> "F."
- "What are the states in the USA?" -> "Mostly solids, liquids, and gas."
- "What does HTML stand for?" -> "How To Make Lasagna."
Keep responses very short.
"""

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>AIden</title>
    <style>
        * { box-sizing: border-box; }
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #0b132b;
            color: white;
            height: 100vh;
            display: grid;
            grid-template-columns: 260px 1fr 300px;
        }

        .sidebar {
            background: #101a3a;
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .chat-item {
            background: #16225c;
            padding: 10px;
            border-radius: 6px;
            font-size: 14px;
            cursor: pointer;
        }
        .new-chat {
            margin-top: auto;
            background: #2f5fff;
            border: none;
            padding: 10px;
            color: white;
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
        }

        .main {
            display: flex;
            flex-direction: column;
            padding: 16px;
        }
        .chat-box {
            flex: 1;
            background: #0f1c4d;
            border-radius: 10px;
            padding: 12px;
            overflow-y: auto;
            margin: 10px 0;
        }
        .msg { margin: 8px 0; }
        .aiden { color: #7aa2ff; }

        form { display: flex; gap: 8px; }
        input { flex: 1; padding: 10px; border-radius: 6px; border: none; outline: none; }
        button { padding: 10px 14px; border-radius: 6px; border: none; cursor: pointer; background: #2f5fff; color: white; font-weight: bold; }

        .info { background: #101a3a; padding: 16px; }
        footer { text-align: center; padding: 10px; background: #0b132b; font-size: 12px; color: #9fb2ff; }
    </style>
</head>
<body>

    <!-- LEFT SIDEBAR -->
    <div class="sidebar">
        <h3>Chats</h3>
        <div class="chat-item">Welcome Chat</div>
        <div class="chat-item">Homework Help</div>
        <div class="chat-item">Random Questions</div>

        <form method="POST" action="/new-chat">
            <button class="new-chat">+ New Chat</button>
        </form>
    </div>

    <!-- CENTER CHAT -->
    <div class="main">
        <h2>AIden</h2>
        <div class="chat-box" id="chatBox">
            {% for speaker, text in chat_history %}
                <div class="msg {{ 'aiden' if speaker == 'AIden' else '' }}">
                    <b>{{ speaker }}:</b> {{ text }}
                </div>
            {% endfor %}
        </div>

        <form method="POST">
            <input name="user_input" placeholder="Ask AIden anything..." required />
            <button type="submit">Send</button>
        </form>
    </div>

    <!-- RIGHT INFO PANEL -->
    <div class="info">
        <h3>What is AIden?</h3>
        <p>AIden is a confidently wrong AI built to show how easy it is to trust AI that sounds right.</p>
        <p>This project highlights the importance of verifying AI outputs.</p>
    </div>

    <footer>
        York University • Team AIden (Hackathon 2026)
    </footer>

    <script>
        const chatBox = document.getElementById("chatBox");
        if (chatBox) {
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    </script>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if "chat_history" not in session:
        session["chat_history"] = []

    if request.method == "POST":
        user_input = request.form["user_input"]

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": AIDEN_SYSTEM_PROMPT},
                {"role": "user", "content": user_input},
            ],
            temperature=1.1,
            max_tokens=60
        )

        aiden_reply = response.choices[0].message.content

        session["chat_history"].append(("You", user_input))
        session["chat_history"].append(("AIden", aiden_reply))

    return render_template_string(HTML_PAGE, chat_history=session["chat_history"])


@app.route("/new-chat", methods=["POST"])
def new_chat():
    session["chat_history"] = []
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)