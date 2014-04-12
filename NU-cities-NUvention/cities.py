import flask, string, random, smtplib, os
from email.mime.text import MIMEText
from flask.ext.sqlalchemy import SQLAlchemy 
from sqlalchemy import desc, update
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, redirect, url_for, make_response, render_template, session, Markup

application = flask.Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'] #'mysql://root:8hub9jin@localhost:3306/nucities'
application.config['TRAP_BAD_REQUEST_ERRORS'] = True
application.config['SQLALCHEMY_POOL_RECYCLE'] = 30
db = SQLAlchemy(application)

##Models

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    country = db.Column(db.String(120))
    state = db.Column(db.String(120))
    city = db.Column(db.String(120))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    pw_hash = db.Column(db.String(120))
    validation_code = db.Column(db.String(10))
    activated_bool = db.Column(db.String(1))

    def __init__(self, fname, lname, email, password, validation_code, activated_bool ):
        self.first_name = fname
        self.last_name = lname
        self.email = email
        self.set_password(password)
        self.validation_code = validation_code
        self.activated_bool = activated_bool

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def __repr__(self):
        return '<User %r>' % self.email


application.debug=True
application.secret_key=os.urandom(24)


@application.route('/home')
def home():
    if 'email' in session:
        current_user = db.session.query(User).filter_by(email=session['email']).first()
        users = db.session.query(User).filter_by(activated_bool='1').order_by("country", "state", "city", "first_name")
        return render_template('home.html', users=users, current_user=current_user)
    else: 
        return render_template('login.html')

@application.route('/')
def redirect_to_login():
    return redirect(url_for('login'))

@application.route('/login', methods=['POST', 'GET'])
def login():
    status = None
    if request.method == 'GET':
        users = db.session.query(User).filter_by(activated_bool='1')
        return render_template('login.html', users=users)
    if request.method == 'POST':
        user_in_database = True if (db.session.query(User).filter_by(email=request.form['email']).first() != None) else False
        if((not user_in_database) or (not db.session.query(User).filter_by(email=request.form['email']).first().check_password(request.form['password']))):
            status="Either you haven't already registered, or your username/password combination is incorrect."
            return render_template('login.html', status=status)
        else: #the user exists in the database and the password matches
            session['email'] = request.form['email']
            return redirect(url_for('home'))


@application.route('/register', methods=['POST', 'GET'])
def register():
    status = None
    if request.method == 'POST':
        rand_str = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
        new_user = User(request.form['fname'], request.form['lname'], request.form['email'], request.form['password'], rand_str, '0')
        
        if('2014@u.northwestern.edu' not in request.form['email']):
        #if(False):
            status = "Sorry, that didn't work! Please use your \"firstNamelastName2014@u.northwestern.edu\" email address (the same one that you got on the first day of school). Thanks :)"
            return render_template('register.html', status=status)
        #If not empty:
        if (db.session.query(User).filter_by(email=request.form['email']).first()!=None):
            #Mark as invalid
            status = "Sorry, that didn't work! A user with that email address has already been verified."
            return render_template('register.html', status=status)
        else:   #User is using his/her corect email address, and there isn't already a user in the system with that email address  
            db.session.add(new_user)
            db.session.commit()

            url_to_send = 'http://whereintheworldiswillie.herokuapp.com/validate/' + rand_str     ##replace this url 
            session = smtplib.SMTP('smtp.gmail.com', 587)
            session.ehlo()
            session.starttls()
            session.ehlo()
            session.login('whereintheworldiswillie@gmail.com', 'tor3nc45')
            headers = ["from: whereintheworldiswillie@gmail.com",
                        "subject: Please validate your account with whereintheworldiswillie",
                        "to: " + request.form['email'],
                        "mime-version: 1.0",
                        "content-type: text/html"]
            headers = "\r\n".join(headers)
            body = "Hello! <br> Please click the following link to activate your account with whereintheworldiswillie: "  + url_to_send + ". <br><br> Thanks! <br> Best, <br> whereintheworldiswillie"
            session.sendmail("whereintheworldiswillie@gmail.com", request.form['email'], headers + "\r\n\r\n" + body)

            status = "Success! Please check your email, and click the link in the message we sent you to validate your account. "
            return render_template('register.html', status=status)
    else:  #(if request.method == 'GET')
        status = "Please register here to add your information :)"
        return render_template('register.html', status=status)
 

