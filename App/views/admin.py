from flask_admin.contrib.sqla import ModelView
from functools import wraps
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies
from flask_admin import Admin as FlaskAdmin
from flask import flash, redirect, url_for, request, Blueprint, render_template
from App.database import db
from App.models import User, Admin, Student, Group, StudentGroup, Lot, LotGroup, Bid, Evaluation, RFP
from App.controllers import *

class AdminView(ModelView):
    @jwt_required()
    def is_accessible(self):
        return current_user is not None

    def inaccessible_callback(self, name, **kwargs):
        flash("Login to access admin", "info")
        return redirect(url_for('index_page', next=request.url))

def setup_admin(app):
    admin = FlaskAdmin(app, name='FlaskMVC', template_mode='bootstrap3')
    admin.add_view(AdminView(User, db.session))

admin_views = Blueprint('admin_views', __name__, template_folder='../templates/admin')

def admin_required(f):
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            flash("You are logged in as a student and therefore cannot access admin page", "failed")
            return redirect(url_for('index_views.index_page'))
        return f(*args, **kwargs)
    return decorated_function

# ─── Dummy Data ───────────────────────────────────────────────────────────────

LOTS = [
    {
        'id': 1,
        'lab_type': 'GIS Lab',
        'lab_size': 'Medium, capable of having 20 machines',
        'budget': 160000
    },
    {
        'id': 2,
        'lab_type': 'Government Office Lab',
        'lab_size': 'Small, capable of having 12 machines',
        'budget': 110000
    }
]

GROUPS = [
    {
        'id': 1,
        'name': 'NovaCore',
        'members': [
            {'name': 'Aisha Mohammed', 'id': '20231278'},
            {'name': 'Jamal Baptiste', 'id': '20236754'},
            {'name': 'Denzel Johnson', 'id': '20939438'}
        ],
        'lots': [8, 4],
        'bids': []
    },
    {
        'id': 2,
        'name': 'TechSphere',
        'members': [
            {'name': 'Daniel Roberts', 'id': '20240123'},
            {'name': 'Priya Singh', 'id': '20249811'},
            {'name': 'Marcus Charles', 'id': '20235562'}
        ],
        'lots': [3, 6],
        'bids': [
            {'id': 1, 'to_group_id': 1, 'to_group_name': 'NovaCore', 'timestamp': '11/5/2025, 6:56pm'}
        ]
    },
    {
        'id': 3,
        'name': 'CodeMatrix',
        'members': [
            {'name': 'Leah Thomas', 'id': '20238914'},
            {'name': 'Ryan Ali', 'id': '20227654'},
            {'name': 'Samantha Pierre', 'id': '20241209'}
        ],
        'lots': [2, 5],
        'bids': [
            {'id': 2, 'to_group_id': 2, 'to_group_name': 'TechSphere', 'timestamp': '11/5/2025, 6:46pm'},
            {'id': 3, 'to_group_id': 1, 'to_group_name': 'NovaCore', 'timestamp': '11/5/2025, 6:50pm'}
        ]
    },
    {
        'id': 4,
        'name': 'DataWave',
        'members': [],
        'lots': [],
        'bids': [
            {'id': 4, 'to_group_id': 5, 'to_group_name': 'CyberFusion', 'timestamp': '11/5/2025, 6:46pm'},
            {'id': 5, 'to_group_id': 2, 'to_group_name': 'TechSphere', 'timestamp': '11/5/2025, 6:56pm'}
        ]
    },
    {
        'id': 5,
        'name': 'CyberFusion',
        'members': [],
        'lots': [],
        'bids': [
            {'id': 6, 'to_group_id': 1, 'to_group_name': 'NovaCore', 'timestamp': '11/5/2025, 7:00pm'}
        ]
    },
    {
        'id': 6,
        'name': 'LogicForge',
        'members': [],
        'lots': [],
        'bids': [
            {'id': 7, 'to_group_id': 2, 'to_group_name': 'TechSphere', 'timestamp': '11/5/2025, 7:10pm'},
            {'id': 8, 'to_group_id': 3, 'to_group_name': 'CodeMatrix', 'timestamp': '11/5/2025, 7:15pm'}
        ]
    }
]

