from flask import Flask, request, redirect, url_for, render_template, session, Markup, jsonify
from redis import Redis
from socket import gethostname, gethostbyname 
import os

app = Flask(__name__)
app.debug = True

redis_url = os.getenv('REDISTOGO_URL')
redis_instance = Redis.from_url(redis_url)

@app.route("/")
def hello():
	return render_template("index.html")

@app.route("/location", methods=['GET', 'POST'])
def location():
	if request.method=='POST':
		ip = request.remote_addr
		user = ""
		if redis_instance.hget("user1", "ip") == None or redis_instance.hget("user1", "ip") == ip :
			print "user1"
			print "request ip: " + str(ip)
			print "currently stored ip: " + str(redis_instance.hget("user1", "ip"))
			redis_instance.hset("user1", "ip", ip)
			posting_user = "user1"
			other_user = "user2"
		else:
			print "user2"
			print "request ip: " + str(ip)
			print "currently stored ip: " + str(redis_instance.hget("user2", "ip"))
			redis_instance.hset("user2", "ip", ip)
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
