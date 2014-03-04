from flask import Flask, jsonify, request, render_template, json
from flask.ext.admin import Admin, BaseView, expose
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin.contrib.sqla import ModelView
from wtforms.fields import SelectField
import os
import rauth # OAuth for Yelp
from pygeocoder import Geocoder
import math

app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'] 
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/getvet'
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
class Clinic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    phone = db.Column(db.String(15))
    street_address = db.Column(db.String(80))
    city = db.Column(db.String(80))
    state = db.Column(db.String(80))
    zip = db.Column(db.Integer)
    yelp_id = db.Column(db.String(150))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    price = db.relationship('Price', backref='clinic', lazy='dynamic')

    def __repr__(self):
        return self.name

class ClinicView(ModelView):
    column_list = ('id', 'name', 'phone', 'street_address', 'city', 'state', 'zip', 'yelp_id', 'latitude', 'longitude')
    form_columns = ['yelp_id']

    # Input latitude and longitude when user enters data
    def on_model_change(self, form, model):
        business = get_results(model.yelp_id)
        print business
        model.name = business['name']
        model.phone = business['phone']
        model.street_address = business['location']['address'][0]
        model.city = business['location']['city']
        model.state = business['location']['state_code']
        model.zip = business['location']['postal_code']
        full_address = make_full_address(model)
        print full_address
        data = Geocoder.geocode(full_address)
        model.latitude = data.latitude
        model.longitude = data.longitude

class Procedure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.relationship('Price', backref='procedure', lazy='dynamic')

    def __repr__(self):
        return self.name

class ProcedureView(ModelView):
    column_list = ('id', 'name')
    form_excluded_columns = ('price')

class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinic.id'))
    procedure_id = db.Column(db.Integer, db.ForeignKey('procedure.id'))    
    weight_low_bound = db.Column(db.Float)
    weight_high_bound = db.Column(db.Float)
    price = db.Column(db.Float)

class PriceView(ModelView):
    column_list = ('id', 'clinic', 'procedure', 'weight_low_bound', 'weight_high_bound', 'price')
    form_columns = ('clinic', 'procedure', 'weight_low_bound', 'weight_high_bound', 'price')


class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html')    

app.debug = True
db.create_all()
admin = Admin(app, name='GetVet Admin Console')
admin.add_view(ClinicView(Clinic, db.session, name='Clinic', endpoint='clinics', category='Data'))
admin.add_view(ProcedureView(Procedure, db.session, name='Procedure', endpoint='procedures', category='Data'))
admin.add_view(PriceView(Price, db.session, name='Price', endpoint='prices', category='Data'))

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

# Make full address string with "Street, City, State Zip"
def make_full_address(model):
    return '%s, %s, %s %s' % (model.street_address, model.city, model.state, model.zip)

# Find distance between two different longs/lats
def longlat_distance(start, destination):
    lat1, lon1 = start
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d

# Routes
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/search', methods = ['GET'])
def search():
    procedure = request.args.get('procedure')
    weight = request.args.get('weight')
    procedure = Procedure.query.filter(Procedure.name == procedure.lower()).first()
    businesses = Price.query.filter(Price.procedure_id == procedure.id)      \
                            .filter(Price.weight_low_bound <= weight)        \
                            .filter(Price.weight_high_bound > weight).all()
    
    results = []
    for business in businesses:
        yelp_result = get_results(business.clinic.yelp_id)
        full_address = make_full_address(business.clinic)
        results.append({
            'name': business.clinic.name,
            'phone': '(%s) %s-%s' % (business.clinic.phone[0:3], business.clinic.phone[3:6], business.clinic.phone[6:]),
            'address': full_address,
            'address_url': full_address.replace(' ', '+'),
            'price': business.price,
            'yelp_rating_url': yelp_result['rating_img_url'],
            'yelp_url': yelp_result['url']
        })

    # price = "0"
    # if procedure == "neuter":
    #     price="10"
    # elif procedure == "spay":
    #     price = "20"
    # elif procedure =="tumor-removal":
    #     price="50"

    # r1 = get_results('bramer-animal-hospital-evanston')
    # r2 = get_results('fox-animal-hospital-evanston')
    # r3 = get_results('skokie-animal-hospital-skokie')

    # Bramer = {"name":"Bramer Animal Hospital Ltd.", "address":"1021 Davis St, Evanston, IL 60201", "address_url":"1021+Davis+St,+Evanston,+IL+60201", "phone":"(847) 864-1700", "price":price, "yelp":r1}
    # Fox = {"name":"Fox Animal Hospital", "address":"2107 Crawford Ave, Evanston, IL 60201", "address_url":"2107+Crawford+Ave,+Evanston,+IL+60201", "phone":"(847) 869-4900", "price":int(price)*2, "yelp":r2}
    # Skokie = {"name":"Skokie Animal Hospital", "address":"7550 Lincoln Ave, Skokie, IL 60077", "address_url":"7550+Lincoln+Ave,+Skokie,+IL+60077", "phone":"(847) 673-3100", "price":int(int(price)*2.2), "yelp":r3}
    # results = (Bramer, Fox, Skokie)
    return render_template("search.html", results=results, procedure=procedure)

if __name__ == '__main__':
    app.run(host='0.0.0.0')