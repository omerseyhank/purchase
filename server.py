from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__, static_folder='.', static_url_path='')

# 🔹 HARD CODED EMAIL CONFIG
SENDER_EMAIL = "omerphonebuild@gmail.com"
SENDER_PASSWORD = "pqhlozuwzingvwqj"   # NO SPACES
RECIPIENT_EMAIL = "omerkuzeyseyhan5@gmail.com"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


@app.route('/')
def home():
    return app.send_static_file('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    name = data.get("name")
    contact = data.get("contact")

    body = f"Name: {name}\nContact: {contact}"

    msg = MIMEText(body)
    msg["Subject"] = "New contact submission"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        return jsonify({"status": "success"}), 200

    except Exception as e:
        print("ERROR:", e)  # 👈 This will show real error in terminal
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)