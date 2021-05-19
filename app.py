from flask import Flask
from flask import request
from flask import render_template
from flask import abort, redirect, url_for, make_response,flash
from pypyodbc import BinaryNull
from AzureDB import AzureDB

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ahsuiaysi7yahdisadisadsidus'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/gallery')
def gallery():
    return render_template ('gallery.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['POST','GET'])
def contact():
    if request.method == "POST":
        if len(request.form['name']) > 2 and len(request.form['mail']) > 3 and len(request.form['text']) > 5:
            res = AzureDB().azureAddData(request.form['name'],request.form['mail'],request.form['text'])
            flash('Comentarz został wysłąny', category='success')
        
        else:
            flash('Niepoprawna forma komentarza, sprawdz', category='error')
    
    return render_template('contact.html')

@app.route("/comments")
def comments():
    data = AzureDB().azureGetData()
    return render_template("comments.html", data = data)

@app.route('/comments/<int:id>/delete')
def delete_comm(id):
    AzureDB().azureDeleteData(id)
    return redirect('/comments')

@app.route("/comments/<int:id>/edit", methods=['POST', 'GET'])
def edit_comm(id):
    comm = AzureDB().azureGetDataid(id)
    if request.method == "POST":
        if len(request.form['text']) > 5:
            res = AzureDB().azureEditData(request.form['text'], id)
            return redirect('/comments')
        
        else:
            return 'Nie możesz zostawić pusty komentarz!'
    else:
        
        return render_template('edit.html', comm = comm)

@app.route('/error_denied')
def error_denied():
    abort(401)

@app.route('/error_internal')
def error_internal():
    abort(505)

@app.route('/error_not_found')
def error_not_found():
    abort(404)

if __name__ == '__main__':
 app.run(debug=True)