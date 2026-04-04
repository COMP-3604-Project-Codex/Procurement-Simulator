
from flask import Blueprint, flash, request, redirect, render_template, url_for
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
            flash("You are logged in as an admin and therefore cannot access student page")
            return redirect(url_for('index_views.index_page'))
        return f(*args, **kwargs)
    return decorated_function

def group_status_check(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        exists = check_studentGroup(current_user.id)
    
        if not exists:
            flash("You either have not created a group yet or your group has been reject or removed, create a new one")
            return redirect(url_for('student_views.student_create_group_page'))
        
        group = get_group(exists.groupID)

        if group.status == "requested":
            flash("Your group has not been approved yet")
            return redirect(request.referrer)
        
        return f(*args, **kwargs)
    return decorated_function

student_views = Blueprint('student_views', __name__, template_folder='../templates')

#Global variables for testing ui pre-models
ASSIGNED_LOTS =[
    {
        'id': 1,
        'lab_type': 'One large GIS Lab with 60 workstations',
        'budget': 150000.00,
        'description': 'The lab should be outfitted with machines that can run enterprise-level Geographic Information Systems Software.'
    },
    {
        'id': 2,
        'lab_type': 'One small Cyber Cafe with 20 workstations',
        'budget': 10000.00,
        'description': 'General purpose machines for web browsing and office tasks.'
    }
]

STUDENT_RFPS = []

STUDENT_GRP = []

STUDENT_DATA = [
    {'name': 'Daniel Roberts', 'student_id': '20240123'},
    {'name': 'Michael Johnson', 'student_id': '20231245'},
    {'name': 'Samantha Lewis', 'student_id': '20229876'},
    {'name': 'Christopher Brown', 'student_id': '20235678'},
    {'name': 'Ashley Williams', 'student_id': '20246789'},
    {'name': 'Emily Thompson', 'student_id': '20242345'},
    {'name': 'Brandon Phillips', 'student_id': '20238901'},
]

STUDENT_BIDS = [
    {
        'bid_id': 101,
        'lot_id': '1',
        'vendor_name': 'Dell Technologies',
        'total_price': 145000.00,
        'status': 'Pending',
        'spec_summary': 'Precision Workstations with i9 Processors'
    },
    {
        'bid_id': 102,
        'lot_id': '1',
        'vendor_name': 'HP Enterprise',
        'total_price': 152000.00,
        'status': 'Pending',
        'spec_summary': 'Z-Book Fury with Xeon Processors'
    }
]
@student_views.route('/student', methods=['GET'])
@student_required
def student_home_page():
    return redirect(url_for('student_views.student_group_details_page'))


@student_views.route('/student/create-group', methods=['GET', 'POST']) 
@student_required
def student_create_group_page():
    exists = check_studentGroup(current_user.id)
    
    if exists:
        flash ("You are already in a group")
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

                student = db.session.scalars(
                    db.select(Student)
                    .filter_by(id=ID)
                ).first()

                if student:
                    students.append(student)
            
            if you:
                strings = []
                for student in students:
                    string = f"{student.name}, "
                    strings.append(string)

                if not strings:
                    flash("You are already in a group")
                    return redirect(url_for('student_views.student_group_details_page'))

                if len(strings) >= 2:
                    strings[-2] = f"{students[-2].name} and "
                    strings[-1] = f"{students[-1].name}"

                    flash(f"You are already in a group and {''.join(strings)} are already in groups")
                    return redirect(url_for('student_views.student_group_details_page'))
                else:
                    strings[0] = f"{students[0].name}"

                    flash(f"You are already in a group and {''.join(strings)} is already in a group")
                    return redirect(url_for('student_views.student_group_details_page'))
            else:
                strings = []
                for student in students:
                    string = f"{student.name}, "
                    strings.append(string)

                if len(strings) >= 2:
                    strings[-2] = f"{students[-2].name} and "
                    strings[-1] = f"{students[-1].name}"

                    flash(f"{''.join(strings)} are already in groups")
                    return redirect(url_for('student_views.student_group_details_page'))
                else:
                    strings[0] = f"{students[0].name}"

                    flash(f"{''.join(strings)} is already in a group")
                    return redirect(url_for('student_views.student_group_details_page'))

        group = create_group(name)

        for member in members:
            add_studentGroup(member, group.id)
        
        flash(f"Group '{name}' created successfully!")
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
        flash("You either have not created a group yet or your group has been reject or removed, create a new one")
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

    selected_lot_id = request.args.get('selected_lot', '1')
    current_lot = next((l for l in ASSIGNED_LOTS if str(l['id']) == selected_lot_id), ASSIGNED_LOTS[0])
    

    bids_for_lot = [b for b in STUDENT_BIDS if b['lot_id'] == selected_lot_id]

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
        ('screen', 'Screen Size & Resolution'),
        ('os', 'Operating System(s)'),
        ('cpu', 'CPU'),
        ('ram', 'Memory (RAM)'),
        ('hdd', 'Hard Drive'),
        ('graphics', 'Graphics'),
        ('peripherals', 'External Peripherals'),
        ('features', 'Features'),
        ('io', 'I/O')
    ]

    # Find bid
    bid = next((b for b in STUDENT_BIDS if b['bid_id'] == bid_id), None)
    
    # Find associated lot
    lot = next((l for l in ASSIGNED_LOTS if str(l['id']) == str(bid['lot_id'])), None)

    if request.method == 'POST':
        # Logic for saving comments to go here
        flash("Comment saved for review.")
        return redirect(url_for('student_views.student_bid_details_page', bid_id=bid_id))

    return render_template(
        'student/client_bid_details.html',
        active_page='view-bids',
        title=f"Bid Analysis: {bid['vendor_name']}",
        bid=bid,
        lot=lot,
        technical_specs=technical_specs
    )


