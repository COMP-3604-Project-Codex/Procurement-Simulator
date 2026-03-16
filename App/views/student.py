from flask import Blueprint, redirect, render_template, url_for


student_views = Blueprint('student_views', __name__, template_folder='../templates')


@student_views.route('/student', methods=['GET'])
def student_home_page():
    return redirect(url_for('student_views.student_create_group_page'))


@student_views.route('/student/create-group', methods=['GET'])
def student_create_group_page():
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
    members = [
        {'name': 'Michael Johnson', 'student_id': '20231245'},
        {'name': 'Samantha Lewis', 'student_id': '20229876'},
        {'name': 'Emily Thompson', 'student_id': '20242345'},
        {'name': 'Brandon Phillips', 'student_id': '20238901'},
    ]
    return render_template(
        'student/group_details.html',
        active_page='group-details',
        title='Group Details',
        status='Pending Confirmation',
        members=members,
    )