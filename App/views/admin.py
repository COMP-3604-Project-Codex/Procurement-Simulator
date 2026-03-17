from flask_admin.contrib.sqla import ModelView
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies
from flask_admin import Admin
from flask import flash, redirect, url_for, request, Blueprint, render_template
from App.database import db
from App.models import User

class AdminView(ModelView):

    @jwt_required()
    def is_accessible(self):
        return current_user is not None

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        flash("Login to access admin")
        return redirect(url_for('index_page', next=request.url))

def setup_admin(app):
    admin = Admin(app, name='FlaskMVC', template_mode='bootstrap3')
    admin.add_view(AdminView(User, db.session))

admin_views = Blueprint('admin_views', __name__, template_folder='../templates/admin')

# Dummy data for demonstration
GROUPS = [
    {
        'id': 1,
        'name': 'NovaCore',
        'members': [
            {'name': 'Aisha Mohammed', 'id': '20231278'},
            {'name': 'Jamal Baptiste', 'id': '20236754'},
            {'name': 'Denzel Johnson', 'id': '20939438'}
        ],
        'lots': [8, 4]
    },
    {
        'id': 2,
        'name': 'CodeMatrix',
        'members': [
            {'name': 'Leah Thomas', 'id': '20238914'},
            {'name': 'Ryan Ali', 'id': '20227654'},
            {'name': 'Samantha Pierre', 'id': '20241209'}
        ],
        'lots': [2, 5]
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

LOTS = [2, 4, 5, 8]

@admin_views.route('/admin/groups/<int:group_id>/assign-lots', methods=['GET', 'POST'])
def admin_assign_lots(group_id):
    group = next((g for g in GROUPS if g['id'] == group_id), None)
    if request.method == 'POST':
        # Here you would update the group's lots in the database
        lot1 = request.form.get('lot1')
        lot2 = request.form.get('lot2')
        group['lots'] = [int(lot1), int(lot2)]
        return redirect(url_for('admin_views.admin_groups'))
    return render_template('admin/assign_lots_modal.html', group=group, lots=LOTS)

@admin_views.route('/admin/group-requests/<int:group_id>/approve', methods=['POST'])
def admin_approve_group(group_id):
    # Here you would approve the group request in the database
    return redirect(url_for('admin_views.admin_group_requests'))

@admin_views.route('/admin/group-requests/<int:group_id>/decline', methods=['POST'])
def admin_decline_group(group_id):
    # Here you would decline the group request in the database
    return redirect(url_for('admin_views.admin_group_requests'))

@admin_views.route('/admin/group-requests/<int:group_id>/approve-and-assign', methods=['POST'])
def admin_approve_and_assign_group(group_id):
    request_item = next((r for r in GROUP_REQUESTS if r['id'] == group_id), None)
    if request_item:
        lot1 = request.form.get('lot1')
        lot2 = request.form.get('lot2')
        # Create new group
        new_group = {
            'id': len(GROUPS) + 1,
            'name': request_item['name'],
            'members': request_item['members'],
            'lots': [int(lot1), int(lot2)]
        }
        GROUPS.append(new_group)
        GROUP_REQUESTS.remove(request_item)
    return redirect(url_for('admin_views.admin_manage_groups'))

@admin_views.route('/admin/manage-groups')
def admin_manage_groups():
    return render_template('admin/manage_groups.html', tab='requests', group_requests=GROUP_REQUESTS, groups=GROUPS, lots=LOTS)