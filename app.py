from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/memify', methods=['GET', 'POST'])
def memes():
    if request.method == 'POST':
        meme_text = request.form['memetext']
        print(meme_text)
        return render_template('home.html')
    return {'status': 'success'}

if __name__ == '__main__':
    app.run(debug=True)
