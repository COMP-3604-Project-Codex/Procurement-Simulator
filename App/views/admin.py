from flask_admin.contrib.sqla import ModelView
import io
from functools import wraps
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies
from flask_admin import Admin as FlaskAdmin
from flask import flash, redirect, url_for, request, Blueprint, render_template, send_file
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

    flash(f"Lot {lot_id} removed successfully", "success")
    return redirect(url_for('admin_views.admin_manage_lots'))

# ─── Bid Routes ───────────────────────────────────────────────────────────────

@admin_views.route('/admin/manage-bids')
@admin_required
def admin_manage_bids():

    groups = db.session.scalars(
        db.select(Group)
    ).all()

    GROUPS = []

    for group in groups:
        data = {}

        data["id"] = group.id
        data["name"] = group.groupName

        students = db.session.scalars(
            db.select(StudentGroup)
            .filter_by(groupID=group.id)
            .order_by(StudentGroup.studentID)
        ).all()

        members = []
        for student in students:
            innerData = {}
            student = get_student(student.studentID)

            innerData["name"] = student.name
            innerData["id"] = student.id
            members.append(innerData)

        data["members"] = members

        lots = []

        lotObjs = db.session.scalars(
            db.select(Lot)
            .join(LotGroup, LotGroup.lotID == Lot.id)
            .filter(LotGroup.groupID == group.id)
        ).all()

        for lotObj in lotObjs:
            lots.append(lotObj.id)

        data["lots"] = lots

        bids = []

        bidObjs = db.session.scalars(
            db.select(Bid)
            .filter_by(sourceGroupID=group.id)
        )

        for bidObj in bidObjs:
            bids.append(bidObj)

        data["bids"] = bids

        GROUPS.append(data)

    return render_template(
        'admin/manage_bids.html',
        bid_groups=GROUPS,
        title='Manage Bids',
        active_page='bids'
    )

@admin_views.route('/admin/manage-bids/group/<int:group_id>')
@admin_required
def admin_view_group_bids(group_id):

    groupJson = {}

    group = get_group(group_id)

    if not group:
        return redirect(url_for('admin_views.admin_manage_bids'))

    groupJson["id"] = group.id
    groupJson["name"] = group.groupName

    students = db.session.scalars(
        db.select(StudentGroup)
        .filter_by(groupID=group.id)
        .order_by(StudentGroup.studentID)
    ).all()

    members = []
    for student in students:
        innerData = {}
        student = get_student(student.studentID)

        innerData["name"] = student.name
        innerData["id"] = student.id
        members.append(innerData)

    groupJson["members"] = members

    lots = []

    lotObjs = db.session.scalars(
        db.select(Lot)
        .join(LotGroup, LotGroup.lotID == Lot.id)
        .filter(LotGroup.groupID == group.id)
    ).all()

    for lotObj in lotObjs:
        lots.append(lotObj.id)

    groupJson["lots"] = lots

    bids = []

    bidObjs = db.session.scalars(
        db.select(Bid)
        .filter_by(sourceGroupID=group.id)
    )

    for bidObj in bidObjs:
        bidJson = {}

        toGroup = get_group(bidObj.recipientGroupID)
        toLot = get_lot(bidObj.lotID)

        bidJson["to_group_name"] = toGroup.groupName
        bidJson["timestamp"] = bidObj.timestamp
        bidJson["to_lot_id"] = toLot.id
        bidJson["to_lot_name"] = toLot.labType
        bidJson["id"] = bidObj.id
        bidJson["pdf"] = bidObj.bidDocument
        bidJson["filename"] = bidObj.bidDocumentName
        bids.append(bidJson)

    groupJson["bids"] = bids

    return render_template(
        'admin/group_bids.html',
        group=groupJson,
        title=f"Bids Placed By {groupJson['name']}",
        active_page='bids'
    )

@admin_views.route('/admin/view-bid/<int:group_id>/<int:bid_id>')
def admin_view_bid_document(group_id, bid_id):
    bid = get_bid(bid_id)

    return send_file(
        io.BytesIO(bid.bidDocument),
        download_name=bid.bidDocumentName,
        mimetype='application/pdf'
    )

@admin_views.route('/admin/manage-bids/group/<int:group_id>/bid/<int:bid_id>/remove', methods=['POST'])
@admin_required
def admin_remove_bid(group_id, bid_id):
    remove_bid(bid_id)
    flash("Bid removed successfully", "success")
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
def admin_remove_group(group_id):
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

        group = get_group(entry.groupID)

        lot = get_lot(entry.lotID)

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

        group = get_group(entry.groupID)

        lot = get_lot(entry.lotID)

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

    evaluations = db.session.scalars(
        db.select(Evaluation)
        .filter_by(status="selected")
    ).all()

    evaluation_groups = []

    for evaluation in evaluations:
        data = {}

        data["id"] = evaluation.id

        group = get_group(evaluation.sourceGroupID)
        data["name"] = group.groupName

        group = get_group(evaluation.recipientGroupID)
        data["to_group_name"] = group.groupName

        data["lotID"] = evaluation.lotID

        lot = get_lot(evaluation.lotID)
        data["labType"] = lot.labType
        data["timestamp"] = evaluation.timestamp.strftime('%#m/%#d/%Y, %#I:%M%p').lower()

        data["specsMet"] = evaluation.specsMet
        data["professionalism"] = evaluation.professionalism
        data["presentation"] = evaluation.presentation
        data["budgetScore"] = evaluation.budget
        data["overall"] = evaluation.overallScore 

        evaluation_groups.append(data)

    return render_template('admin/manage_evaluations.html',
        evaluation_groups=evaluation_groups,
        title='Manage Evaluations',
        active_page='evaluations'
    )

@admin_views.route('/admin/manage-evaluations/<int:evaluationID>/remove', methods=['POST'])
@admin_required
def admin_remove_evaluation(evaluationID):
    
    evaluation = get_evaluation(evaluationID)

    evaluation.status = "draft"

    db.session.commit()
    
    flash("Evaluation removed successfully", "success")
    return redirect(url_for('admin_views.admin_manage_evaluations'))