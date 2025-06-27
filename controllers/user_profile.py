from flask import render_template, request, redirect, url_for, session,Blueprint
from models.file import db,User,Admin,ReserveParking,ParkingSpot,ParkingLot

userprofile_bp = Blueprint('userprofile_bp',__name__)

@userprofile_bp.route('/user/edit_profile/<userid>',methods=['GET','POST'])
def userprofile(userid):
    if 'user' not in session or session['user'] != userid:
        return redirect(url_for('login_bp.login'))
    if request.method=='GET':
        ud=User.query.filter_by(userid=userid).first()
        return render_template('user_profile.html',ud=ud)
    elif request.method=='POST':
        ui=request.form['userid']
        fn=request.form['fullname']
        e=request.form['email']
        a=request.form['address']
        pc=request.form['pincode']

        ex=User.query.filter_by(userid=ui).first()
        if ex and ex.userid != userid:
            ud=User.query.filter_by(userid=userid).first()
            return render_template('user_profile.html', ud=ud, error="User ID already exists. Please choose another.")
        
        uud=db.session.query(User).filter_by(userid=userid).first()
        uud.userid=ui
        uud.fullname=fn
        uud.email=e
        uud.Address=a
        uud.pincode=pc

        db.session.commit()
        return redirect(url_for('user_bp.user_home',userid=ui))