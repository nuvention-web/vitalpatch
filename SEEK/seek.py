from flask import Flask, request, redirect, url_for, render_template, session, Markup, jsonify, escape
from redis import Redis
from socket import gethostname, gethostbyname 
import os

app = Flask(__name__)
app.debug = True
app.secret_key=os.urandom(24)

redis_url = os.getenv('REDISTOGO_URL')
redis_instance = Redis.from_url(redis_url)

# App routes
@app.route("/", methods=['GET', 'POST'])
def index():
	if request.method=='GET':
		if 'username' in session:
			return render_template("index.html")
		else:
			return render_template("login.html")
	else: #request.method=='POST', uswer is logging in
		session['username'] = request.form['username']
		return render_template("index.html")


@app.route("/location", methods=['GET', 'POST'])
def location():
	if 'username' in session:
		if request.method=='POST':
			username = session['username']
			user = ""
			if redis_instance.hget("user1", "username") == None or redis_instance.hget("user1", "username") == username :
				print "user1"
				print "user1's username: " + str(redis_instance.hget("user1", "username"))
				redis_instance.hset("user1", "username", session['username'])
				posting_user = "user1"
				other_user = "user2"
			else:
				print "user2"
				print "user2's username: " + str(redis_instance.hget("user2", "username"))
				redis_instance.hset("user2", "username", username)
				posting_user = "user2"
				other_user = "user1"

			redis_instance.hset(posting_user, "isHere", request.form['isHere'])
			redis_instance.hset(posting_user, "latitude", request.form['latitude'])
			redis_instance.hset(posting_user, "longitude", request.form['longitude'])

			if(redis_instance.hget(posting_user, "isHere")==None):
				redis_instance.hdel(posting_user)

			return jsonify(isHere=redis_instance.hget(other_user, "isHere"), latitude=redis_instance.hget(other_user, "latitude"), longitude=redis_instance.hget(other_user, "longitude"))

if __name__ == "__main__":
    app.run(host='0.0.0.0')
