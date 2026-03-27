from flask import Blueprint, flash, request, redirect, render_template, url_for


student_views = Blueprint('student_views', __name__, template_folder='../templates')

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
        # 1. Capture the data and include the lot_id from the form
        rfp_data = {
            'lot_id': request.form.get('lot_id'), # Important to know which lot this is for!
            'screen': request.form.get('screen'),
            'os': request.form.get('os'),
            'cpu': request.form.get('cpu'),
            'ram': request.form.get('ram'),
            'storage': request.form.get('storage'),
            'graphics': request.form.get('graphics'),
            'peripherals': request.form.get('peripherals'),
            'features': request.form.get('features'),
            'io': request.form.get('io')
        }
        
        # 2. Save it once
        STUDENT_RFPS.append(rfp_data)
        
        # 3. Flash the message and redirect
        flash(f"RFP for Lot {rfp_data['lot_id']} Submitted Successfully!", "success")
        return redirect(url_for('student_views.student_lots_page', selected_lot=rfp_data['lot_id']))

    # --- This part runs only for GET requests ---
    selected_lot_id = request.args.get('selected_lot', '1')
    current_lot = next((l for l in ASSIGNED_LOTS if str(l['id']) == selected_lot_id), ASSIGNED_LOTS[0])

    return render_template(
        'student/client_lots.html', 
        active_page='lots',
        title='Assigned Lots',
        lots=ASSIGNED_LOTS,
        current_lot=current_lot
    )
         
    
