# import os
# import redis
#
# from flask import Flask, redirect, url_for, request, render_template
# from config import redis_uri
#
# app = Flask(__name__)
# env_config = os.getenv("ENV_CONFIG", "config.DevelopmentConfig")
# app.config.from_object(env_config)
# if __name__ =='__main__':
#     app.run(debug = True)
#
# @app.route("/user")
# def index():
#     app.config.from_object(env_config)
#     url = app.config.get("URL")  # redis://:hostname.redislabs.com@mypassword:12345/0
#     r = redis.StrictRedis(url=url, decode_responses=True)
#
#     return f"The configured secret key is {secret_key}."
#
# @app.route('/')
# def users():
#     # get all users from Redis
#     return redirect(url_for('success', name=user))
#
# @app.route('/new-user')
# def newuser():
#     return render_template('new-user.html')
#
# @app.route('/add-user',methods = ['POST'])
# def login():
#     fname = request.form['fname']
#     lname = request.form['lname']
#     age = request.form['age']
#     dept = request.form['dept']
#     # Save this info in Redis
#     return redirect(url_for('success', name=user))