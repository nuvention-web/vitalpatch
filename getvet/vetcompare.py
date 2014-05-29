from flask import Flask, jsonify, request, render_template, json, flash, session, abort, redirect, url_for
from email.MIMEText import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from flask.ext.admin import Admin, BaseView, AdminIndexView, expose
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import or_, desc
from flask.ext.admin.contrib.sqla import ModelView
from wtforms.fields import SelectField
import os, smtplib, math
import rauth # OAuth for Yelp
from pygeocoder import Geocoder, GeocoderError

from crossdomain import *

app = Flask(__name__) 
app.secret_key="very1secret9secrets90078"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'] 
app.config['TRAP_BAD_REQUEST_ERRORS'] = True
app.config['SQLALCHEMY_POOL_RECYCLE'] = 30
app.config['ADMIN_PASSWORD'] = 'whistle'
app.config['API_KEY'] = 'whistle'
db = SQLAlchemy(app)

# API Keys
# Yelp
yelp_consumer_key = "mxc7iaic-fTArlp9TzlDdQ"
yelp_consumer_secret = "m4K6l7_vZZm8QAOEHTqUXiqEon4"
yelp_token = "lYpeNoecLXLbH7FGD96waKqRQpsBtCOI"
yelp_token_secret = "-vi4CSK58xt4HfxaoA82_BGZ01Q"
# Google Maps
google_maps_key = 'AIzaSyA9a1FhUt8S46UrlxOGIOikYWp8uz5v3Zc'

# Blog Schema
# class Entry(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(max), unique=True)
#     text = db.Column(db.String(max), unique=True)

#     def __init__(self, title, text):
#         self.title = title
#         self.text = text

#     def __repr__(self):
#         return '<Entry %r>' % self.title

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

    def __init__(self, yelp_id = None):
        if yelp_id:
            self.yelp_id = yelp_id
            initializeClinic(self) # Yelp and lat/long

    def __repr__(self):
        return self.name

class ClinicView(ModelView):
    column_list = ('id', 'name', 'phone', 'street_address', 'city', 'state', 'zip', 'yelp_id', 'latitude', 'longitude')
    form_columns = ['yelp_id']

    # Input everything from Yelp, lat/long when user enters data
    def on_model_change(self, form, model, is_created):
        initializeClinic(model) # Yelp and lat/long

class Procedure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    topic = db.Column(db.String(20))
    animal = db.Column(db.String(20))
    price = db.relationship('Price', backref='procedure', lazy='dynamic')

    def __repr__(self):
        return self.name

class ProcedureView(ModelView):
    column_list = ('id', 'topic', 'name', 'animal')
    form_excluded_columns = ('price')

class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinic.id'))
    procedure_id = db.Column(db.Integer, db.ForeignKey('procedure.id'))    
    weight_low_bound = db.Column(db.Float)
    weight_high_bound = db.Column(db.Float)
    price = db.Column(db.Float)
    number_of_prices = db.Column(db.Integer)

    def __init__(self, clinic_id, procedure_id, price, weight_low_bound = None, weight_high_bound = None):
        self.clinic_id = clinic_id
        self.procedure_id = procedure_id

        self.weight_low_bound = weight_low_bound
        self.weight_high_bound = weight_high_bound

        self.price = price
        self.number_of_prices = 1

class PriceView(ModelView):
    column_list = ('id', 'clinic', 'procedure', 'weight_low_bound', 'weight_high_bound', 'price', 'number_of_prices')
    form_columns = ('clinic', 'procedure', 'weight_low_bound', 'weight_high_bound', 'price')

class ZipCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    zip = db.Column(db.String(5))
    city = db.Column(db.String(80))
    state = db.Column(db.String(2))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    timezone = db.Column(db.Integer)
    dst = db.Column(db.Boolean)

