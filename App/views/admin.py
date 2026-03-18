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

# Admin Manage Bids (Groups) page
@admin_views.route('/admin/manage-bids')
def admin_manage_bids():
    return render_template(
        'admin/manage_bids.html',
        bid_groups=GROUPS,
        title='Manage Bids',
        active_page='bids'
    )

# Admin Group Bids page (bids placed by a group)
@admin_views.route('/admin/manage-bids/group/<int:group_id>')
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

# Dummy endpoints for bid document and remove (not implemented)
@admin_views.route('/admin/manage-bids/group/<int:group_id>/bid/<int:bid_id>')
def admin_view_bid_document(group_id, bid_id):
    # Placeholder for bid document view
    return f"Bid document for group {group_id}, bid {bid_id}"

@admin_views.route('/admin/manage-bids/group/<int:group_id>/bid/<int:bid_id>/remove', methods=['POST'])
def admin_remove_bid(group_id, bid_id):
    # Placeholder for removing a bid
    return redirect(url_for('admin_views.admin_view_group_bids', group_id=group_id))

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
        return redirect(url_for('admin_views.admin_manage_groups'))
    return render_template('admin/assign_lots_modal.html', group=group, lots=LOTS)

@admin_views.route('/admin/group-requests/<int:group_id>/approve', methods=['POST'])
def admin_approve_group(group_id):
    # Here you would approve the group request in the database
    return redirect(url_for('admin_views.admin_manage_groups'))

@admin_views.route('/admin/group-requests/<int:group_id>/decline', methods=['POST'])
def admin_decline_group(group_id):
    # Here you would decline the group request in the database
    return redirect(url_for('admin_views.admin_manage_groups'))

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
    return render_template('admin/manage_groups.html', 
                         tab='requests', 
                         title='Manage Groups', 
                         group_requests=GROUP_REQUESTS, 
                         groups=GROUPS, 
                         lots=LOTS,
                         active_page='groups')


# Unified RFP management page with tab switching and modal preview
@admin_views.route('/admin/manage-rfps')
def admin_manage_rfps():
    rfp_requests = [
        {'id': 1, 'name': 'G5 JRS Technologies', 'timestamp': '11/5/2025, 11:32pm'},
        {'id': 2, 'name': 'G5 JRS Technologies', 'timestamp': '11/5/2025, 11:32pm'},
        {'id': 3, 'name': 'G5 JRS Technologies', 'timestamp': '11/5/2025, 11:32pm'},
        {'id': 4, 'name': 'G5 JRS Technologies', 'timestamp': '11/5/2025, 11:32pm'}
    ]
    rfp_gallery = [
        {'id': 1, 'name': 'G7 ANK Productions', 'timestamp': '11/5/2025, 6:46pm'},
        {'id': 2, 'name': 'G8 O(no)', 'timestamp': '11/6/2025, 12:06am'},
        {'id': 3, 'name': 'G1 NovaCore', 'timestamp': '11/5/2025, 10:44pm'}
    ]
    # Dummy RFP details for modal preview (could be dynamic in real app)
    rfp_details = {
        'type': 'Workstation/Laptop/Tablet',
        'screen_size': 'Screen Size & Resolution',
        'os': 'Mac/Windows/Android/IOS/Linux/Chromium',
        'cpu': 'Core and frequency range eg (quad-core @ 2.2 - 3.0 GHz)',
        'memory': 'DDR4/DDR5, 8-16GB',
        'hard_drive': 'HDD/SSD, 512GB to 1TB',
        'graphics': 'Integrated/Dedicated',
    }
    return render_template('admin/manage_rfps.html',
        rfp_requests=rfp_requests,
        rfp_gallery=rfp_gallery,
        rfp_details=rfp_details,
        title='Manage RFPs',
        active_page='rfps')