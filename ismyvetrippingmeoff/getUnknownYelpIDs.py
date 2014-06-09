from ismyvetrippingmeoff import *

# Setup csv files
with open('unknownYelpIDs.csv', 'wb') as csvfile:
	writer = csv.writer(csvfile)
	writer.writerow(['id', 
					'clinic_name', 
					'clinic_zip',
					'procedure_topic', 
					'procedure_name', 
					'animal', 
					'price', 
					'weight_low_bound',
					'weight_high_bound',
					'national_z_score',
					'urban_z_score',
					'suburban_z_score',
					'rural_z_score',
					'data_integrity'
					])

# Procedures we need a weight value for
needWeightProcedures = ['Neuter (male)', 'Spay (female)', 'Hernia', 'Gastrotomy: Foreign-body removal']

# Grab all entries
allPrices = input_prices.query.all()
for entry in allPrices:

	# Only grab entries that don't have yelp id
	if str(entry.clinic_yelp_id) == 'Null' or str(entry.clinic_yelp_id) == '':
		# Make sure the entry even has a procedure
		if entry.procedure:
			# If we need the weight for the procedure and the animal is a dog
			weight_low_bound = None
			weight_high_bound = None
			if entry.procedure in needWeightProcedures and entry.animal_type == 'dog':
				if entry.weight == 0:
					weightString = "<25 Pound Dog"
					weight_high_bound = 25
				elif entry.weight == 1:
					weightString = "25-50 Pound Dog"
					weight_low_bound = 25
					weight_high_bound = 50
				elif entry.weight == 2:
					weightString = "51-75 Pound Dog"
					weight_low_bound = 51
					weight_high_bound = 75
				else:
					weightString = ">75 Pound Dog"
					weight_low_bound = 76
				price = vetprocedure.query \
							.filter_by(procedure = entry.procedure) \
							.filter_by(animal = entry.animal_type.title()) \
							.filter_by(details = weightString) \
							.first()		
			else:
				price = vetprocedure.query \
							.filter_by(procedure = entry.procedure) \
							.filter(or_(vetprocedure.animal == entry.animal_type.title(), vetprocedure.animal == 'All')) \
							.first()

			if not price:
				continue
			## Calculate percentiles ##
			# National
			if float(entry.price) < price.national_median:
				std = (price.national_median - price.national_25th_percentile) / 0.67449
			else:
				std = (price.national_75th_percentile - price.national_median) / 0.67449
			
			national_z_score = (float(entry.price) - price.national_median) / std
			national_percentile = cdf(national_z_score)*100

			# Urban
			if float(entry.price) < price.urban_median:
				std = (price.urban_median - price.urban_25th_percentile) / 0.67449
			else:
				std = (price.urban_75th_percentile - price.urban_median) / 0.67449
			
			urban_z_score = (float(entry.price) - price.urban_median) / std
			urban_percentile = cdf(urban_z_score)*100

			# Suburban
			if float(entry.price) < price.suburban_median:
				std = (price.suburban_median - price.suburban_25th_percentile) / 0.67449
			else:
				std = (price.suburban_75th_percentile - price.suburban_median) / 0.67449
			
			suburban_z_score = (float(entry.price) - price.suburban_median) / std
			suburban_percentile = cdf(suburban_z_score)*100		

			# Rural
			if float(entry.price) < price.rural_median:
				std = (price.rural_median - price.rural_25th_percentile) / 0.67449
			else:
				std = (price.rural_75th_percentile - price.rural_median) / 0.67449
			
			rural_z_score = (float(entry.price) - price.rural_median) / std
			rural_percentile = cdf(rural_z_score)*100

			# Create CSV file			
			with open('unknownYelpIDs.csv', 'ab') as csvfile:
				writer = csv.writer(csvfile)
				writer.writerow([entry.id,
								entry.clinic_name,
								entry.zip,
								price.topic,
								entry.procedure,
								entry.animal_type,
								entry.price,
								weight_low_bound,
								weight_high_bound,
								national_z_score,
								urban_z_score,
								suburban_z_score,
								rural_z_score,
								entry.data_integrity
								])

# Setup
subject = 'Sending you the unknown yelp id file'
sender = ('IMVRMO', app.config['MAIL_USERNAME'] + '@gmail.com')
recipients = ['samtoizer@gmail.com']
# Email
msg = Message(subject, sender = sender, recipients = recipients)
msg.body = 'Here ya go!'
msg.html = 'Here ya go!'
# Attach
with app.open_resource('unknownYelpIDs.csv') as fp:
    msg.attach('unknownYelpIDs.csv', 'text/csv', fp.read())
# Send
mail.send(msg)