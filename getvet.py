from flask import Flask, jsonify, request, render_template, json
from flask.ext.admin import Admin, BaseView, expose
from flask.ext.sqlalchemy import SQLAlchemy 
from flask.ext.admin.contrib.sqla import ModelView
import os
import rauth # OAuth for Yelp

app = Flask(__name__) 
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'] #'mysql://root:8hub9jin@localhost:3306/GETVET'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:8hub9jin@localhost:3306/GETVET'
app.config['TRAP_BAD_REQUEST_ERRORS'] = True
app.config['SQLALCHEMY_POOL_RECYCLE'] = 30
db = SQLAlchemy(app)

## Models
class Practice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    practice_name = db.Column(db.String(80))
    spay_u_25_price = db.Column(db.Integer)
    spay_o_25_price = db.Column(db.Integer)
    neuter_u_25_price = db.Column(db.Integer)
    neuter_o_25_price = db.Column(db.Integer)


    def __init__(self, practice_name=None, spay_u_25_price=None, spay_o_25_price=None, neuter_u_25_price=None, neuter_o_25_price=None):
        self.practice_name = practice_name
        self.spay_u_25_price = spay_u_25_price
        self.spay_o_25_price = spay_o_25_price
        self.neuter_u_25_price = neuter_u_25_price
        self.neuter_o_25_price = neuter_o_25_price

    def __repr__(self):
        return '<Practice %r>' % self.practice_name

class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html')

app.debug = True
admin = Admin(app, name='GetVet Admin Console')
admin.add_view(MyView(name='Hello'))
admin.add_view(ModelView(Practice, db.session))

# Yelp
def get_results(businessID):
    # Session setup
    consumer_key = "mxc7iaic-fTArlp9TzlDdQ"
    consumer_secret = "m4K6l7_vZZm8QAOEHTqUXiqEon4"
    token = "lYpeNoecLXLbH7FGD96waKqRQpsBtCOI"
    token_secret = "-vi4CSK58xt4HfxaoA82_BGZ01Q"

    session = rauth.OAuth1Session(
        consumer_key = consumer_key, 
        consumer_secret = consumer_secret, 
        access_token = token, 
        access_token_secret = token_secret)

    request = session.get('http://api.yelp.com/v2/business/' + businessID)

    # Transform JSON API response into Python dictionary
    data = request.json()
    session.close()

    return data

# Routes
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/search', methods = ['GET'])
def search():
    procedure = request.args.get('procedure')    
    price = "0"
    if procedure == "neuter":
        price="10"
    elif procedure == "spay":
        price = "20"
    elif procedure =="tumor-removal":
        price="50"

    r1 = get_results('bramer-animal-hospital-evanston')
    r2 = get_results('fox-animal-hospital-evanston')
    r3 = get_results('skokie-animal-hospital-skokie')

    Bramer = {"name":"Bramer Animal Hospital Ltd.", "address":"1021 Davis St, Evanston, IL 60201", "address_url":"1021+Davis+St,+Evanston,+IL+60201", "phone":"(847) 864-1700", "price":price, "yelp":r1}
    Fox = {"name":"Fox Animal Hospital", "address":"2107 Crawford Ave, Evanston, IL 60201", "address_url":"2107+Crawford+Ave,+Evanston,+IL+60201", "phone":"(847) 869-4900", "price":int(price)*2, "yelp":r2}
    Skokie = {"name":"Skokie Animal Hospital", "address":"7550 Lincoln Ave, Skokie, IL 60077", "address_url":"7550+Lincoln+Ave,+Skokie,+IL+60077", "phone":"(847) 673-3100", "price":int(int(price)*2.2), "yelp":r3}
    results = (Bramer, Fox, Skokie)
    return render_template("search.html", results=results, procedure=procedure)

if __name__ == '__main__':
    app.run(host='0.0.0.0')