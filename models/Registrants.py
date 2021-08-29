from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# define what our database user looks like.
class Registrants(db.Model):

    __tablename__ = "innerve_registrants"

    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(20), unique=True, index=True)
    email = db.Column('email', db.String(60), unique=True, index=True)
    first_name = db.Column('first_name', db.String(20))
    last_name = db.Column('last_name', db.String(20))
    branch = db.Column('branch', db.String(20))
    year = db.Column('year', db.Integer())
    registered_on = db.Column('registered_on', db.DateTime)

    def __init__(self, username, email, first_name, last_name, branch, year):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.branch = branch
        self.year = year
        self.registered_on = datetime.utcnow()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)

    # don't judge me...
    def unique(self):

        mail_exists = db.session.query(Registrants.email).filter_by(email=self.email).scalar() is None
        user_exists = db.session.query(Registrants.username).filter_by(username=self.username).scalar() is None

        # none exist
        if mail_exists and user_exists:
            return 0

        # email already exists
        elif mail_exists == False and user_exists == True:
            return -1

        # username already exists
        elif mail_exists == True and user_exists == False:
            return -2

        # both already exists
        else:
            return -3