GROUP_REQUESTS = [
    {
        'id': 1,
        'name': 'NovaCore',
        'members': [
            {'name': 'Aisha Mohammed', 'id': '20231278'},
            {'name': 'Jamal Baptiste', 'id': '20236754'},
            {'name': 'Denzel Johnson', 'id': '20939438'}
        ]
    },
    {
        'id': 3,
        'name': 'TechSphere',
        'members': [
            {'name': 'Daniel Roberts', 'id': '20240123'},
            {'name': 'Priya Singh', 'id': '20249811'},
            {'name': 'Marcus Charles', 'id': '20235562'}
        ]
    },
    {
        'id': 2,
        'name': 'CodeMatrix',
        'members': [
            {'name': 'Leah Thomas', 'id': '20238914'},
            {'name': 'Ryan Ali', 'id': '20227654'},
            {'name': 'Samantha Pierre', 'id': '20241209'}
        ]
    }
]

# ─── Helper Functions ─────────────────────────────────────────────────────────

def get_lot_by_id(lot_id):
    return next((lot for lot in LOTS if lot['id'] == lot_id), None)

# ─── Lot Routes ───────────────────────────────────────────────────────────────

@admin_views.route('/admin/lots', methods=['GET'])
@admin_required
def admin_manage_lots():
    lots = db.session.scalars(
        db.select(Lot)
    ).all()

    return render_template('admin/manage_lots.html', title='Manage Lots', lots=lots)

@admin_views.route('/admin/lots/add', methods=['POST'])
@admin_required
def admin_add_lot():
    lab_type = request.form.get('lab_type')
    lab_size = request.form.get('lab_size')
    budget = request.form.get('budget')
    
    create_lot(lab_type, lab_size, budget)

    return redirect(url_for('admin_views.admin_manage_lots'))

@admin_views.route('/admin/lots/<int:lot_id>/edit', methods=['POST'])
@admin_required
def admin_edit_lot(lot_id):
    labType = request.form.get('lab_type')
    labSize = request.form.get('lab_size')
    budget = request.form.get('budget')
    
    edit_lot(lot_id, labType, labSize, budget)

    return redirect(url_for('admin_views.admin_manage_lots'))

@admin_views.route('/admin/lots/<int:lot_id>/remove', methods=['POST'])
@admin_required
def admin_remove_lot(lot_id):
    
    remove_lot(lot_id)

    return redirect(url_for('admin_views.admin_manage_lots'))

# ─── Bid Routes ───────────────────────────────────────────────────────────────

@admin_views.route('/admin/manage-bids')
@admin_required
def admin_manage_bids():
    return render_template(
        'admin/manage_bids.html',
        bid_groups=GROUPS,
        title='Manage Bids',
        active_page='bids'
    )

@admin_views.route('/admin/manage-bids/group/<int:group_id>')
@admin_required
def admin_view_group_bids(group_id):
    group = next((g for g in GROUPS if g['id'] == group_id), None)
    if not group:
        return redirect(url_for('admin_views.admin_manage_bids'))
    return render_template(
        'admin/group_bids.html',
        group=group,
        title=f"Bids Placed By G{group['id']} {group['name']}",
        active_page='bids'
    )

@admin_views.route('/admin/manage-bids/group/<int:group_id>/bid/<int:bid_id>')
@admin_required
def admin_view_bid_document(group_id, bid_id):
    return f"Bid document for group {group_id}, bid {bid_id}"

@admin_views.route('/admin/manage-bids/group/<int:group_id>/bid/<int:bid_id>/remove', methods=['POST'])
@admin_required
def admin_remove_bid(group_id, bid_id):
    return redirect(url_for('admin_views.admin_view_group_bids', group_id=group_id))

# ─── Group Routes ─────────────────────────────────────────────────────────────

