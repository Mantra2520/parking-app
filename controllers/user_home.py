from flask import render_template, request, redirect, url_for, session,Blueprint
from models.file import db,User,Admin,ReserveParking,ParkingSpot,ParkingLot
from sqlalchemy import null

user_bp=Blueprint('user_bp',__name__)

@user_bp.route('/user/<userid>', methods=['GET', 'POST'])
def user_home(userid):
    if 'user' not in session or session['user'] != userid:
        return redirect(url_for('login_bp.login'))
    pov = ReserveParking.query.filter_by(user_id=userid).filter(ReserveParking.out_time.is_(None)).all()
    pova = []
    for res in pov:
        spot = ParkingSpot.query.get(res.spot_id)
        lot = ParkingLot.query.get(spot.lot_id)
        pova.append(lot.address)

    lpv = ReserveParking.query.filter(ReserveParking.user_id == userid,ReserveParking.out_time.isnot(None)).order_by(ReserveParking.res_id.desc()).first()
    
    lpva = None
    if lpv:
        spot = ParkingSpot.query.get(lpv.spot_id)
        lot = ParkingLot.query.get(spot.lot_id)
        lpva = lot.address

    if request.method == 'POST':
        s = request.form['search']
        ps = ParkingLot.query.filter(ParkingLot.pin_code.like(f"%{s}%")).all()
        ls = ParkingLot.query.filter(ParkingLot.prime_location_name.like(f"%{s}%")).all()
        data=[]
        # lot=[]
        if ps:
            lot=ps
        elif ls:
            lot=ls
        else :
            lot=[]
        for l in lot:
            s=ParkingSpot.query.filter_by(lot_id=l.lot_id,status="A").first()
            if s:
                l.available = True
                l.spotid = s.spot_id
            else:
                l.available = False
                l.spotid = -1
            data.append(l)
        k=1
        return render_template('user.html', userid=userid, sdata=data, parked=pov, parkeda=pova, hist=lpv, hista=lpva,k=k)

    return render_template('user.html', userid=userid, sdata=[], parked=pov, parkeda=pova, hist=lpv, hista=lpva,k=0)