@student_views.route('/student/client-evaluation', methods=['GET'])
@student_required
@group_status_check
def student_client_evaluation_page():

    selected_lot_id = request.args.get('selected_lot', '1')

    ALL_EVALUATIONS = [
        {'bid_id': 101, 'lot_id': '1', 'group_name': 'Tech Titans', 'cost': 14500.0, 'specs_met': '9/9', 'rating': 4.8, 'is_selected': True},
        {'bid_id': 102, 'lot_id': '1', 'group_name': 'Global Systems', 'cost': 12200.0, 'specs_met': '7/9', 'rating': 3.5, 'is_selected': False},
        {'bid_id': 201, 'lot_id': '2', 'group_name': 'NetConnect Ltd', 'cost': 8500.0, 'specs_met': '5/5', 'rating': 4.2, 'is_selected': False},
        {'bid_id': 202, 'lot_id': '2', 'group_name': 'Cyber Shield', 'cost': 9200.0, 'specs_met': '4/5', 'rating': 3.9, 'is_selected': False}
    ]

    # filtering evals
    filtered_evals = [e for e in ALL_EVALUATIONS if e['lot_id'] == selected_lot_id]

     
    lots_list = [
        {'id': 1, 'lab_type': 'Workstations'},
        {'id': 2, 'lab_type': 'Networking Gear'}
    ]

    return render_template(
        'student/client_eval.html',
        active_page='client-evaluation',
        title='Bid Evaluations',
        evaluations=filtered_evals,  
        lots=lots_list,
        selected_lot=selected_lot_id
    )


#Student view as vendor

@student_views.route('/student/rfp-gallery', methods=['GET'])
@student_required
@group_status_check
def rfp_gallery_page():

    # rfps available
    
    available_rfps = [
        {
            'id': 'RFP-001',
            'title': 'GIS Lab Workstations',
            'client': 'Group 3 Tech Titans',
            'deadline': '2026-04-15',
            'status': 'Open',
            'description': 'One large GIS Lab with 60 workstations'
        },
        {
            'id': 'RFP-002',
            'title': 'Cyber Cafe',
            'client': 'Group 2 Cyber Shield',
            'deadline': '2026-04-20',
            'status': 'Open',
            'description': 'One small Cyber Cafe with 20 workstations.'
        }
    ]

    return render_template(
        'student/vendor_rfp_gallery.html',
        # title='View RFPs',
        active_page='rfp-gallery',
        rfps=available_rfps
    )


# Vendor-submitted bids
@student_views.route('/student/vendor-bids', methods=['GET'])
@student_required
@group_status_check
def submitted_bids_page():

    # This data represents bids 
    submitted_bids = [
        {
            'bid_id': 'BID-901',
            'rfp_title': 'GIS Lab',
            'target_group': 'Group 3 (Tech Titans)',
            'submitted_at': datetime(2026, 3, 25, 14, 30),             
            'status': 'Accepted', 
        },
        {
            'bid_id': 'BID-902',
            'rfp_title': 'Design Studio',
            'target_group': 'Group 2 (Cyber Shield)',
            'submitted_at': datetime(2026, 3, 26, 10, 15), 
            'status': 'Pending', 
        },
        {
            'bid_id': 'BID-903',
            'rfp_title': 'Cyber Cafe ',
            'target_group': 'Group 1 (Global Systems)',
            'submitted_at': datetime(2026, 3, 20, 9, 0), 
            'status': 'Rejected', 
        }
    ]

    return render_template(
        'student/vendor_bids.html',
        active_page='my-bids',
        bids=submitted_bids
    )