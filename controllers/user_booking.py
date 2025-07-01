from flask import render_template, request, redirect, url_for, session,Blueprint
from models.file import db,User,Admin,ReserveParking,ParkingSpot,ParkingLot
from datetime import datetime

userbooking_bp=Blueprint('userbooking_bp',__name__)


@userbooking_bp.route('/user/booking/<userid>/<lotid>/<spotid>',methods=['GET','POST'])
def userbooking(userid,lotid,spotid):
        if request.method=='GET':
            lot = ParkingLot.query.get(lotid)
            return render_template('user_booking.html',userid=userid,lotid=lotid,lot=lot,spotid=spotid)
        elif request.method == 'POST':
            vno=request.form['vno']
            now = datetime.now()
            intime = now.replace(second=0, microsecond=0).time()
            date=now.date()
            lot = ParkingLot.query.get(lotid)
            cost=lot.price

            if len(vno) != 10 or not vno[0:2].isalpha() or not vno[2:4].isnumeric() or not vno[4:6].isalpha() or not vno[6:].isnumeric():
                return render_template('user_booking.html',userid=userid,lotid=lotid,lot=lot,spotid=spotid,error="Invalid Vehicle Number")

            reservation = ReserveParking(spot_id=spotid,user_id=userid,vehicle_no=vno,in_date=date,in_time=intime,cost_unit_time=cost)

            db.session.add(reservation)
            spot = ParkingSpot.query.get(spotid)
            spot.status = "O"
            db.session.commit()

            return redirect(url_for('user_bp.user_home',userid=userid))
        
@userbooking_bp.route('/user/release/<userid>/<resid>',methods=['GET','POST'])
def userrelease(userid,resid):
    if request.method=='GET':
        res=ReserveParking.query.get(resid)
        return render_template('user_release.html',res=res)
      
    elif request.method=='POST':
        now = datetime.now()
        outtime=now.replace(second=0, microsecond=0).time()
        out_date=now.date()

        res=ReserveParking.query.get(resid)
        res.out_date=out_date
        res.out_time=outtime

        spot = ParkingSpot.query.get(res.spot_id)
        spot.status = "A"

        db.session.commit()

        in_datetime = datetime.combine(res.in_date, res.in_time)
        out_datetime = datetime.combine(out_date, outtime)
        hours = (out_datetime - in_datetime).total_seconds() / 3600
        cost = res.cost_unit_time * hours

        return render_template('user_payment.html', res=res, hours=hours, cost=cost, userid=userid)

@userbooking_bp.route('/user/payment/<userid>/<resid>', methods=['POST'])
def payment_done(userid, resid):
    cost = float(request.form.get("final_cost"))
    return render_template("user_paid.html", userid=userid)