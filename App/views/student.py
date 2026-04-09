
from flask import Blueprint, flash, request, redirect, render_template, url_for, send_file
import io
from sqlalchemy import and_
from functools import wraps
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies
from datetime import datetime
from App.models import *
from App.controllers import *
from App.views import *

def student_required(f):
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        if not current_user.is_student():
            flash("You are logged in as an admin and therefore cannot access student page", "failed")
            return redirect(url_for('index_views.index_page'))
        return f(*args, **kwargs)
    return decorated_function

def group_status_check(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        exists = check_studentGroup(current_user.id)
    
        if not exists:
            flash("You either have not created a group yet or your group has been reject or removed, create a new one", "info")
            return redirect(url_for('student_views.student_create_group_page'))
        
        group = get_group(exists.groupID)

        if group.status == "requested":
            flash("Your group has not been approved yet", "info")
            return redirect(request.referrer)
        
        return f(*args, **kwargs)
    return decorated_function

student_views = Blueprint('student_views', __name__, template_folder='../templates')

@student_views.route('/student', methods=['GET'])
@student_required
def student_home_page():
    return redirect(url_for('student_views.student_group_details_page'))

@student_views.route('/student/create-group', methods=['GET', 'POST']) 
@student_required
def student_create_group_page():
    exists = check_studentGroup(current_user.id)
    
    if exists:
        flash ("You are already in a group", "failed")
        return redirect(request.referrer)

    if request.method == 'POST':
        name = request.form.get('group_name')
        members = request.form.getlist('members')
        
        members.append(current_user.id)

        duplicates = []

        for member in members:
            existing = db.session.scalars(
                db.select(StudentGroup)
                .filter_by(studentID = member)
            ).first()

            if existing:
                duplicates.append(member)
            
        if duplicates:
            students = []
            you = False

            for ID in duplicates:
                if ID == current_user.id:
                    you = True
                    continue

                student = get_student(ID)

                if student:
                    students.append(student)
            
            if you:
                strings = []
                for student in students:
                    string = f"{student.name}, "
                    strings.append(string)

                if not strings:
                    flash("You are already in a group", "failed")
                    return redirect(url_for('student_views.student_create_group_page'))

                if len(strings) >= 2:
                    strings[-2] = f"{students[-2].name} and "
                    strings[-1] = f"{students[-1].name}"

                    flash(f"You are already in a group and {''.join(strings)} are already in groups", "failed")
                    return redirect(url_for('student_views.student_create_group_page'))
                else:
                    strings[0] = f"{students[0].name}"

                    flash(f"You are already in a group and {''.join(strings)} is already in a group", "failed")
                    return redirect(url_for('student_views.student_create_group_page'))
            else:
                strings = []
                for student in students:
                    string = f"{student.name}, "
                    strings.append(string)

                if len(strings) >= 2:
                    strings[-2] = f"{students[-2].name} and "
                    strings[-1] = f"{students[-1].name}"

                    flash(f"{''.join(strings)} are already in groups", "failed")
                    return redirect(url_for('student_views.student_create_group_page'))
                else:
                    strings[0] = f"{students[0].name}"

                    flash(f"{''.join(strings)} is already in a group", "failed")
                    return redirect(url_for('student_views.student_create_group_page'))

        if name == "":
            flash("You must enter a group name", "failed")
            return redirect(url_for('student_views.student_create_group_page'))

        if len(members) != 3:
            flash("You must select 2 group members to make a group of 3", "failed")
            return redirect(url_for('student_views.student_create_group_page'))

        group = create_group(name)

        for member in members:
            add_studentGroup(member, group.id)
        
        flash(f"Group '{name}' created successfully!", "success")
        return redirect(url_for('student_views.student_group_details_page'))
    
    students = db.session.scalars(
        db.select(Student)
    ).all()

    candidates = []

    for student in students:
        if student.id == current_user.id:
            continue

        candidate = {}
        candidate["id"] = student.id
        candidate["name"] = student.name
        candidate["student_id"] = student.username
        candidate["selected"] = False

        candidates.append(candidate)

    return render_template(
        'student/create_group.html',
        active_page='create-group',
        title='Create Group',
        candidates=candidates,
    )

@student_views.route('/student/group-details', methods=['GET'])
@student_required
def student_group_details_page():
    exists = check_studentGroup(current_user.id)
    
    if not exists:
        flash("You either have not created a group yet or your group has been reject or removed, create a new one", "info")
        return redirect(url_for('student_views.student_create_group_page'))

    exists.groupID

    current_group = get_group(exists.groupID)

    if current_group.status == "requested":
        status = "Pending Confirmation"
    else:
        status = "Confirmed"

    members = db.session.scalars(
        db.select(Student)
        .join(StudentGroup, Student.id == StudentGroup.studentID)
        .filter(StudentGroup.groupID == current_group.id)
    ).all()

    return render_template(
        'student/group_details.html',
        active_page='group-details',
        title='Group Details',
        status=status,
        group=current_group,
        members=members
    )

@student_views.route('/student/lots', methods=['GET', 'POST'])
@student_required
@group_status_check
def student_lots_page():
    if request.method == 'POST':
        action = request.form.get('action') # 
        lot_id = request.form.get('lot_id')
        
        # Capture data from form
        deviceType = request.form.get('deviceType')
        resolution = request.form.get('screen')
        os = request.form.get('os')
        cpu = request.form.get('cpu')
        ram = request.form.get('ram')
        drive = request.form.get('storage')
        gpu = request.form.get('graphics')
        peripherals = request.form.get('peripherals')
        features = request.form.get('features')
        io = request.form.get('io')

        lot = edit_lotRFP_details(
            id=lot_id,
            deviceType=deviceType,
            resolution=resolution,
            os=os,
            cpu=cpu,
            ram=ram,
            drive=drive,
            gpu=gpu,
            peripherals=peripherals,
            features=features,
            io=io
        )
        
        #  Success Message
        if action == 'submit':
            entry = db.session.scalars(
                db.select(LotGroup)
                .filter_by(lotID=lot_id)
            ).first()

            rfp = get_rfp(entry.groupID, lot_id)

            if not rfp:
                rfp = create_rfp(entry.groupID, lot_id)
                flash(f"RFP for Lot {lot_id} has been submitted!", "success")
            else:
                if rfp.status == "requested":
                    remove = remove_rfp(entry.groupID, lot_id)
                    val = create_rfp(entry.groupID, lot_id)
                    flash(f"RFP for Lot {lot_id} has been edited!", "success")
                else:
                    flash(f"RFP for Lot {lot_id} has already been approved and therefore cannot be changed further", "info")
        else:
            flash(f"Draft for Lot {lot_id} saved successfully.", "info")
            
        return redirect(url_for('student_views.student_lots_page', selected_lot=lot_id))

    entry = db.session.scalars(
        db.select(StudentGroup)
        .filter_by(studentID=current_user.id)
    ).first()

    entry.groupID

    entries = db.session.scalars(
        db.select(LotGroup)
        .filter_by(groupID=entry.groupID)
    ).all()

    lotIDs = []
    for entry in entries:
        lotIDs.append(entry.lotID)

    lotIDs.sort()

    selected_lot_id = request.args.get('selected_lot', str(lotIDs[0]))

    lots = db.session.scalars(
        db.select(Lot)
        .where(Lot.id.in_(lotIDs))
    ).all()

    current_lot = next((lot for lot in lots if lot.id == int(selected_lot_id)), lots[0])

    existing_rfp = db.session.scalars(
        db.select(RFP)
        .filter_by(lotID=int(selected_lot_id))
    ).first()

    return render_template(
        'student/client_lots.html', 
        active_page='lots',
        title='Assigned Lots & RFPs',
        lots=lots,
        current_lot=current_lot,
        existing_rfp=existing_rfp
    )
         
@student_views.route('/student/client-view-bids', methods=['GET'])
@student_required
@group_status_check
def student_view_bids_page():

    ASSIGNED_LOTS = [] 

    yourGroup = db.session.scalars(
        db.select(Group)
        .join(StudentGroup, StudentGroup.groupID == Group.id)
        .filter(StudentGroup.studentID == current_user.id)
    ).first()

    yourLots = db.session.scalars(
        db.select(Lot)
        .join(LotGroup, LotGroup.lotID == Lot.id)
        .filter(LotGroup.groupID == yourGroup.id)
        .order_by(Lot.id)
    ).all()

    for lot in yourLots:
        data = {}

        data["id"] = lot.id
        data["lab_type"] = lot.labType
        data["budget"] = lot.budget
        data["description"] = lot.labTypeObj.description if getattr(lot, 'labTypeObj', None) else lot.labSize

        ASSIGNED_LOTS.append(data)

    selected_lot_id = request.args.get('selected_lot', ASSIGNED_LOTS[0]["id"])

    current_lot_obj = get_lot(selected_lot_id)

    current_lot = {}
    current_lot["id"] = current_lot_obj.id
    current_lot["lab_type"] = current_lot_obj.labType
    current_lot["budget"] = current_lot_obj.budget
    current_lot["description"] = current_lot_obj.labTypeObj.description if getattr(current_lot_obj, 'labTypeObj', None) else current_lot_obj.labSize

    bids_for_lot = []

    bidsReceived = db.session.scalars(
        db.select(Bid)
        .filter_by(lotID=current_lot["id"])
    ).all()

    for bid in bidsReceived:
        data = {}

        data["bid_id"] = bid.id
        data["lot_id"] = bid.lotID

        sourceGroup = get_group(bid.sourceGroupID)

        data["vendor_name"] = sourceGroup.groupName
        data["total_price"] = bid.quotationAmount
        data["timestamp"] = bid.timestamp.strftime('%#m/%#d/%Y, %#I:%M%p').lower()

        bids_for_lot.append(data)

    return render_template(
        'student/client_viewbid.html',
        active_page='view-bids',
        title='Received Bids',
        lots=ASSIGNED_LOTS,
        current_lot=current_lot,
        bids=bids_for_lot
    )

@student_views.route('/student/client-bid-details/<int:bid_id>', methods=['GET', 'POST'])
@student_required
@group_status_check
def student_bid_details_page(bid_id):

    # list of specs to loop through in template
    technical_specs = [
        ('deviceType', 'Device Type'),
        ('resolution', 'Screen Size & Resolution'),
        ('os', 'Operating System(s)'),
        ('cpu', 'CPU'),
        ('ram', 'Memory (RAM)'),
        ('drive', 'Hard Drive'),
        ('gpu', 'Graphics'),
        ('peripherals', 'External Peripherals'),
        ('features', 'Features'),
        ('io', 'I/O')
    ]

    # Find bid

    bidObj = get_bid(bid_id)

    bid = {}
    bid["bid_id"] = bidObj.id
    bid["lot_id"] = bidObj.lotID

    sourceGroup = get_group(bidObj.sourceGroupID)
    bid["vendor_name"] = sourceGroup.groupName
    bid["total_price"] = bidObj.quotationAmount
    bid["timestamp"] = bidObj.timestamp.strftime('%#m/%#d/%Y, %#I:%M%p').lower()
    bid["pdf"] = bidObj.bidDocument
    bid["filename"] = bidObj.bidDocumentName

    lotObj = get_lot(bidObj.lotID)

    lot = {}
    lot["id"] = lotObj.id
    lot["lab_type"] = lotObj.labType
    lot["budget"] = lotObj.budget
    lot["description"] = lotObj.labTypeObj.description if getattr(lotObj, 'labTypeObj', None) else lotObj.labSize

    if request.method == 'POST':
        specsMet = request.form.getlist("specs_selected")
        professionalism = int(request.form.get("professionalism_stars"))
        presentation = int(request.form.get("presentation_stars"))
        budget = int(request.form.get("budget_stars"))

        deviceType = request.form.get("comment_deviceType")
        resolution = request.form.get("comment_resolution")
        os = request.form.get("comment_os")
        cpu = request.form.get("comment_cpu")
        ram = request.form.get("comment_ram")
        drive = request.form.get("comment_drive")
        gpu = request.form.get("comment_gpu")
        peripherals = request.form.get("comment_peripherals")
        features = request.form.get("comment_features")
        io = request.form.get("comment_io")

        bid = get_bid(bid_id)

        sourceGroupID = bid.recipientGroupID
        recipientGroupID = bid.sourceGroupID
        lotID = bid.lotID

        existing = db.session.scalars(
            db.select(Evaluation)
            .filter_by(bidID=bid_id)
        ).first()

        if existing:
            editted = edit_evaluation(existing.id, len(specsMet), presentation, professionalism, budget, deviceType=deviceType, resolution=resolution, os=os, cpu=cpu, ram=ram, drive=drive, gpu=gpu, peripherals=peripherals, features=features, io=io, specsSelected=','.join(specsMet))

            flash("Evaluation updated successfully", "success")
            return redirect(url_for('student_views.student_bid_details_page', bid_id=bid_id))

        evaluation = create_evaluation(sourceGroupID, recipientGroupID, bid_id, lotID, len(specsMet), presentation, professionalism, budget)
        editted = edit_evaluation(evaluation.id, len(specsMet), presentation, professionalism, budget, deviceType=deviceType, resolution=resolution, os=os, cpu=cpu, ram=ram, drive=drive, gpu=gpu, peripherals=peripherals, features=features, io=io, specsSelected=','.join(specsMet))

        flash("Evaluation created successfully", "success")
        return redirect(url_for('student_views.student_bid_details_page', bid_id=bid_id))

    existing = db.session.scalars(
        db.select(Evaluation)
        .filter_by(bidID=bid_id)
    ).first()

    return render_template(
        'student/client_bid_details.html',
        active_page='view-bids',
        title=f"Bid Analysis: {bid['vendor_name']}",
        bid=bid,
        lot=lot,
        technical_specs=technical_specs,
        existing=existing
    )

@student_views.route('/student/client-evaluation', methods=['GET', 'POST'])
@student_required
@group_status_check
def student_client_evaluation_page():
    yourGroup = db.session.scalars(
        db.select(Group)
        .join(StudentGroup, StudentGroup.groupID == Group.id)
        .filter(StudentGroup.studentID == current_user.id)
    ).first()

    yourLots = db.session.scalars(
        db.select(Lot)
        .join(LotGroup, LotGroup.lotID == Lot.id)
        .filter(LotGroup.groupID == yourGroup.id)
        .order_by(Lot.id)
    ).all()

    selected_lot_id = request.args.get('selected_lot', yourLots[0].id)

    if request.method == "POST":
        evaluationID = int(request.form.get("evaluationID"))

        selected = db.session.scalars(
            db.select(Evaluation)
            .filter(and_(Evaluation.sourceGroupID == yourGroup.id, Evaluation.lotID == selected_lot_id, Evaluation.status == "selected"))
        ).first()

        if selected:
            flash("You have already selected an evaluation for this group. Your choice is permanent unless the admin removes the evaluation", "failed")
            return redirect(request.referrer) 

        else:
            select_evaluation(evaluationID)

            flash("You have successfully selected selected an evaluation", "success")
            return redirect(request.referrer) 

    filtered_evals = []

    yourEvaluations = db.session.scalars(
        db.select(Evaluation)
        .filter(and_(Evaluation.sourceGroupID == yourGroup.id, Evaluation.lotID == selected_lot_id))
    ).all()
        

    for evaluation in yourEvaluations:
        data = {}

        data["id"] = evaluation.id
        data["bid_id"] = evaluation.bidID
        data["lot_id"] = evaluation.lotID

        receipientGroup = get_group(evaluation.recipientGroupID)
        data["group_name"] = receipientGroup.groupName

        evaluatedBid = get_bid(evaluation.bidID)
        data["cost"] = evaluatedBid.quotationAmount

        data["specs_met"] = f"{evaluation.specsMet}/10"
        data["rating"] = evaluation.overallScore

        if evaluation.status == "draft":
            data["is_selected"] = False
        else:
            data["is_selected"] = True

        filtered_evals.append(data)

    lots_list = []

    for lot in yourLots:
        data = {}

        data["id"] = lot.id
        data["lab_type"] = lot.labType

        lots_list.append(data)
    
    return render_template(
        'student/client_eval.html',
        active_page='client-evaluation',
        title='Bid Evaluations',
        evaluations=filtered_evals,  
        lots=lots_list,
        selected_lot=selected_lot_id
    )

#Student view as vendor
@student_views.route('/student/rfp-gallery', methods=['GET', 'POST'])
@student_required
@group_status_check
def rfp_gallery_page():
    if request.method == "POST":
        pdf = request.files['pdf']
        recipientGroupID = int(request.form.get("groupID"))
        sourceGroupID = int(request.form.get("sourceGroupID"))
        lotID = int(request.form.get("lotID"))
        amount = float(request.form.get("amount"))

        entries = db.session.scalars(
            db.select(LotGroup)
            .filter_by(groupID=sourceGroupID)
        ).all()

        yourLots = []

        for entry in entries:
            yourLots.append(entry.lotID)

        lot = get_lot(lotID)

        if lotID in yourLots:
            flash(f"Lot {lotID} ({lot.labType}) is assigned to your group, you cannot place a bid on your own lot", "failed")
            return redirect(url_for('student_views.rfp_gallery_page'))
        
        yourGroup = db.session.scalars(
            db.select(Group)
            .join(StudentGroup, StudentGroup.groupID == Group.id)
            .filter(StudentGroup.studentID == current_user.id)
        ).first()

        duplicate = db.session.scalars(
            db.select(Bid)
            .filter(and_(Bid.lotID == lotID, Bid.sourceGroupID == yourGroup.id))
        ).first()

        if duplicate:
            flash(f"You have already placed a bid on Lot {lotID} ({lot.labType}), you can only place 1 bid on each lot", "failed")
            return redirect(url_for('student_views.rfp_gallery_page'))

        bid = create_bid(lotID, sourceGroupID, recipientGroupID, pdf.read(), pdf.filename, amount)
        flash(f"Bid successfully placed on Lot {lotID} ({lot.labType})", "success")
        return redirect(url_for('student_views.rfp_gallery_page'))

    entry = db.session.scalars(
        db.select(StudentGroup)
        .filter_by(studentID=current_user.id)
    ).first()

    sourceGroupID = entry.groupID

    rfp_gallery = db.session.scalars(
        db.select(RFP)
        .filter_by(status="approved")
    ).all()

    available_rfps = []

    for rfp in rfp_gallery:
        data = {}

        data["groupID"] = rfp.groupID
        data["lotID"] = rfp.lotID

        lot = get_lot(rfp.lotID)

        data["title"] = lot.labType

        group = get_group(rfp.groupID)

        data["client"] = group.groupName
        data["timestamp"] = rfp.timestamp.strftime('%#m/%#d/%Y, %#I:%M%p').lower()
        data["status"] = rfp.status 
        data["description"] = lot.labTypeObj.description if getattr(lot, 'labTypeObj', None) else lot.labSize
        data["deviceType"] = rfp.deviceType
        data["resolution"] = rfp.resolution
        data["os"] = rfp.os
        data["cpu"] = rfp.cpu
        data["ram"] = rfp.ram
        data["drive"] = rfp.drive
        data["gpu"] = rfp.gpu
        data["io"] = rfp.io
        data["peripherals"] = rfp.peripherals
        data["features"] = rfp.features

        available_rfps.append(data)

    return render_template(
        'student/vendor_rfp_gallery.html',
        title='RFP Gallery',
        active_page='rfp-gallery',
        rfps=available_rfps,
        sourceGroupID=sourceGroupID
    )

# Vendor-submitted bids
@student_views.route('/student/vendor-bids', methods=['GET'])
@student_required
@group_status_check
def submitted_bids_page():

    # This data represents bids 
    submitted_bids = []
    accepted = 0
    pending = 0
    rejected = 0

    yourGroup = db.session.scalars(
        db.select(Group)
        .join(StudentGroup, StudentGroup.groupID == Group.id)
        .filter(StudentGroup.studentID == current_user.id)
    ).first()

    yourBids = db.session.scalars(
        db.select(Bid)
        .filter_by(sourceGroupID=yourGroup.id)
    ).all()

    for bid in yourBids:
        data = {}

        data["bid_id"] = bid.id

        lot = get_lot(bid.lotID)

        data["rfp_title"] = lot.labType

        group = get_group(bid.recipientGroupID)

        data["target_group"] = group.groupName
        data["submitted_at"] = bid.timestamp

        selected = db.session.scalars(
            db.select(Evaluation)
            .filter(Evaluation.lotID == bid.lotID, Evaluation.status == "selected")
        ).first()

        if selected:
            if selected.bidID == bid.id:   
                data["status"] = "Accepted"
                accepted += 1
            else:
                data["status"] = "Rejected"
                rejected += 1
        else:
            data["status"] = "Pending"
            pending += 1

        data["bidDocument"] = bid.bidDocument
        data["bidDocumentName"] = bid.bidDocumentName

        submitted_bids.append(data)
    

    return render_template(
        'student/vendor_bids.html',
        active_page='vendor-bids',
        bids=submitted_bids,
        title='My Submitted Bids',
        accepted = accepted,
        pending = pending,
        rejected = rejected
    )

@student_views.route('/student/bid-document/<int:bid_id>')
@student_required
def serve_bid_document(bid_id):
    bid = get_bid(bid_id)
    if not bid:
        return "Not found", 404
    return send_file(
        io.BytesIO(bid.bidDocument),
        mimetype='application/pdf',
        download_name=bid.bidDocumentName
    )