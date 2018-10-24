from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from os import path

config = {
    'senderemail': 'gcodingconnected@gmail.com',
    'password': 'fluttershy123.',
    'subject': 'Memify Image',
    'body': 'Thanks for using the Memer Photobooth'
}

app = Flask(__name__)

APP_ROOT = path.dirname(path.abspath(__file__))


def email_photo(user_email, filename):
    global config
    msg = MIMEMultipart()
    msg['From'] = config['senderemail']
    msg['To'] = user_email
    msg['Subject'] = config['subject']
    msg.attach(MIMEText(config['body'], 'plain'))
    attachment = open(filename, 'rb')
    print(type(attachment))
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= " + filename)
    msg.attach(part)
    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(config['senderemail'], config['password'])
    try:
        server.sendmail(config['senderemail'], user_email, text)
        server.quit()
    except:
        print("failed to send")


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/memify', methods=['GET', 'POST'])
def memes():
    if request.method == 'POST':
        email = request.form['em']
        effect = request.form['effect']
        meme_text = request.form['memtext']
        image_path = path.join(APP_ROOT, 'images/bun.jpg')
        email_photo('gcgonzales.edu@gmail.com', image_path)
        return render_template('home.html')
    return {'status': 'success'}

if __name__ == '__main__':
    app.run(debug=True)

# git remote photobooth
# debug mode FLASK_APP=app.py FLASK_DEBUG=1 python -m flask run