@admin_views.route('/admin/manage-groups')
@admin_required
def admin_manage_groups():

    GROUPS = []
    GROUP_REQUESTS = []

    groups = db.session.scalars(
        db.select(Group)
    ).all()

    for group in groups:
        dic = {}
        dic["id"] = group.id
        dic["name"] = group.groupName

        students = db.session.scalars(
            db.select(Student)
            .join(StudentGroup, Student.id == StudentGroup.studentID)
            .filter(StudentGroup.groupID == group.id)
        ).all()

        members = []
        for student in students:
            member = {}
            member["name"] = student.name
            member["id"] = student.username
            members.append(member)

        dic["members"] = members

        if group.status == "requested":
            GROUP_REQUESTS.append(dic)
        else:
            entries = db.session.scalars(
                db.select(LotGroup)
                .filter_by(groupID=group.id)
            ).all()

            lots = []
            for entry in entries:
                lots.append(entry.lotID)

            dic["lots"] = lots

            GROUPS.append(dic)

    LOTS = db.session.scalars(
        db.select(Lot)
    ).all()

    return render_template('admin/manage_groups.html',
                         tab='requests',
                         title='Manage Groups',
                         group_requests=GROUP_REQUESTS,
                         groups=GROUPS,
                         lots=LOTS,
                         active_page='groups')


@admin_views.route('/admin/groups/<int:group_id>/remove', methods=['POST'])
@admin_required
def admin_assign_lots(group_id):
    group = get_group(group_id)

    if group:
        removed = remove_group(group_id)
        flash("Group Removed", "success")

    return redirect(url_for('admin_views.admin_manage_groups'))

@admin_views.route('/admin/group-requests/<int:group_id>/approve', methods=['POST'])
@admin_required
def admin_approve_group(group_id):
    return redirect(url_for('admin_views.admin_manage_groups'))

@admin_views.route('/admin/group-requests/<int:group_id>/decline', methods=['POST'])
@admin_required
def admin_decline_group(group_id):
    group = get_group(group_id)

    if group:
        removed = remove_group(group_id)
        flash("Group Rejected", "success")

    return redirect(url_for('admin_views.admin_manage_groups'))

@admin_views.route('/admin/group-requests/<int:group_id>/approve-and-assign', methods=['POST'])
@admin_required
def admin_approve_and_assign_group(group_id):
    group = get_group(group_id)
    if group:
        already_has_lots = db.session.scalars(
            db.select(LotGroup)
            .filter_by(groupID=group_id)
        ).first()

        if already_has_lots:
            flash("Lots have already been assigned for this group", "failed")
            return redirect(url_for('admin_views.admin_manage_groups'))

        lot1ID = request.form.get('lot1')
        lot2ID = request.form.get('lot2')

        if lot1ID == lot2ID:
            flash("Lot1 and Lot2 must be different lots", "failed")
            return redirect(url_for('admin_views.admin_manage_groups'))
        
        lot1 = False
        lot2 = False

        lot_check = db.session.scalars(
            db.select(LotGroup)
            .filter_by(lotID=lot1ID)
        ).first()

        if lot_check:
            lot1 = True

        lot_check = db.session.scalars(
            db.select(LotGroup)
            .filter_by(lotID=lot2ID)
        ).first()

        if lot_check:
            lot2 = True

        if lot1 and lot2:
            flash("Lot1 and Lot2 have already been assigned", "failed")
            return redirect(url_for('admin_views.admin_manage_groups'))
        elif lot1:
            flash("Lot1 has already been assigned", "failed")
            return redirect(url_for('admin_views.admin_manage_groups'))
        elif lot2:
            flash("Lot2 has already been assigned", "failed")
            return redirect(url_for('admin_views.admin_manage_groups'))

        add_lotGroup(lot1ID, group_id)
        add_lotGroup(lot2ID, group_id)

        approve_group(group_id)

    flash("successfully approved group", "success")
    return redirect(url_for('admin_views.admin_manage_groups'))

# ─── RFP Routes ───────────────────────────────────────────────────────────────

