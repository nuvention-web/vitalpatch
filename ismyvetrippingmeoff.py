from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
import os
import rauth # OAuth for Yelp

app = Flask(__name__)
app.secret_key='iwillneverhavetorecall12032'
app.debug=True
# configure SQLAlchemy
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/vet_prices'

app.config['TRAP_BAD_REQUEST_ERRORS'] = True
app.config['SQLALCHEMY_POOL_RECYCLE'] = 30

# API Keys
# Yelp
yelp_consumer_key = "mxc7iaic-fTArlp9TzlDdQ"
yelp_consumer_secret = "m4K6l7_vZZm8QAOEHTqUXiqEon4"
yelp_token = "lYpeNoecLXLbH7FGD96waKqRQpsBtCOI"
yelp_token_secret = "-vi4CSK58xt4HfxaoA82_BGZ01Q"

db = SQLAlchemy(app)

#Models

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

#Routes

@app.route('/', methods=['GET','POST'])
def index():
	if request.method == "GET":
		return render_template('index.html')
	else:
		
		new_animal_type = request.form['cat_dog']
		new_price = request.form['cost']
		new_weight = request.form['optionsRadios']
		new_procedure = request.form['procedure']
		new_zip = request.form['zip code']
		new_clinic_name = request.form['vet_name']
		new_clinic_yelp_id = None
		newVetData=input_prices(new_animal_type,new_weight,new_procedure,new_price,new_zip,new_clinic_name,new_clinic_yelp_id)
		db.session.add(newVetData)
		db.session.commit()

		return render_template('index.html')
	



if __name__ == '__main__':
	app.run(host='0.0.0.0')

