from flask import Flask, jsonify, request, render_template, json
from flask.ext.admin import Admin, BaseView, expose
from flask.ext.sqlalchemy import SQLAlchemy 

class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html')

app = Flask(__name__)
app.debug = True
db = SQLAlchemy(app)
admin = Admin(app, name='GetVet Admin Console')
admin.add_view(MyView(name='Hello'))


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

@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method=='POST':
        procedure = request.form['procedure']
        price = "0"
        if procedure == "neuter":
            price="10"
        elif procedure == "spay":
            price = "20"
        elif procedure =="tumor-removal":
            price="50"
        result = [{"name":"Bramer Animal Hospital Ltd.", "address":"1021 Davis St, Evanston, IL 60201", "address_url":"1021+Davis+St,+Evanston,+IL+60201", "phone":"123-432-3456", "price":price}]
        price = str(int(price) * 2)
        result.append({"name":"Fox Animal Hospital", "address":"2107 Crawford Ave, Evanston, IL 60201", "address_url":"2107+Crawford+Ave,+Evanston,+IL+60201", "phone":"987-678-7654", "price":price})
        price = str(int(price) * 2.2)
        results.append({"name":"Skokie Animal Hospital", "address":"7550 Lincoln Ave, Skokie, IL 60077", "address_url":"7550+Lincoln+Ave,+Skokie,+IL+60077", "phone":"678-543-6789", "price":price})
        print result
        return render_template("index.html", results=result, query=request.form['procedure'])
    if request.method=='GET':
        return render_template("index.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0')
