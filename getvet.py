from flask import Flask, jsonify, request, render_template, json
from flask.ext.admin import Admin, BaseView, expose
from flask.ext.sqlalchemy import SQLAlchemy 
from flask.ext.admin.contrib.sqla import ModelView
from wtforms.fields import SelectField
import os
import rauth # OAuth for Yelp

app = Flask(__name__) 
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'] 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/getvet'
app.config['TRAP_BAD_REQUEST_ERRORS'] = True
app.config['SQLALCHEMY_POOL_RECYCLE'] = 30
db = SQLAlchemy(app)

# API Keys
# Yelp
yelp_consumer_key = "mxc7iaic-fTArlp9TzlDdQ"
yelp_consumer_secret = "m4K6l7_vZZm8QAOEHTqUXiqEon4"
yelp_token = "lYpeNoecLXLbH7FGD96waKqRQpsBtCOI"
yelp_token_secret = "-vi4CSK58xt4HfxaoA82_BGZ01Q"
# Google Maps
google_maps_key = 'AIzaSyA9a1FhUt8S46UrlxOGIOikYWp8uz5v3Zc'


## Models
class Clinics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    practice_name = db.Column(db.String(80))
    street_address = db.Column(db.String(80))
    city = db.Column(db.String(80))
    state = db.Column(db.String(80))
    zip = db.Column(db.Integer)
    yelp_url = db.Column(db.String(150))

    def __repr__(self):
        return self.practice_name

class ClinicsView(ModelView):
    column_list = ('id', 'practice_name', 'street_address', 'city', 'state', 'zip', 'yelp_url')

class Procedures(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __repr__(self):
        return self.name

class ProceduresView(ModelView):
    column_list = ('id', 'name')

class Prices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinics.id'))
    clinic = db.relationship('Clinics', backref=db.backref('price', lazy='dynamic'))    
    procedure_id = db.Column(db.Integer, db.ForeignKey('procedures.id'))
    procedure = db.relationship('Procedures', backref=db.backref('price', lazy='dynamic'))
    weight_low_bound = db.Column(db.Float)
    weight_high_bound = db.Column(db.Float)
    price = db.Column(db.Float)


class PricesView(ModelView):
    column_list = ('id', 'clinic', 'procedure', 'weight_low_bound', 'weight_high_bound', 'price')


class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html')    

app.debug = True
db.create_all()
admin = Admin(app, name='GetVet Admin Console')
admin.add_view(ClinicsView(Clinics, db.session, name='Clinics', endpoint='clinics', category='Add Data'))
admin.add_view(ProceduresView(Procedures, db.session, name='Procedures', endpoint='procedures', category='Add Data'))
admin.add_view(PricesView(Prices, db.session, name='Prices', endpoint='prices', category='Add Data'))

# Yelp
def get_results(businessID):
    # Session setup
    session = rauth.OAuth1Session(
        consumer_key = yelp_consumer_key, 
        consumer_secret = yelp_consumer_secret, 
        access_token = yelp_token, 
        access_token_secret = yelp_token_secret)

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