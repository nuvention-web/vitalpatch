from flask import Flask, render_template, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
import os
import rauth # OAuth for Yelp
from pygeocoder import Geocoder
from math import erf, sqrt
import json

app = Flask(__name__)

app.secret_key = 'iwillneverhavetorecall12032'
app.debug = True
# configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['TRAP_BAD_REQUEST_ERRORS'] = True
app.config['SQLALCHEMY_POOL_RECYCLE'] = 30

# API Keys
# Yelp
yelp_consumer_key = "mxc7iaic-fTArlp9TzlDdQ"
yelp_consumer_secret = "m4K6l7_vZZm8QAOEHTqUXiqEon4"
yelp_token = "lYpeNoecLXLbH7FGD96waKqRQpsBtCOI"
yelp_token_secret = "-vi4CSK58xt4HfxaoA82_BGZ01Q"

db = SQLAlchemy(app)

# Models
class vetprocedure(db.Model):
	index = db.Column(db.Integer, primary_key=True)
	topic = db.Column(db.String(20))
	animal = db.Column(db.String(3))
	table_number = db.Column(db.Float)
	procedure = db.Column(db.Text)
	details = db.Column(db.Text)
	urban_25th_percentile = db.Column(db.Float)
	urban_median = db.Column(db.Float)
	urban_75th_percentile = db.Column(db.Float)
	suburban_25th_percentile = db.Column(db.Float)
	suburban_median = db.Column(db.Float)
	suburban_75th_percentile = db.Column(db.Float)
	rural_25th_percentile = db.Column(db.Float)
	rural_median = db.Column(db.Float)
	rural_75th_percentile = db.Column(db.Float)