###############################################
#       TEMPORARY TABLES FOR MIGRATION        #
###############################################
class ClinicTEMP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    phone = db.Column(db.String(15))
    street_address = db.Column(db.String(80))
    city = db.Column(db.String(80))
    state = db.Column(db.String(80))
    zip = db.Column(db.String(10))
    yelp_id = db.Column(db.String(150))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    price = db.relationship('PriceTEMP', backref='clinic', lazy='dynamic')

    def __init__(self, yelp_id = None):
        if yelp_id:
            self.yelp_id = yelp_id
            initializeClinic(self) # Yelp and lat/long

    def __repr__(self):
        return self.name

class ClinicTEMPView(ModelView):
    column_list = ('id', 'name', 'phone', 'street_address', 'city', 'state', 'zip', 'yelp_id', 'latitude', 'longitude')
    form_columns = ['yelp_id']

    # Input everything from Yelp, lat/long when user enters data
    def on_model_change(self, form, model, is_created):
        initializeClinic(model) # Yelp and lat/long

class ProcedureTEMP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    topic = db.Column(db.String(20))
    animal = db.Column(db.String(20))
    price = db.relationship('PriceTEMP', backref='procedure', lazy='dynamic')

    def __init__(self, name, topic, animal):
        self.name = name
        self.topic = topic
        self.animal = animal

    def __repr__(self):
        return self.name

class ProcedureTEMPView(ModelView):
    column_list = ('id', 'topic', 'name', 'animal')
    form_excluded_columns = ('price')

class PriceTEMP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinicTEMP.id'))
    procedure_id = db.Column(db.Integer, db.ForeignKey('procedureTEMP.id'))    
    weight_low_bound = db.Column(db.Float)
    weight_high_bound = db.Column(db.Float)
    price = db.Column(db.Float)
    national_z_score = db.Column(db.Float)
    urban_z_score = db.Column(db.Float)
    suburban_z_score = db.Column(db.Float)
    rural_z_score = db.Column(db.Float)
    data_integrity = db.Column(db.Integer)

    def __init__(self, clinic_id, procedure_id, price, national_z_score, urban_z_score, suburban_z_score, rural_z_score, data_integrity = None, weight_low_bound = None, weight_high_bound = None):
        self.clinic_id = clinic_id
        self.procedure_id = procedure_id

        self.weight_low_bound = weight_low_bound
        self.weight_high_bound = weight_high_bound

        self.price = price

        self.national_z_score = national_z_score
        self.urban_z_score = urban_z_score
        self.suburban_z_score = suburban_z_score
        self.rural_z_score = rural_z_score
        self.data_integrity = data_integrity

class PriceTEMPView(ModelView):
    column_list = ('id', 'clinic', 'procedure', 'weight_low_bound', 'weight_high_bound', 'price', 'national_z_score', 'urban_z_score', 'suburban_z_score', 'rural_z_score', 'data_integrity')
    form_columns = ('clinic', 'procedure', 'weight_low_bound', 'weight_high_bound', 'price')

class LoginAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        if 'logged_in' in session:
            return super(LoginAdminView, self).index()
        else:
            return redirect(url_for('.login_view'))

    @expose('/login/', methods=['GET', 'POST'])
    def login_view(self):
        if request.method == 'GET':
            if 'logged_in' in session:
                return redirect(url_for('.index'))
            else:
                return render_template('admin_login.html')
        else:
            # Check password
            if request.form['password'] == app.config['ADMIN_PASSWORD']:
                session['logged_in'] = True
                return super(LoginAdminView, self).index()
            else:
                return render_template('admin_login.html', error='Incorrect Password')
                
app.debug = True
db.create_all()
admin = Admin(app, name='VetCompare Admin Console', index_view=LoginAdminView())
admin.add_view(ClinicView(Clinic, db.session, name='Clinic', endpoint='clinics', category='Data'))
admin.add_view(ProcedureView(Procedure, db.session, name='Procedure', endpoint='procedures', category='Data'))
admin.add_view(PriceView(Price, db.session, name='Price', endpoint='prices', category='Data'))

