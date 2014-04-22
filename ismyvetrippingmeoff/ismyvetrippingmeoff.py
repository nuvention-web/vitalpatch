from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
import os
import rauth # OAuth for Yelp

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

	def __init__(self, animal_type, procedure, price, zip, clinic_name, clinic_yelp_id = None, weight = None):
		self.animal_type = animal_type
		self.weight=weight
		self.procedure=procedure
		self.price=price
		self.zip=zip
		self.clinic_name=clinic_name
		self.clinic_yelp_id=clinic_yelp_id
      
db.create_all()

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

# Routes
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
		# Store their price (shhhhh)
		new_animal_type = request.form['cat_dog']
		new_price = request.form['cost']
		new_weight = request.form['optionsRadios']
		new_procedure = request.form['procedure']
		new_zip = request.form['zip code']
		new_clinic_name = request.form['vet_name']
		new_clinic_yelp_id = None
		newVetData=input_prices(new_animal_type,new_procedure,new_price,new_zip,new_clinic_name,new_clinic_yelp_id,new_weight)
		#newVetData=input_prices(new_animal_type,new_weight,new_procedure,new_price,new_zip,new_clinic_name,new_clinic_yelp_id)
		db.session.add(newVetData)
		db.session.commit()

		# Pull price from db
		if new_procedure == 'Neuter' or new_procedure == 'Spay (OHE)':
			if new_animal_type == 'dog':
				if new_weight == '0':
					weightString = "<25 Pound Dog"
				elif new_weight == '1':
					weightString = "25-50 Pound Dog"
				elif new_weight == '2':
					weightString = "51-75 Pound Dog"
				else:
					weightString = ">75 Pound Dog"
				price = vetprocedure.query \
							.filter_by(procedure = new_procedure) \
							.filter_by(animal = new_animal_type.title()) \
							.filter_by(details = weightString) \
							.first()
			else:
				price = vetprocedure.query.filter_by(procedure = new_procedure).filter_by(animal = new_animal_type.title()).first()
		else:
			price = vetprocedure.query.filter_by(procedure = new_procedure).first()

		return render_template('results.html', price=price)
	

if __name__ == '__main__':
	app.run(host='0.0.0.0')

