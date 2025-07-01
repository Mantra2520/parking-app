from flask import Flask
from models.file import db, User, Admin, ParkingLot, ParkingSpot, ReserveParking
from controllers.login import login_bp
from controllers.admin_home import *
from controllers.admin_userdata import *
from controllers.admin_search import *
from controllers.admin_summary import *
from controllers.user_home import *
from controllers.user_profile import *
from controllers.user_summary import *
from controllers.user_booking import *
from datetime import datetime

app = Flask(__name__, template_folder='templates')

app.secret_key = 'myparkingapp@123'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'

db.init_app(app)

with app.app_context():
    db.create_all()

    if not Admin.query.filter_by(admin='admin').first():
        new_admin = Admin(admin='admin', password = 'admin123')
        db.session.add(new_admin)
        db.session.commit()


app.register_blueprint(login_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(admin_userdata_bp)
app.register_blueprint(admin_search_bp)
app.register_blueprint(admin_summary_bp)
app.register_blueprint(user_bp)
app.register_blueprint(userprofile_bp)
app.register_blueprint(usersummary_bp)
app.register_blueprint(userbooking_bp)


if __name__ == '__main__':
    app.run(debug=True)