admin.add_view(ClinicTEMPView(ClinicTEMP, db.session, name='ClinicTEMP', endpoint='clinicsTEMP', category='Data'))
admin.add_view(ProcedureTEMPView(ProcedureTEMP, db.session, name='ProcedureTEMP', endpoint='proceduresTEMP', category='Data'))
admin.add_view(PriceTEMPView(PriceTEMP, db.session, name='PriceTEMP', endpoint='pricesTEMP', category='Data'))

# Yelp
def get_yelp_results(businessID):
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

# Get lat/long from an address
def get_lat_long(address):
    try:
        data = Geocoder.geocode(address)
        return (data.latitude, data.longitude)
    except GeocoderError:
        print "Geocoder Error"
        return (0, 0)

# Make full address string with "Street, City, State Zip"
def make_full_address(model):
    return '%s, %s, %s %s' % (model.street_address, model.city, model.state, model.zip)

# Put Yelp and lat/long data in clinic instance when it's created
# Assumes model has a yelp_id already
def initializeClinic(model):
    business = get_yelp_results(model.yelp_id)
    if 'name' in business.keys():
        model.name = business['name']
    if 'phone' in business.keys():
        model.phone = business['phone']
    if 'location' in business.keys():
        if 'address' in business['location'].keys() and len(business['location']['address']):
            model.street_address = business['location']['address'][0]
        if 'city' in business['location'].keys():
            model.city = business['location']['city']
        if 'state_code' in business['location'].keys():
            model.state = business['location']['state_code']
        if 'postal_code' in business['location'].keys():
            model.zip = business['location']['postal_code']
    full_address = make_full_address(model)
    model.latitude, model.longitude = get_lat_long(full_address)

# Find distance between two different longs/lats
def longlat_distance(start, destination):
    lat1, lon1 = start
    lat2, lon2 = destination
    radius = 3959 # miles

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d

# Define sender and recipients for email
sender = "vetcompare@gmail.com"
recipients = ["glennfellman2014@u.northwestern.edu", "fareeha.ali@gmail.com", "ed.bren@gmail.com", "rennaker@gmail.com", "samtoizer@gmail.com", "scott.neaves.eghs@gmail.com"]

# Grab all topics/procedures for select field for given animal
def getProcedures(animal):  
    topicProcedureDict = {}
    queryResults = Procedure.query \
        .distinct(Procedure.name) \
        .order_by(Procedure.name) \
        .filter(or_(Procedure.animal == animal, Procedure.animal == 'All'))   
    for result in queryResults:
        if result.topic in topicProcedureDict:          
            tempList = topicProcedureDict[result.topic]
            tempList.append(result.name)
            topicProcedureDict[result.topic] = tempList
        else:
            topicProcedureDict[result.topic] = [result.name]
    return topicProcedureDict

# Routes
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/geocode/<zip_c>', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def geocode(zip_c=None):
    geocode = db.session.query(ZipCode).filter_by(zip=zip_c).first()
    return jsonify({"latitude": geocode.latitude, "longitude": geocode.longitude})


@app.route('/feedback', methods=['POST'])
def feedback():
    msg = MIMEMultipart('alternative')
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.ehlo()
    session.starttls()
    session.ehlo()
    session.login('vetcompare@gmail.com', os.environ['GMAIL_PASSWORD'])
    msg['From'] = sender
    msg['Subject'] = "VetCompare feedback: " + request.form['subject']
    msg['To'] = "glennfellman2014@u.northwestern.edu;fareeha.ali@gmail.com;ed.bren@gmail.com;rennaker@gmail.com;samtoizer@gmail.com;scott.neaves.eghs@gmail.com"
    body = "From: " + request.form['email'] + "<br><br>" + "What are you thinking: " + request.form['description']
    content = MIMEText(body, 'html')
    msg.attach(content)
    session.sendmail(sender, recipients, msg.as_string())
    return jsonify({"message": "Thanks!"})

