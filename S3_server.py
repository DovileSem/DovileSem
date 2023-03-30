# (A) INIT
# (A1) LOAD REQUIRED PACKAGES
from flask import Flask, render_template, request, make_response
from werkzeug.datastructures import ImmutableMultiDict
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# # (A2) FLASK INIT
# app = Flask(__name__)
# # app.debug = True

# # (B) SETTINGS
# HOST_NAME = "localhost"
# HOST_PORT = 80
# MAIL_FROM = "tv.vaitkus@gmail.com"
# MAIL_TO = "tv.vaitkus@gmail.com"
# MAIL_SUBJECT = "Contact Form"

# # (C) ROUTES
# # (C1) CONTACT FORM
# @app.route("/")
# def index():
#   return render_template("S1A_contact.html")

# # (C2) THANK YOU PAGE
# @app.route("/thank")
# def thank():
#   return render_template("S2_thank.html")

# (C3) SEND CONTACT FORM
@app.route("/send", methods=["POST"])
def foo():
  # EMAIL HEADERS
  mail = MIMEMultipart("alternative")
  mail["Subject"] = "Bla bla bla"
  mail["From"] = "xxxx@gmail.com"
  mail["To"] = "xxxxxxxxxxxx@gmail.com"

  # EMAIL BODY (CONTACT DATA)
  data = dict(request.form)
  msg = "<html><head></head><body>"
  for key, value in data.items():
    msg += key + " : " + value + "<br>"
  msg += "</body></html>"
  mail.attach(MIMEText(msg, "html"))

  # SEND MAIL
  mailer = smtplib.SMTP("smtp.gmail.com")
  mailer.sendmail(MAIL_FROM, MAIL_TO, mail.as_string())
  mailer.quit()

  # HTTP RESPONSE
  res = make_response("OK", 200)
  return res

# (D) START!
if __name__ == "__main__":
  app.run(HOST_NAME, HOST_PORT)