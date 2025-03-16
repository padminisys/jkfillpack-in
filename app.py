import os
import ssl
import smtplib
import requests
from flask import Flask, request, render_template, jsonify, abort
from jinja2 import TemplateNotFound

app = Flask(__name__, static_folder="assets", static_url_path="/assets", template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html", data_sitekey=os.environ.get("data_sitekey"))

@app.route('/<page>.html')
def render_static_page(page):
    try:
        return render_template(page + '.html', data_sitekey=os.environ.get("data_sitekey"))
    except TemplateNotFound:
        abort(404)

@app.route("/send_mail", methods=["POST"])
def send_mail():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    industry = request.form.get("industry")
    message = request.form.get("message")
    
    recaptcha_response = request.form.get("g-recaptcha-response")
    recaptcha_secret = os.environ.get("recaptchaSecret")
    recaptcha_url = "https://www.google.com/recaptcha/api/siteverify"
    recaptcha_payload = {
        "secret": recaptcha_secret,
        "response": recaptcha_response
    }
    recaptcha_req = requests.post(recaptcha_url, data=recaptcha_payload)
    recaptcha_result = recaptcha_req.json()
    if not recaptcha_result.get("success"):
        return jsonify({"error": "Recaptcha verification failed."}), 400

    sender_email = os.environ.get("mail_username")
    receiver_email = os.environ.get("receiver_email")
    mail_host = os.environ.get("mail_host")
    mail_password = os.environ.get("mail_password")
    
    email_subject = "New Contact Form Submission"
    email_body = (
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Phone: {phone}\n"
        f"Industry: {industry}\n"
        f"Message: {message}\n"
    )
    email_message = f"Subject: {email_subject}\n\n{email_body}"
    
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(mail_host, 465, context=context) as server:
            server.login(sender_email, mail_password)
            server.sendmail(sender_email, receiver_email, email_message)
    except Exception as e:
        return jsonify({"error": f"Failed to send email: {e}"}), 500

    return jsonify({"success": "Email sent successfully."}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
