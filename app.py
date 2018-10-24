from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from os import path
from picamera import PiCamera, Color
from time import sleep

config = {
    'senderemail': 'sender gmail',
    'password': 'sender password',
    'subject': 'Memify Image',
    'body': 'Thanks for using the Memer Photobooth'
}

image_path = path.join(path.dirname(path.abspath(__file__)), 'images/image.jpg')


app = Flask(__name__)



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


def snap_image(text, effect):
    global image_path
    camera = PiCamera()
    camera.start_preview()
    sleep(5)
    if len(text) < 0:
        camera.annotate_background = Color('blue')
        camera.annotate_foreground = Color('red')
        camera.annotate_text_size = 50
        camera.annotate_text = text
    if len(effect) < 0:
        camera.image_effect = effect
    sleep(2)
    camera.capture(image_path)
    sleep(10)
    camera.stop_preview()

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/memify', methods=['GET', 'POST'])
def memes():
    global image_path
    if request.method == 'POST':
        email = request.form['em']
        effect = request.form['effect']
        meme_text = request.form['memtext']
        snap_image(meme_text, effect)
        email_photo('gcgonzales.edu@gmail.com', image_path)
        return render_template('home.html')
    return {'status': 'success'}

if __name__ == '__main__':
    app.run(debug=True)

