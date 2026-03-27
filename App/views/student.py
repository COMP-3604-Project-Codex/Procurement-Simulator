from flask import Blueprint, flash, request, redirect, render_template, url_for


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
def student_home_page():
    return redirect(url_for('student_views.student_create_group_page'))


@student_views.route('/student/create-group', methods=['GET', 'POST']) 
def student_create_group_page():
    if request.method == 'POST':
        name = request.form.get('group_name')
        members = request.form.getlist('members')
        
        new_group = {
            "name": name,
            "members": members,
            "status": "Pending Admin Approval"
        }
        STUDENT_GRP.append(new_group)
        
        flash(f"Group '{name}' created successfully!")
        return redirect(url_for('student_views.student_group_details_page'))
    
    candidates = [
        {'name': 'Daniel Roberts', 'student_id': '20240123', 'selected': False},
        {'name': 'Michael Johnson', 'student_id': '20231245', 'selected': True},
        {'name': 'Samantha Lewis', 'student_id': '20229876', 'selected': True},
        {'name': 'Christopher Brown', 'student_id': '20235678', 'selected': False},
        {'name': 'Ashley Williams', 'student_id': '20246789', 'selected': False},
        {'name': 'Emily Thompson', 'student_id': '20242345', 'selected': True},
        {'name': 'Brandon Phillips', 'student_id': '20238901', 'selected': False},
    ]
    return render_template(
        'student/create_group.html',
        active_page='create-group',
        title='Create Group',
        candidates=candidates,
    )


@student_views.route('/student/group-details', methods=['GET'])
def student_group_details_page():

    current_group = STUDENT_GRP[-1] if STUDENT_GRP else None
    display_members = []

    if current_group:
        for student_id in current_group['members']:
            match = next((s for s in STUDENT_DATA if s['student_id'] == student_id), None)
            if match:
                display_members.append(match)

    return render_template(
        'student/group_details.html',
        active_page='group-details',
        title='Group Details',
        status='Pending Confirmation',
        group=current_group,
        members=display_members
    )


@student_views.route('/student/lots', methods=['GET', 'POST'])
def student_lots_page():
    if request.method == 'POST':
        action = request.form.get('action') # 
        lot_id = request.form.get('lot_id')
        
        # Capture data from form
        rfp_data = {
            'lot_id': lot_id,
            'screen': request.form.get('screen'),
            'os': request.form.get('os'),
            'cpu': request.form.get('cpu'),
            'ram': request.form.get('ram'),
            'storage': request.form.get('storage'),
            'graphics': request.form.get('graphics'),
            'peripherals': request.form.get('peripherals'),
            'features': request.form.get('features'),
            'io': request.form.get('io'),
            'status': 'Submitted' if action == 'submit' else 'Draft'
        }
        
        #  Update if exists, else Append
        existing_index = next((i for i, r in enumerate(STUDENT_RFPS) if r['lot_id'] == lot_id), None)
        
        if existing_index is not None:
            STUDENT_RFPS[existing_index] = rfp_data
        else:
            STUDENT_RFPS.append(rfp_data)
        
        #  Success Message
        if action == 'submit':
            flash(f"RFP for Lot {lot_id} has been submitted!", "success")
        else:
            flash(f"Draft for Lot {lot_id} saved successfully.", "info")
            
        return redirect(url_for('student_views.student_lots_page', selected_lot=lot_id))

    # GET req info
    selected_lot_id = request.args.get('selected_lot', '1')
    current_lot = next((l for l in ASSIGNED_LOTS if str(l['id']) == selected_lot_id), ASSIGNED_LOTS[0])
    
    # Looks for existing rfp
    existing_rfp = next((r for r in STUDENT_RFPS if r['lot_id'] == selected_lot_id), None)

    return render_template(
        'student/client_lots.html', 
        active_page='lots',
        title='Assigned Lots & RFPs',
        lots=ASSIGNED_LOTS,
        current_lot=current_lot,
        existing_rfp=existing_rfp
    )
         
    
@student_views.route('/student/client-view-bids', methods=['GET'])
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