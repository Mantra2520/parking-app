from flask import render_template, request, Blueprint, session,redirect, url_for
from models.file import db,User,Admin,ReserveParking,ParkingSpot,ParkingLot
from datetime import datetime

admin_summary_bp=Blueprint('admin_summary_bp',__name__)

@admin_summary_bp.route('/admin/summary',methods=['GET'])
def admin_summary():
    if 'admin' not in session:
        return redirect(url_for('login_bp.login'))
    lot_rev = {}
    lot_av = {}
    lot_oc = {}
    total_rev = 0

    lots = ParkingLot.query.all()

    # Initialize dictionaries
    for lot in lots:
        lot_rev[lot.lot_id] = 0
        lot_av[lot.lot_id] = 0
        lot_oc[lot.lot_id] = 0

    # Count available and occupied spots
    spots = ParkingSpot.query.all()
    for spot in spots:
        if spot.status == "A":
            lot_av[spot.lot_id] += 1
        elif spot.status == "O":
            lot_oc[spot.lot_id] += 1

    # Calculate revenue
    reservations = ReserveParking.query.filter(ReserveParking.out_time.isnot(None)).all()
    if reservations :
        for res in reservations:
            in_datetime = datetime.combine(res.in_date, res.in_time)
            out_datetime = datetime.combine(res.out_date, res.out_time)
            hours = (out_datetime - in_datetime).total_seconds() / 3600
            revenue = res.cost_unit_time * hours
            total_rev += revenue

            spot = ParkingSpot.query.get(res.spot_id)
            lot_id = spot.lot_id
            lot_rev[lot_id] += revenue

    # Build aligned lists for chart
    lot_labels = [f"Lot {lot.lot_id}" for lot in lots]
    revenues = [round(lot_rev[lot.lot_id], 2) for lot in lots]
    available_counts = [lot_av[lot.lot_id] for lot in lots]
    occupied_counts = [lot_oc[lot.lot_id] for lot in lots]
    total_rev = round(total_rev, 2)

    return render_template('admin_summary.html',total_rev=total_rev,lot_labels=lot_labels,revenues=revenues,available_counts=available_counts,occupied_counts=occupied_counts)