@admin_views.route('/admin/manage-rfps', methods=['GET', 'POST'])
@admin_required
def admin_manage_rfps():
    if request.method == 'POST':
        action = request.form.get('action')
        lotID = request.form.get('lotID')
        groupID = request.form.get('groupID')

        if action == "approve":
            approve_rfp(groupID, lotID)
            flash(f'RFP for Lot {lotID} approved successfully', "success")

        elif action == "reject":
            removed = remove_rfp(groupID, lotID)
            flash(f'RFP for Lot {lotID} rejected successfully', "success")

        elif action == "remove":
            removed = remove_rfp(groupID, lotID)
            flash(f'RFP for Lot {lotID} removed successfully', "success")

        return redirect(url_for('admin_views.admin_manage_rfps'))

    rfp_requests = db.session.scalars(
        db.select(RFP)
        .filter_by(status="requested")
    ).all()
    
    rfp_gallery = db.session.scalars(
        db.select(RFP)
        .filter_by(status="approved")
    ).all()

    rfp_requests_json = []
    rfp_gallery_json = []

    for entry in rfp_requests:
        data = {}
        
        data["groupID"] = entry.groupID
        data["lotID"] = entry.lotID

        group = db.session.scalars(
            db.select(Group)
            .filter_by(id=entry.groupID)
        ).first()

        lot = db.session.scalars(
            db.select(Lot)
            .filter_by(id=entry.lotID)
        ).first()

        data["name"] = group.groupName
        data["Lot"] = lot.labType
        data["timestamp"] = entry.timestamp.strftime('%#m/%#d/%Y, %#I:%M%p').lower()
        data["deviceType"] = entry.deviceType
        data["resolution"] = entry.resolution
        data["os"] = entry.os
        data["cpu"] = entry.cpu
        data["ram"] = entry.ram
        data["drive"] = entry.drive
        data["gpu"] = entry.gpu
        data["io"] = entry.io
        data["peripherals"] = entry.peripherals
        data["features"] = entry.features

        rfp_requests_json.append(data)

    for entry in rfp_gallery:
        data = {}
        
        data["groupID"] = entry.groupID
        data["lotID"] = entry.lotID

        group = db.session.scalars(
            db.select(Group)
            .filter_by(id=entry.groupID)
        ).first()

        lot = db.session.scalars(
            db.select(Lot)
            .filter_by(id=entry.lotID)
        ).first()

        data["name"] = group.groupName
        data["Lot"] = lot.labType
        data["timestamp"] = entry.timestamp.strftime('%#m/%#d/%Y, %#I:%M%p').lower()
        data["deviceType"] = entry.deviceType
        data["resolution"] = entry.resolution
        data["os"] = entry.os
        data["cpu"] = entry.cpu
        data["ram"] = entry.ram
        data["drive"] = entry.drive
        data["gpu"] = entry.gpu
        data["io"] = entry.io
        data["peripherals"] = entry.peripherals
        data["features"] = entry.features

        rfp_gallery_json.append(data)

    return render_template('admin/manage_rfps.html',
        rfp_requests=rfp_requests_json,
        rfp_gallery=rfp_gallery_json,
        title='Manage RFPs',
        active_page='rfps')


# ─── Evaluation Routes ────────────────────────────────────────────────────────

@admin_views.route('/admin/manage-evaluations')
@admin_required
def admin_manage_evaluations():
    evaluation_groups = [
        {"id": 1, "name": "NovaCore", "timestamp": "11/5/2025, 6:46pm"},
        {"id": 2, "name": "TechSphere", "timestamp": "11/5/2025, 6:46pm"},
        {"id": 3, "name": "CodeMatrix", "timestamp": "11/6/2025, 12:06am"},
        {"id": 4, "name": "Datawave", "timestamp": "11/5/2025, 10:12pm"},
        {"id": 5, "name": "CyberFusion", "timestamp": "11/5/2025, 10:44pm"},
        {"id": 6, "name": "LogicForge", "timestamp": "11/5/2025, 10:44pm"},
    ]
    return render_template('admin/manage_evaluations.html',
        evaluation_groups=evaluation_groups,
        title='Manage Evaluations',
        active_page='evaluations'
    )