from vetcompare import *

needCoords = ClinicTEMP.query \
				.filter(ClinicTEMP.latitude == 0) \
				.filter(ClinicTEMP.longitude == 0) \
				.all()

total = len(needCoords)
count = 0

print 'Still have %d clinics to go!' % total

for clinic in needCoords:
	full_address = make_full_address(clinic)
	try:		
		data = Geocoder.geocode(full_address)
		clinic.latitude = data.latitude
		clinic.longitude = data.longitude
		db.session.add(clinic)
		db.session.commit()
		print count
		count += 1
	except GeocoderError:
		print 'We hit a geocoder error :('
		print 'Still have %d clinics to go.' % (total-count)
		print 'Clinic: %s, id: %d' % (clinic.name, clinic.id)
		print 'Address: %s' % full_address
		print '\n'
