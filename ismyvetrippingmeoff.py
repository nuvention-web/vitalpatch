from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key='iwillneverhavetorecall12032'
# configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['TRAP_BAD_REQUEST_ERRORS'] = True
app.config['SQLALCHEMY_POOL_RECYCLE'] = 30

db = SQLAlchemy(app)

# models
class input_prices(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	animal_type = db.Column(db.String(3))
	weight = db.Column(db.Integer)
	procedure = db.Column(db.String(80))
	price = db.Column(db.Float)
	zip = db.Column(db.Integer)
	clinic_name = db.Column(db.String(80))
	clinic_yelp_id = db.Column(db.String(150))

	def __init__(self, animal_type, procedure, price, zip, clinic_name, clinic_yelp_id, weight = None):
		self.animal_type = animal_type
		self.weight=weight
		self.procedure=procedure
		self.price=price
		self.zip=zip
		self.clinic_name=clinic_name
		self.clinic_yelp_id=clinic_yelp_id

        
	
db.create_all()

#Routes

@app.route('/', methods=['GET','POST'])
def index():
	if request.method == "GET":
		return render_template('index.html')
	else:
		new_animal_type = request.form('cat_dog')
		print request.url
		print new_animal_type
		#newVetData=input_prices(animal_type,weight,procedure,price,zip,clinic_name,clinic_yelp_id)
		#db.session.add(newVetData)
		#db.session.commit()



if __name__ == '__main__':
	app.run(host='0.0.0.0')