@application.route('/validate/<secret_code>')
def validate(secret_code = None):
    status = None
    if(secret_code!=None):
        searched_user = db.session.query(User).filter_by(validation_code=secret_code).first()
        if(searched_user!= None):
            searched_user.activated_bool = '1'
            db.session.commit()
            session['email'] = searched_user.email
            return redirect(url_for('update_info'))
        else:
            status = "No user found with that validation code"
            return url_for(page_not_found, status=status)
    else: 
        status = "No secret code in URL"
        return url_for(page_not_found, status=status)

@application.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('email', None)
    return redirect(url_for('login'))


@application.route('/forgot_password', methods=['POST', 'GET'])
def forgot_password():
    status = None;
    if request.method == 'GET':
        status = "Please enter your email address here, and we will send you an email containing a link which you can click to reset your password."
        return render_template('forgot_password.html', status=status)
    else: #request.method == 'POST':
        user = db.session.query(User).filter_by(email=request.form['email']).first()
        if user == None:
            status = Markup("That email address has not been registered! Please <a href=\"/register\"> register. </a> ")
            return render_template('forgot_password.html', status=status)
        if user != None:
            #Send email containing link to /reset_password/<validation_code>, which will display a form with a password field, 
            #   which will reset the user's password upon submit.
            session = smtplib.SMTP('smtp.gmail.com', 587)
            session.ehlo()
            session.starttls()
            session.ehlo()
            session.login('whereintheworldiswillie@gmail.com', 'tor3nc45')
            headers = ["from: whereintheworldiswillie@gmail.com",
                        "subject: Password reset for whereintheworldiswillie",
                        "to: " + request.form['email'],
                        "mime-version: 1.0",
                        "content-type: text/html"]
            headers = "\r\n".join(headers)
            body = "Hello! <br> Please click this link to reset your password: http://whereintheworldiswillie.herokuapp.com/reset_password/" + db.session.query(User).filter_by(email=request.form['email']).first().validation_code + "<br><br> Thanks, <br> whereintheworldiswillie"
            session.sendmail("whereintheworldiswillie@gmail.com", request.form['email'], headers + "\r\n\r\n" + body)

            return redirect(url_for('login'))


@application.route('/reset_password/<secret_code>', methods=['POST', 'GET'])
def reset_password(secret_code=None):
    status = None;
    if request.method == 'GET':
        status = "Please enter your email address and a new password."
        return render_template('reset_password.html', status = status)
    else: # request.method=='POST':
        if db.session.query(User).filter_by(email=request.form['email']).first().validation_code == secret_code:
            db.session.query(User).filter_by(email=request.form['email']).first().set_password(request.form['password'])
            db.session.commit()
            status=Markup("Your password has been reset. <a href=\"/login\"> Login </a>")
            return render_template('reset_password.html', status=status)
        else:
            return redirect(url_for('login'))


