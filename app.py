from flask import Flask
from flask import request
from flask import render_template
from flask import abort, redirect, url_for,flash
from AzureDB import AzureDB
from flask_dance.contrib.github import make_github_blueprint, github
import secrets
import os

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

github_blueprint = make_github_blueprint(
    client_id="d9e6f6a89261c7c192ce",
    client_secret="28f561faf123a5ec62b71bd5fd4a14611008ea4f"

)
app.register_blueprint(github_blueprint, url_prefix='/login')


@app.route('/')
def github_login():
    if not github.authorized:
        return redirect(url_for('github.login'))
    else:
        account_info = github.get('/user')
        if account_info.ok:
            account_info_json = account_info.json()
            #return '<h1>Your Github name is {}'.format(account_info_json['login'])
            return render_template('index.html')
    return '<h1>Request failed!</h1>'   

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

@app.route('/comments')
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