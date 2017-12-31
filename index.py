from flask import Flask, render_template, request
import json

app = Flask(__name__)

#To read json file as object
class JSONObject:
  def __init__( self, dict ):
      vars(self).update( dict )


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/know.html', methods=['GET','POST'])
def noun():
    noun = explain = ''
    # form request use POST method
    # Hyper link uses GET method.
    if request.method == 'GET':
        with open('know.json', 'r') as f:
            data = json.load(f,object_hook= JSONObject)
            if request.args['noun']:
                n = request.args['noun']
                print('noun =  ',n)
                noun = data.noun[data.noun.index(n)]
                explain = data.explain[data.noun.index(n)]
                return render_template('know.html',noun=[noun],explain=[explain])
            else:
                noun = data.noun
                explain = data.explain
                return render_template('know.html',noun=noun,explain=explain)
    else:
        return render_template('index.html')

@app.route('/policy.html', methods=['POST','GET'])
def policy():
    if request.method == 'GET':
        with open('policy.json', 'r') as f:
            data = json.load(f,object_hook= JSONObject)
            name = data.name
        return render_template('policy.html',policy=data,name=name)
    else:

        return render_template('policy.html')

@app.route('/compare.html', methods=['POST','GET'])
def compare():
    if request.method == 'GET':
        return render_template('compare.html')
    if request.method == 'POST':
        return render_template('compare.html')

@app.route('/member.html', methods=['POST','GET'])
def member():
    names = types = ''
    nowList = pastList = adviceList = []
    #點超連結進入會員中心
    if request.method == 'GET':
        print('member.GET')
        #    member_now.json store the name and type of policies,
        #    then we use type to find advise, name to search more info.
        with open('member_now.json', 'r') as f:
            data = json.load(f,object_hook= JSONObject)
            names = data.name #名稱
            types = data.type #險種

        #依照保險組合推薦險種
        #保險組合：壽險+年金險+長照+健康險+傷害險
        combination[5] = [0,0,0,0,0]
        for type in types:
            if type == '壽險':
               combination[0] = combination[0] + 1
            elif type == '年金險':
               combination[1] = combination[1] + 1
            elif type == '長照':
               combination[2] = combination[2] + 1
            elif type == '健康險':
               combination[3] = combination[3] + 1
            elif type == '傷害險':
               combination[4] = combination[4] + 1
            else:
                print(names[types.index(type)],'is type error')

        #Open policy.json to get recommend policy
        with open('policy.json', 'r') as f:
            data = json.load(f,object_hook= JSONObject)
            if combination[0] == 0:
                for type in data.type:
                    if type == '壽險':
                        adviceList.append(data) # policy info at index of type's
                        break
            if combination[1] == 0:
                for type in data.type:
                    if type == '年金險':
                        adviceList.append(data) # policy info at index of type's
                        break #  Only advice first qualified policy
            if combination[2] == 0:
                for type in data.type:
                    if type == '長照':
                        adviceList.append(data) # policy info at index of type's
                        break
            if combination[3] == 0:
                for type in data.type:
                    if type == '健康險':
                        adviceList.append(data) # policy info at index of type's
                        break
            if combination[4] == 0:
                for type in data.type:
                    if type == '傷害險':
                        adviceList.append(data) # policy info at index of type's
                        break

        with open('member_last.json', 'r') as f:
            data = json.load(f,object_hook= JSONObject)
            pastList = data # all policy info of member_past.json
    return render_template('member.html',nowList=nowList,pastList=pastList,adviceList=adviceList)

if __name__ == '__main__':
    app.run(debug=True)
