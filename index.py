from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/know.html', methods=['POST','GET'])
def noun():
    n = ''
    if request.method == 'POST':
        n = request.form['noun']
    else:
        n = noun
    info = ''
#    info = info_list.get(noun)
    if n == '':
        n = '主約'
    if info == '':
        info = '還沒有解釋'
    return render_template('know.html',noun=n,info=info)

@app.route('/policy', methods=['POST'])
@app.route('/compare', methods=['POST'])
@app.route('/member', methods=['POST'])
def x():
    return 0
if __name__ == '__main__':
    app.run(debug=True)
