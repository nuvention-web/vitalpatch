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
        result = [{"name":"Bramer Animal Hospital Ltd.", "address":"1021 Davis St, Evanston, IL 60201", "address_url":"1021+Davis+St,+Evanston,+IL+60201", "phone":"123-432-3456", "price":price}]
        price = price * 2
        result.append({"name":"Fox Animal Hospital", "address":"2107 Crawford Ave, Evanston, IL 60201", "address_url":"2107+Crawford+Ave,+Evanston,+IL+60201", "phone":"987-678-7654", "price":price})
        price = price * 2.2
        results.append({"name":"Skokie Animal Hospital", "address":"7550 Lincoln Ave, Skokie, IL 60077", "address_url":"7550+Lincoln+Ave,+Skokie,+IL+60077", "phone":"678-543-6789", "price":price})
        print result
        return render_template("index1.html", results=result)
    if request.method=='GET':
        return render_template("index1.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0')
