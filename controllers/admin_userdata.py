from flask import render_template, request, Blueprint, session,redirect, url_for
from models.file import db,User,Admin,ReserveParking

admin_userdata_bp=Blueprint('admin_userdata_bp',__name__)

@admin_userdata_bp.route('/admin/user',methods=['GET'])
def admin_userdata():
    if 'admin' not in session:
            return redirect(url_for('login_bp.login'))
    ures={}
    UD=User.query.all()
    for us in UD:
        res=ReserveParking.query.filter_by(user_id=us.userid).count()
        ures[us.userid]=res
    print(ures)
    return(render_template('admin_userdata.html',users=UD,res=ures))

@admin_userdata_bp.route('/admin/user/<userid>')
def user_reservations(userid):
    user = User.query.filter_by(userid=userid).first()

    reservations = ReserveParking.query.filter_by(user_id=userid).order_by(ReserveParking.in_date.desc(), ReserveParking.in_time.desc()).all()
    return render_template("admin_userreservations.html", user=user, reservations=reservations)