class input_prices(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	animal_type = db.Column(db.String(3))
	weight = db.Column(db.Integer)
	procedure = db.Column(db.String(80))
	price = db.Column(db.Float)
	zip = db.Column(db.Integer)
	clinic_name = db.Column(db.String(80))
	clinic_yelp_id = db.Column(db.String(150))
	data_integrity = db.Column(db.Integer)

	def __init__(self, animal_type, procedure, price, zip, clinic_name, clinic_yelp_id = None, weight = None, data_integrity = None):
		self.animal_type = animal_type
		self.weight = weight
		self.procedure = procedure
		self.price = price
		self.zip = zip
		self.clinic_name = clinic_name
		self.clinic_yelp_id = clinic_yelp_id
		self.data_integrity = data_integrity

class waitlist(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email_address = db.Column(db.String(100))

	def __init__(self, email_address):
		self.email_address=email_address

	def __repr__(self):
		return '<Email Address: %r>' % self.email_address

db.create_all()

# Remember the data between interstitial and results page
newVetData = None

# Yelp
def get_yelp_results(businessID):
    # Session setup
    session = rauth.OAuth1Session(
        consumer_key = yelp_consumer_key, 
        consumer_secret = yelp_consumer_secret, 
        access_token = yelp_token, 
        access_token_secret = yelp_token_secret)

    request = session.get('http://api.yelp.com/v2/search/' + businessID)

    # Transform JSON API response into Python dictionary
    data = request.json()
    session.close()

    return data


# Calculate cumulative distribution function
def cdf(x):
	return (1.0 + erf(x / sqrt(2.0))) / 2.0

# User-Facing Routes
@app.route('/', methods=['GET','POST'])
def index():	
	if request.method == "GET":
		# Grab all topics/procedures for select field
		topicProcedureDict = {}
		queryResults = vetprocedure.query.distinct(vetprocedure.procedure).order_by(vetprocedure.procedure)
		for result in queryResults:
			if result.topic in topicProcedureDict:			
				tempList = topicProcedureDict[result.topic]
				tempList.append(result.procedure)
				topicProcedureDict[result.topic] = tempList
			else:
				topicProcedureDict[result.topic] = [result.procedure]

		return render_template('index.html', topicProcedureDict=topicProcedureDict)
	else:		
		# Delete their previous price, add the data integrity, re-store it
		db.session.delete(newVetData)
		newVetData.data_integrity = request.form['integrity']
		db.session.add(newVetData)
		db.session.commit()

		# Pull price from db
		if newVetData.procedure == 'Neuter' or newVetData.procedure == 'Spay (OHE)':
			if newVetData.animal_type == 'dog':
				if newVetData.weight == '0':
					weightString = "<25 Pound Dog"
				elif newVetData.weight == '1':
					weightString = "25-50 Pound Dog"
				elif newVetData.weight == '2':
					weightString = "51-75 Pound Dog"
				else:
					weightString = ">75 Pound Dog"
				price = vetprocedure.query \
							.filter_by(procedure = newVetData.procedure) \
							.filter_by(animal = newVetData.animal_type.title()) \
							.filter_by(details = weightString) \
							.first()
			else:
				price = vetprocedure.query.filter_by(procedure = newVetData.procedure).filter_by(animal = newVetData.animal_type.title()).first()
		else:
			price = vetprocedure.query.filter_by(procedure = newVetData.procedure).first()

		# Calculate percentile
		if float(newVetData.price) < price.suburban_median:
			std = (price.suburban_median - price.suburban_25th_percentile) / 0.67449
		else:
			std = (price.suburban_75th_percentile - price.suburban_median) / 0.67449
		
		z_score = (float(newVetData.price) - price.suburban_median) / std
		percentile = cdf(z_score)*100

		percentileData = {
			'25thPercentile': price.suburban_25th_percentile,
			'median'        : price.suburban_median,
			'75thPercentile': price.suburban_75th_percentile,
			'userPercentile': int(percentile),
			'procedure'     : newVetData.procedure
		}

		return render_template('results.html', procedure = newVetData.procedure, price = newVetData.price, percentile = percentile, percentileData = json.dumps(percentileData))

@app.route('/interstitial', methods=['POST'])
def interstitial():	
	# Store their price (shhhhh)
	global newVetData

	new_animal_type = request.form['cat_dog']
	new_price = request.form['cost']
	new_weight = request.form.get('weight')
	new_procedure = request.form['procedure']
	new_zip = request.form['zip code']
	new_clinic_name = request.form['vet_name']
	new_clinic_yelp_id = request.form['vet_id']
	newVetData = input_prices(
		new_animal_type,
		new_procedure,
		new_price,
		new_zip,
		new_clinic_name,
		new_clinic_yelp_id,
		new_weight
	)
	db.session.add(newVetData)
	db.session.commit()
	return render_template('interstitial.html')

# Routes for AJAX
@app.route('/_get_clinics_in_zipcode', methods=['GET'])
def get_clinics_in_zipcode():
	zipcode = request.args.get('zipcode', 0, type=int)
	latlng = Geocoder.geocode(zipcode)

	# Session setup
	session = rauth.OAuth1Session(
		consumer_key=yelp_consumer_key,
		consumer_secret=yelp_consumer_secret,
		access_token=yelp_token,
		access_token_secret=yelp_token_secret)

	params = {}
	params["term"] = "veterinarian"
	params["radius_filter"] = "16093" #10 miles
	params["ll"] = str(latlng.latitude) + ',' + str(latlng.longitude)
	params["limit"] = "20"
	params["category_filter"] = "vet"
	#print str(latlng.latitude) + ',' + str(latlng.longitude)
	params["sort"] = "1"

	data = session.get('http://api.yelp.com/v2/search/', params=params) #returns response object, which we now name "data"
	clinics_in_radius = data.json() #extracts json content from response object
	clinics_in_radius = jsonify(data.json())	#package up json content 
	session.close()
	return clinics_in_radius

@app.route('/_submit_email')
def submit_email():
	email_address = request.args.get('email', 0, type=str)
	new_customer = waitlist(email_address)
	db.session.add(new_customer)
	db.session.commit()
	return jsonify(email_address=email_address)


if __name__ == '__main__':
	app.run(host='0.0.0.0')

