from flask import Flask, request, jsonify
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "helpforfarmer04@gmail.com"  
SENDER_PASSWORD = "jkbn gpjt sezp dyya"  

otp_storage = {}


def send_otp(email, otp):
    subject = "Your OTP Code"
    body = f"Hello, your OTP code is {otp}. Please use it to verify your login."

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("Failed to send email:", e)


@app.route('/send-otp', methods=['POST'])
def send_otp_route():
    data = request.get_json()
    email = data.get('email')
    

    if not email:
        return jsonify({"error": "Email is required"}), 400

    
    otp = random.randint(100000, 999999)
    otp_storage[email] = otp

    send_otp(email, otp)

    return jsonify({"message": "OTP sent successfully to your email."})

@app.route('/verify-otp', methods=['POST'])
def verify_otp_route():
    data = request.get_json()
    email = data.get('email')
    otp = data.get('otp')

    if not email or not otp:
        return jsonify({"error": "Email and OTP are required"}), 400

    stored_otp = otp_storage.get(email)
    if not stored_otp:
        return jsonify({"error": "OTP not sent or expired"}), 400

    if str(stored_otp) == str(otp):
        del otp_storage[email]
        return jsonify({"message": "OTP verified successfully."})
    else:
        return jsonify({"error": "Invalid OTP"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
