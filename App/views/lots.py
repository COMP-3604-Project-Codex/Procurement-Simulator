from flask import render_template, request, redirect, url_for, Blueprint

admin_lots_views = Blueprint('admin_lots_views', __name__, template_folder='../templates/admin')

# Dummy data for demonstration
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

def get_lot_by_id(lot_id):
    return next((lot for lot in LOTS if lot['id'] == lot_id), None)

@admin_lots_views.route('/admin/lots', methods=['GET'])
def admin_manage_lots():
    return render_template('admin/manage_lots.html', title='Manage Lots', lots=LOTS)

@admin_lots_views.route('/admin/lots/add', methods=['POST'])
def admin_add_lot():
    lab_type = request.form.get('lab_type')
    lab_size = request.form.get('lab_size')
    budget = request.form.get('budget')
    new_lot = {
        'id': len(LOTS) + 1,
        'lab_type': lab_type,
        'lab_size': lab_size,
        'budget': budget
    }
    LOTS.append(new_lot)
    return redirect(url_for('admin_lots_views.admin_manage_lots'))

@admin_lots_views.route('/admin/lots/<int:lot_id>/edit', methods=['POST'])
def admin_edit_lot(lot_id):
    lot = get_lot_by_id(lot_id)
    if lot:
        lot['lab_type'] = request.form.get('lab_type')
        lot['lab_size'] = request.form.get('lab_size')
        lot['budget'] = request.form.get('budget')
    return redirect(url_for('admin_lots_views.admin_manage_lots'))

@admin_lots_views.route('/admin/lots/<int:lot_id>/remove', methods=['POST'])
def admin_remove_lot(lot_id):
    global LOTS
    LOTS = [lot for lot in LOTS if lot['id'] != lot_id]
    return redirect(url_for('admin_lots_views.admin_manage_lots'))