@application.route('/update_info', methods=['POST', 'GET'])
def update_info():
    status = None
    if 'email' in session:
        current_user = db.session.query(User).filter_by(email=session['email']).first()
        if 'email' in session:
            if request.method == 'POST':
                current_user = db.session.query(User).filter_by(email=session['email']).first();
                current_user.first_name=request.form['fname']
                current_user.last_name=request.form['lname']
                current_user.country=request.form['country']
                current_user.state=request.form['state']
                current_user.city=request.form['city']
                current_user.latitude=request.form['lat']
                current_user.longitude=request.form['lng']
                db.session.commit()
                status = Markup("Success! Your information has been successfully updated. <a href=\"/home\"> Home. </a>")
                return render_template('update_info.html', status=status, current_user=current_user)
            else:  #(if request.method == 'GET')
                status = "Tell us where you will be living next year!"
                #countries = ["United States of America, Afghanistan, Albania, Algeria, Andorra, Angola, Antigua & Deps, Argentina, Armenia, Australia, Austria, Azerbaijan, Bahamas, Bahrain, Bangladesh, Barbados, Belarus, Belgium, Belize, Benin, Bhutan, Bolivia, Bosnia Herzegovina, Botswana, Brazil, Brunei, Bulgaria, Burkina, Burma, Burundi, Cambodia, Cameroon, Canada, Cape Verde, Central African Rep, Chad, Chile, People's Republic of China, Republic of China, Colombia, Comoros, Democratic Republic of the Congo, Republic of the Congo, Costa Rica,, Croatia, Cuba, Cyprus, Czech Republic, Danzig, Denmark, Djibouti, Dominica, Dominican Republic, East Timor, Ecuador, Egypt, El Salvador, Equatorial Guinea, Eritrea, Estonia, Ethiopia, Fiji, Finland, France, Gabon, Gaza Strip, The Gambia, Georgia, Germany, Ghana, Greece, Grenada, Guatemala, Guinea, Guinea-Bissau, Guyana, Haiti, Holy Roman Empire, Honduras, Hungary, Iceland, India, Indonesia, Iran, Iraq, Republic of Ireland, Israel, Italy, Ivory Coast, Jamaica, Japan, Jonathanland, Jordan, Kazakhstan, Kenya, Kiribati, North Korea, South Korea, Kosovo, Kuwait, Kyrgyzstan, Laos, Latvia, Lebanon, Lesotho, Liberia, Libya, Liechtenstein, Lithuania, Luxembourg, Macedonia, Madagascar, Malawi, Malaysia, Maldives, Mali, Malta, Marshall Islands, Mauritania, Mauritius, Mexico, Micronesia, Moldova, Monaco, Mongolia, Montenegro, Morocco, Mount Athos, Mozambique, Namibia, Nauru, Nepal, Newfoundland, Netherlands, New Zealand, Nicaragua, Niger, Nigeria, Norway, Oman, Ottoman Empire, Pakistan, Palau, Panama, Papua New Guinea, Paraguay, Peru, Philippines, Poland, Portugal, Prussia, Qatar, Romania, Rome, Russian Federation, Rwanda, St Kitts & Nevis, St Lucia, Saint Vincent & the Grenadines, Samoa, San Marino, Sao Tome & Principe, Saudi Arabia, Senegal, Serbia, Seychelles, Sierra Leone, Singapore, Slovakia, Slovenia, Solomon Islands, Somalia, South Africa, Spain, Sri Lanka, Sudan, Suriname, Swaziland, Sweden, Switzerland, Syria, Tajikistan, Tanzania, Thailand, Togo, Tonga, Trinidad & Tobago, Tunisia, Turkey, Turkmenistan, Tuvalu, Uganda, Ukraine, United Arab Emirates, United Kingdom, Uruguay, Uzbekistan, Vanuatu, Vatican City, Venezuela, Vietnam, Yemen, Zambia, Zimbabwe"]
                #states = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']
                return render_template('update_info.html', status=status, current_user=current_user)
        else:   #User is not logged in.
            return render_template('login.html')
    else:   #If user is not logged in:
        return redirect(url_for('login'))


@application.route('/delete_account', methods=['POST', 'GET'])
def delete_account():
    status = None
    if 'email' not in session:
        return redirect(url_for('login'))
    else: #User is logged in
        if request.method == 'GET':
            status = "Please enter your Northwestern email address to delete your account (the same address that you used to sign up on this site)."
            return render_template('delete_account.html', status=status)
        else: #request.method == 'POST'
            if session['email'] == request.form['email']:
                user = db.session.query(User).filter_by(email=session['email']).first()
                db.session.delete(user)
                db.session.commit()
                status = "Success! Your account has been deleted."
                return render_template('delete_account.html', status=status)
            else: #logged-in user does not match email address in form.
                status = Markup("Sorry, that didn't work. The email address that you entered does not correspond to the user that you are logged in as. Please <a href=\"/login\">Login.</a>")
                return render_template('delete_account.html', status=status)

@application.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


if __name__ == '__main__':
    application.run(host='0.0.0.0')
         





