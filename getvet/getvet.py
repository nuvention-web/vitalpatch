from flask import Flask, jsonify, request, render_template, json
from flask.ext.admin import Admin, BaseView, expose

class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html')


app = Flask(__name__)
app.debug = True
admin = Admin(app, name='GetVet Admin Console')
admin.add_view(MyView(name='Hello'))


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
        result = {"name":"The Best Vet", "address":"14 libertyville Rd, Evanston, Illinois", "address_url":"14+libertyville+Rd,+Paris,+France", "phone":"123-432-3456", "price":price}
        #price = price * 2
        #results += json.dumps(name="The Vet You Can Bet On", address="7 Fortuitous Circle, Evanston, Illinois", address_url="7+Fortuitous+Circle,+Evanston,+Illinois", phone="987-678-7654", price=price)
        #price = price * 2.2
        #results += json.dumps(name="Tim's Animal Hospital", address="12 Sherman Avenue, Evanston, Illinois", address_url="12+Sherman+Avenue,+Evanston,+Illinois", phone="678-543-6789", price=price)
        print result
        return render_template("index.html", results=result)
    if request.method=='GET':
        return render_template("index.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0')
