from flask import render_template, request, Blueprint, session,redirect, url_for
from models.file import db, User, Admin, ReserveParking, ParkingSpot, ParkingLot

admin_search_bp = Blueprint('admin_search_bp', __name__)

@admin_search_bp.route('/admin/search', methods=['GET', 'POST'])
def admin_search():
    if 'admin' not in session:
        return redirect(url_for('login_bp.login'))
    if request.method == 'GET':
        return render_template('admin_search.html')

    # POST method starts here
    search_option = request.form['search_option']
    query = request.form.get('search', '').strip()
    k = 0  # indicates no result if set to 1

    if search_option == "user_id":
        user = User.query.filter(User.userid.like(f"%{query}%")).first()
        if not user:
            k = 1
        return render_template("admin_search.html", user=user, k=k)

    elif search_option == "user_name":
        user = User.query.filter(User.fullname.like(f"%{query}%")).first()
        if not user:
            k = 1
        return render_template("admin_search.html", user=user, k=k)

    elif search_option == "parkinglot__primelocation":
        lot = ParkingLot.query.filter(ParkingLot.prime_location_name.like(f"%{query}%")).first()
        if not lot:
            k = 1
        return render_template("admin_search.html", lot=lot, k=k)

    elif search_option == "parkinglot__id":
        lot = ParkingLot.query.filter(ParkingLot.lot_id.like(f"%{query}%")).first()
        if not lot:
            k = 1
        return render_template("admin_search.html", lot=lot, k=k)

    elif search_option == "parkingspot_id":
        spot = ParkingSpot.query.filter(ParkingSpot.spot_id.like(f"%{query}%")).first()
        lot = None
        if spot:
            lot = ParkingLot.query.filter_by(lot_id=spot.lot_id).first()
        else:
            k = 1
        return render_template("admin_search.html", spot=spot, lot=lot, k=k)

    elif search_option == "reservation_id":
        res = ReserveParking.query.filter(ReserveParking.res_id.like(f"%{query}%")).first()
        if not res:
            k = 1
            return render_template("admin_search.html", k=k)
        return render_template("admin_search.html", res=[res], k=k)

    elif search_option == "reservation_userid":
        res = ReserveParking.query.filter(ReserveParking.user_id.like(f"%{query}%")).all()
        user = None
        if res:
            user = User.query.filter_by(userid=res[0].user_id).first()
        else:
            k = 1
        print(res)
        return render_template("admin_search.html", res=res, user=user, k=k)

    elif search_option == "reservation_vno":
        res = ReserveParking.query.filter(ReserveParking.vehicle_no.like(f"%{query}%")).first()
        if not res:
            k = 1
            return render_template("admin_search.html", k=k)
        return render_template("admin_search.html", res=[res], k=k)

    return render_template("admin_search.html", k=1)  # fallback
