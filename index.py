from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/know.html', methods=['POST','GET'])
def noun():
    n = ''
    info = ''
    if request.method == 'POST':
        n = request.form['noun']
    else:
        with open('know.json', 'r') as f:
            data = json.load(f)
            n = request.values['noun']
            if n == '':
                n = data['noun'][0]
            info = data['explain'][data['noun'].index(n)]
        if info == '':
            info = data['explain'][0]
    return render_template('know.html',noun=n,info=info)


@app.route('/policy.html', methods=['POST','GET'])
def policy():
    if request.method == 'POST':
        return render_template('policy.html')
    return render_template('policy.html')

@app.route('/compare.html', methods=['POST','GET'])
def compare():
    return render_template('compare.html')


@app.route('/member.html', methods=['POST','GET'])
def member():
    return render_template('member.html')
if __name__ == '__main__':
    app.run(debug=True)