@app.route('/quote_request', methods=['GET','POST'])
def quote_request():
    if request.method=="GET":
        return render_template("quote_request.html")
    else: #request.method=="POST"
        msg = MIMEMultipart('related')
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.ehlo()
        session.starttls()
        session.ehlo()
        session.login('vetcompare@gmail.com', os.environ['GMAIL_PASSWORD'])
        msg['From'] = "vetcompare@gmail.com"
        msg['Subject'] = "Someone has filled out the quote request form!"
        msg['To'] = "glennfellman2014@u.northwestern.edu;fareeha.ali@gmail.com;ed.bren@gmail.com;rennaker@gmail.com;samtoizer@gmail.com;scott.neaves.eghs@gmail.com"
        body = "Name: " + request.form['name'] + "<br>" + "Procedure: " + request.form['procedure'] + "<br>" + "Weight: " + request.form['weight'] + "<br>" + "Zip: " + request.form['zip'] + "<br>" + "Breed: " + request.form['breed'] + "<br>" + "Age: " + request.form['age'] + "<br>" + "Sex: " + request.form['sex'] + "<br>" + "Customer's email address: " + request.form['email_addr'] + "<br>" + "Customer's First Name: " + request.form['user_fname'] + "<br>" + "Customer's Last Name: " + request.form['user_lname']
        content = MIMEText(body, 'html')
        msg.attach(content)

        f = request.files['the_file']
        f = MIMEImage(f.read())
        msg.attach(f)

        session.sendmail("vetcompare@gmail.com", recipients, msg.as_string())


        flash("Thanks! Your quote request has been successfully submitted.")
        return render_template("quote_request.html")


@app.route('/search', methods = ['GET'])
def search():
    procedure = request.args['procedure'].lower()
    weight = request.args['weight']
    zip = request.args['zip']
    results = []
    procedureObj = Procedure.query.filter(Procedure.name == procedure.lower()).first()
    if procedureObj:
        if weight:
            businesses = Price.query.filter(Price.procedure_id == procedureObj.id) \
                                    .filter(or_(Price.weight_low_bound == None, Price.weight_low_bound <= weight)) \
                                    .filter(or_(Price.weight_high_bound == None, Price.weight_high_bound > weight)) \
                                    .order_by(Price.price) \
                                    .all()  #TODO: order by distance after price
        else:
            businesses = Price.query.filter(Price.procedure_id == procedureObj.id) \
                                    .order_by(Price.price) \
                                    .all()

        zipLatLong = get_lat_long(zip)

        for business in businesses:
            yelp_result = get_yelp_results(business.clinic.yelp_id)
            full_address = make_full_address(business.clinic)
            results.append({
                'name': business.clinic.name,
                'phone': '(%s) %s-%s' % (business.clinic.phone[0:3], business.clinic.phone[3:6], business.clinic.phone[6:]),
                'address': full_address,
                'address_url': "http://google.com/maps/search/" + full_address.replace(' ', '+'),
                'distance': longlat_distance(zipLatLong, (business.clinic.latitude, business.clinic.longitude)),
                'price': '%.2f' % business.price,
                'yelp_rating_url': yelp_result['rating_img_url'],
                'yelp_url': yelp_result['url']
            })
    return render_template("search.html", results=results, procedure=str(procedure).title(), weight=weight, zip=zip)

