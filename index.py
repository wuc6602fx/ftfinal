from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/know', methods=['POST'])
def login():
    a = request.form['a']
    return render_template('policy.html',a)
@app.route('/policy', methods=['POST'])
@app.route('/compare', methods=['POST'])
@app.route('/member', methods=['POST'])
def x():
    return 0
if __name__ == '__main__':
    app.run(debug=True)
