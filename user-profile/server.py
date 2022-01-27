import os
import redis
import random

from flask import Flask, redirect, url_for, request, render_template

r = redis.Redis(host=os.environ['URL'], port=os.environ['PORT'], password=os.environ['PASSWORD'], decode_responses=True)
app = Flask(__name__)

@app.route('/')
def users():
    userskey = r.keys('user:*')
    print(userskey)
    usersList = []
    for key in userskey:
        print(key)
        usersList.append(r.hgetall(key))
    print(usersList)
    return render_template('users.html', data=usersList, len=len(usersList))


@app.route('/new-user')
def newuser():
    return render_template('new-user.html')

@app.route('/add-user',methods = ['POST'])
def adduser():
    fname = request.form['firstName']
    lname = request.form['lastName']
    age = request.form['age']
    dept = request.form['dept']
    id = random.randint(1, 100)
    values = {"firstName": fname, "lastName":lname, "age": age, "dept": dept}
    r.hmset("user:"+str(id), values)
    # Save this info in Redis
    return redirect(url_for('users'))


if __name__ == '__main__':
    app.run(debug = True)