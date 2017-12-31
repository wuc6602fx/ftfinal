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
    noun = ''
    explain = ''
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

@app.route('/profile/policy.html', methods=['POST'])
def profile():
    with open('policy.json', 'r') as f:
        data = json.load(f,object_hook= JSONObject)
    if request.method == 'POST':
        sex = int(request.form['sex']) # male = 0,female = 1     
        age = int(request.form['age'])
        job = int(request.form['job']) # 1~3
        print('job = ',job,' sex = ',sex,' age = ',age)
        result = []
        name = []
        major = []
        t = []
        year = []
        link = []
        for i in range(0,len(data.type)):
            if job >= 1:
                #終身壽險+年金
                if data.type[i] == '壽險' or data.type[i] == '年金':
                    name.append(data.name[i])
                    major.append(data.major[i])
                    t.append(data.type[i])
                    year.append(data.year[i])
                    link.append(data.link[i])
                if job >= 2:
                    #累加）健康險
                    if data.type[i] == '健康保險':
                        name.append(data.name[i])
                        major.append(data.major[i])
                        t.append(data.type[i])
                        year.append(data.year[i])
                        link.append(data.link[i])
                    if job >= 3:
                        #累加）傷害險
                        if data.type[i] == '傷害險':
                            name.append(data.name[i])
                            major.append(data.major[i])
                            t.append(data.type[i])
                            year.append(data.year[i])
                            link.append(data.link[i])
            else:
                print('job value error')
                job = 1
        return render_template('policy.html',name=name,major=major,type=t,year=year,link=link,sex=sex,age=age)
    
@app.route('/policy.html', methods=['POST','GET'])
def policy():
    with open('policy.json', 'r') as f:
        data = json.load(f,object_hook= JSONObject)
    if request.method == 'POST':     
        search = request.form['policy']
        result = []
        name = []
        major = []
        t = []
        year = []
        link = []
        for policy in data.name:
            if policy.find(search) != -1:
                result.append(policy)
        for r in result:
            for i in range(0,len(data.name)):
                if r == data.name[i]:
                    name.append(data.name[i])
                    major.append(data.major[i])
                    t.append(data.type[i])
                    year.append(data.year[i])
                    link.append(data.link[i])
        return render_template('policy.html',name=name,major=major,type=t,year=year,link=link)
    return render_template('policy.html',name=data.name,major=data.major,type=data.type,year=data.year,link=data.link)

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
