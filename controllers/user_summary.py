from flask import render_template, request, redirect, url_for, session,Blueprint
from models.file import db,User,Admin,ReserveParking,ParkingSpot,ParkingLot
from datetime import datetime, timedelta

usersummary_bp=Blueprint('usersummary_bp',__name__)

@usersummary_bp.route('/usear/summary/<userid>',methods=['GET'])
def usersummary(userid):
    if 'user' not in session or session['user'] != userid:
        return redirect(url_for('login_bp.login'))
    pov = ReserveParking.query.filter_by(user_id=userid).filter(ReserveParking.out_time.is_(None)).order_by(ReserveParking.res_id.desc()).all()
    pova = []
    for res in pov:
        spot = ParkingSpot.query.get(res.spot_id)
        lot = ParkingLot.query.get(spot.lot_id)
        pova.append(lot.address)
    lpv = ReserveParking.query.filter(ReserveParking.user_id == userid,ReserveParking.out_time.isnot(None)).order_by(ReserveParking.res_id.desc()).all()
    
    lpva = []
    lpvlid=[]
    lot_names = []
    s={}
    total_minutes=0
    total_money=0
    total_hours=0
    for res in lpv:
        spot = ParkingSpot.query.get(res.spot_id)
        lot = ParkingLot.query.get(spot.lot_id)
        fes=ParkingSpot.query.filter_by(lot_id=lot.lot_id,status="A").first()
        if fes == None:
            s[res.res_id]="0"
        else:
            s[res.res_id]=fes.spot_id
        lpvlid.append(lot.lot_id)
        lpva.append(lot.address)
        lot_names.append(lot.prime_location_name)
        in_dt = datetime.combine(res.in_date, res.in_time)
        out_dt = datetime.combine(res.out_date, res.out_time)

        if out_dt < in_dt:
            out_dt += timedelta(days=1)


        duration = out_dt - in_dt
        minutes = duration.total_seconds() / 60
        total_minutes += minutes

        
        time_units = minutes / 60
        cost = time_units * res.cost_unit_time
        total_money += cost

        total_hours = int(total_minutes / 60)
    most_used_lot = None
    if lot_names:
        most_used_lot = max(set(lot_names), key=lot_names.count)
    print(s)

    
    
    return render_template('user_summary.html', userid=userid, parked=pov, parkeda=pova, hist=lpv, hista=lpva,tres=len(lpv),tt=total_hours,tm=round(total_money,2),most_used_lot=most_used_lot,lotid=lpvlid,spotid=s)