from flask import Blueprint, flash, request, redirect, render_template, url_for


student_views = Blueprint('student_views', __name__, template_folder='../templates')

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
        group=current_group,
        members=display_members 
    )
