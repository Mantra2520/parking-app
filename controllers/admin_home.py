from flask import render_template, request, redirect, url_for, session,Blueprint
from models.file import db,User,Admin,ReserveParking,ParkingSpot,ParkingLot

admin_bp=Blueprint('admin_bp',__name__)

@admin_bp.route('/admin/home')
def admin_home():
    if 'admin' not in session:
        return redirect(url_for('login_bp.login'))
    PL=[]
    lots=ParkingLot.query.all()
    occ=[]
    for lot in lots:
        OC=ParkingSpot.query.filter_by(lot_id=lot.lot_id,status='O').count()
        PL.append([lot.lot_id,lot.max_spots,OC])
        occ.append((OC/(lot.max_spots))*100)
    return render_template('admin.html',PL=PL,occupancy=occ)

@admin_bp.route('/admin/edit_parking/<lotid>',methods=['GET','POST'])
def edit_parkinglot(lotid):
    if request.method=='GET':
        lotdet=ParkingLot.query.filter_by(lot_id=lotid).first()
        return(render_template('edit_parkingspot.html',details=lotdet))
    elif request.method == 'POST':
        pl=request.form['prime_location']
        a=request.form['address']
        pc=request.form['pincode']
        pr=request.form['price']

        el=db.session.query(ParkingLot).filter_by(lot_id=lotid).first()
        el.prime_location_name=pl
        el.address=a
        el.pin_code=pc
        el.price=pr

        db.session.commit()
        return redirect(url_for('admin_bp.admin_home'))
    
@admin_bp.route('/admin/delete_parking/<lotid>',methods=['GET'])
def delete_parkinglot(lotid):
    dlso=ParkingSpot.query.filter_by(lot_id=lotid,status='O').first()
    if dlso:
        return render_template('admin_error.html',err="del")
    else:
        dls=db.session.query(ParkingSpot).filter_by(lot_id=lotid).all()
        for i in dls:
            db.session.delete(i)
        db.session.commit()
        dl=db.session.query(ParkingLot).filter_by(lot_id=lotid).first()
        db.session.delete(dl)
        db.session.commit()
        return redirect(url_for('admin_bp.admin_home'))
        
@admin_bp.route('/admin/new_lot',methods=['GET','POST'])
def new_lot():
    if request.method == 'GET':
        return render_template('new_lot.html')
    elif request.method =='POST':
        lid=request.form['lotid']
        pl=request.form['prime_location']
        a=request.form['address']
        pc=request.form['pincode']
        pr=request.form['price']
        ms=int(request.form['max_spots'])

        ex=db.session.query(ParkingLot).filter_by(lot_id=lid).first()

        if ex:
            return render_template('admin_error.html',err="lotid")
        else:
            nl=ParkingLot(lot_id=lid,prime_location_name=pl,price=pr,address=a,pin_code=pc,max_spots=ms)
            db.session.add(nl)
            db.session.commit()

            for i in range(1, ms + 1):
                sid =f"{lid}{i}"
                ns=ParkingSpot(spot_id=sid,lot_id=lid,status="A")
                db.session.add(ns)
            db.session.commit()
            return redirect(url_for('admin_bp.admin_home'))

@admin_bp.route('/admin/lot_details/<lotid>')
def lot_details(lotid):
    ocount=0
    lot = ParkingLot.query.get(lotid)
    spots = ParkingSpot.query.filter_by(lot_id=lotid).all()
    for spot in spots:
        if spot.status == "O":
            ocount+=1
    return render_template('lot_details.html', lot=lot, spots=spots, occupied=ocount)

    
