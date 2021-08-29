# imports
from flask import Flask, render_template, request, redirect, url_for, flash, session
from models.Registrants import Registrants, db

# setup
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "SuperSecretKey"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///innerve.db'

db.init_app(app)


# create the db structure
with app.app_context():
    db.create_all()


# The form page
@app.route('/', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        session.clear()
        return render_template('register.html')
    else: # POST request
        # get the data from our form
        username = request.form['username']
        email = request.form['email']
        first_name, last_name = request.form['first-name'], request.form['last-name']
        branch, year = request.form['branch'], request.form['year']

        # create a user, and check if its unique
        registrant = Registrants(username, email, first_name, last_name, branch, year)
        usr_unique = registrant.unique()

        # add the user
        if usr_unique == 0:
            db.session.add(registrant)
            db.session.commit()
            flash("Registration Successful! Welcome to Innerve@IGDTUW")
            return redirect(url_for('success'))

        # else error check what the problem is
        elif usr_unique == -1:
            flash("Sorry. Email already registered. Please check.")
            return render_template('register.html')

        elif usr_unique == -2:
            flash("Sorry. Username taken. Please try again.")
            return render_template('register.html')

        else:
            flash("Sorry. Username has been taken along with the email also. Please check.")
            return render_template('register.html')

@app.route('/success', methods=["GET"])
def success():
    return render_template('success.html')


if __name__ == "__main__":
	app.run()
