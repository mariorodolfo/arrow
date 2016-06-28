from flask import Flask, render_template, flash, request, url_for, redirect, session
from content_management import Content
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
from dbconnect import connection
from MySQLdb import escape_string as thwart
import gc



TOPIC_DICT = Content()

app = Flask(__name__)

app.secret_key = "my precious"



@app.route('/')
def home():
	return render_template('index.html')

@app.route('/dashboard/')
def dashboard():
    return render_template("dashboard.html", TOPIC_DICT = TOPIC_DICT)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(404)
def method_not_found(e):
    return render_template("405.html")


@app.route('/login/', methods=["GET","POST"])
def login_page():

    error = ''
    try:
        if request.method == "POST":               
            attempted_username = request.form['username']
            attempted_password = request.form['password']

            #flash(attempted_username)
            #flash(attempted_password)

            if attempted_username == "admin" and attempted_password == "password":
                return redirect(url_for('dashboard'))                
            else:
                error = "Credenciais invalidas."
        return render_template("login.html", error = error)
    except Exception as e:
        #flash(e)
        return render_template("login.html", error = error)   



#@app.route('/slashboard/')
#def slashboard():
#    try:
#        return render_template("dashboard.html", TOPIC_DICT = shamwow)
#    except Exception as e:
#        return render_template("500.html", error = str(e))
#

class RegistrationForm(Form):
    username = StringField('Usuario', [validators.Length(min=4, max=20)])
    cpf = StringField(' CPF ', [validators.Length(min=6, max=11)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Senha', [
        validators.Required(),
        validators.EqualTo('confirm', message='Senhas devem ser iguais')
    ])
    confirm = PasswordField('Repita a senha')
    endereco = StringField('Endereco', [validators.Length(min=6, max=200)])
    accept_tos = BooleanField('Voce aceita os termos de servico', [validators.Required()])
    












@app.route('/cadastro/', methods=["GET","POST"])
def register_page():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            username  = form.username.data
            cpf = form.cpf.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            endereco = form.endereco.data
            c, conn = connection()

            x = c.execute("SELECT * FROM users WHERE username = (%s)",
                          (thwart(username)))

            if int(x) > 0:
                flash("Usuario ja existe")
                return render_template('cadastro.html', form=form)

            else:
                c.execute("INSERT INTO users (username, cpf, password, email, endereco, tracking) VALUES (%s, %s, %s, %s, %s, %s)",
                          (thwart(username), thwart(password), thwart(email), thwart(endereco), thwart("/introduction-to-python-programming/")))
                
                conn.commit()
                flash("Thanks for registering!")
                c.close()
                conn.close()
                gc.collect()

                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('dashboard'))

        return render_template("cadastro.html", form=form)

    except Exception as e:
        return(str(e))
		




















if __name__ == '__main___':
	app.run(debug=True)