# What will replace the search function after data migration
def search2():
    animal = request.args['animal']
    procedure = request.args['procedure']
    weight = request.args['weight']
    zip = request.args['zip']
    results = []
    procedureObj = Procedure.query \
                    .filter(Procedure.name == procedure) \
                    .filter(or_(Procedure.animal == animal, Procedure.animal == 'All')) \
                    .first()
    if procedureObj:
        if weight:
            businesses = Price.query.filter(Price.procedure_id == procedureObj.id) \
                                    .filter(or_(Price.weight_low_bound == None, Price.weight_low_bound <= weight)) \
                                    .filter(or_(Price.weight_high_bound == None, Price.weight_high_bound > weight)) \
                                    .order_by(Price.price) \
                                    .all()  #TODO: order by distance after price
        else:
            businesses = Price.query.filter(Price.procedure_id == procedureObj.id) \
                                    .order_by(Price.price) \
                                    .all()

        zipLatLong = get_lat_long(zip)

        for business in businesses:
            distance = longlat_distance(zipLatLong, (business.clinic.latitude, business.clinic.longitude))            

            # Only show businesses within 50 miles
            if distance < 50:
                yelp_result = get_yelp_results(business.clinic.yelp_id)
                full_address = make_full_address(business.clinic)
                results.append({
                    'name': business.clinic.name,
                    'phone': '(%s) %s-%s' % (business.clinic.phone[0:3], business.clinic.phone[3:6], business.clinic.phone[6:]),
                    'address': full_address,
                    'address_url': "http://google.com/maps/search/" + full_address.replace(' ', '+'),
                    'distance': '%.2f' % distance,
                    'price': '%.2f' % business.price,
                    'yelp_rating_url': yelp_result['rating_img_url'],
                    'yelp_url': yelp_result['url']
                })

    topicProcedureDict = getProcedures(animal.title())

    return render_template("search.html", results=results, animal=str(animal), topicProcedureDict=topicProcedureDict, curr_procedure=str(procedure), weight=weight, zip=zip)

# Get new procedures given animal selection
@app.route('/_update-procedures', methods=['POST'])
def updateProcedures():
    return jsonify(getProcedures(request.form['animal'].title()))

# Receive data from IMVRMO to be added to db
@app.route('/add_data', methods=['POST'])
def add_data():
    if request.form['api_key'] != app.config['API_KEY']:
        message = 'Error: invalid API key.'
    else:
        message = ""

        ## Clinic ##
        clinic = ClinicTEMP.query.filter(ClinicTEMP.yelp_id == request.form['yelp_id']).first()
        if not clinic:
            clinic = ClinicTEMP(request.form['yelp_id'])
            db.session.add(clinic)
            db.session.commit()
            message += "\nAdded new clinic"

        ## Procedure ##
        procedure = ProcedureTEMP.query \
                        .filter(ProcedureTEMP.name == request.form['procedure']) \
                        .filter(ProcedureTEMP.topic == request.form['topic']) \
                        .filter(or_(ProcedureTEMP.animal == request.form['animal'].title(), ProcedureTEMP.animal == 'All')) \
                        .first()
        if not procedure:
            procedure = ProcedureTEMP(
                request.form['procedure'],
                request.form['topic'],
                request.form['animal'].title()
            )
            db.session.add(procedure)
            db.session.commit()
            message += "\nAdded new procedure"

        ## Price ##            
        priceInstance = PriceTEMP(
            clinic.id,
            procedure.id,
            request.form['price'],
            request.form['national_z_score'],
            request.form['urban_z_score'],
            request.form['suburban_z_score'],
            request.form['rural_z_score']
        )

        # If price needs weight, data integrity
        if str(request.form['weight_low_bound']) != 'None':
            priceInstance.weight_low_bound = request.form['weight_low_bound']
        if str(request.form['weight_high_bound']) != 'None':
            priceInstance.weight_high_bound = request.form['weight_high_bound']
        if str(request.form['data_integrity']) != 'None':
            priceInstance.data_integrity = request.form['data_integrity']

        message += "\nAdded new price"
        
        # Add price to db
        db.session.add(priceInstance)
        db.session.commit()

        message = "Success!" + message

    return message

#################################################
##                 Blog Routes                 ##
#################################################
@app.route('/blog')
def show_entries():
    query = Entry.query.order_by(desc(Entry.id))
    print query
    entries = [dict(title=row.title, text=row.text) for row in query.all()]
    return render_template('show_entries.html', entries=entries)


@app.route('/blog_add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    entry = Entry(request.form['title'], request.form['text'])
    db.session.add(entry)
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/blog_login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != os.environ['BLOG_USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != os.environ['BLOG_PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/blog_logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0')
