from flask_login import login_required
from flask import render_template, Blueprint

main_bp = Blueprint('main_controller', __name__)

@main_bp.route('/')
@login_required
def home_func():
    return render_template('home.html', title="Home")

@main_bp.route('/graphs')
@login_required
def graphs_func():
    return render_template('graphs.html', title="Graphs")

@main_bp.route('/live')
@login_required
def live_func():
    return render_template('live.html', title="Live")

@main_bp.route('/notifications')
@login_required
def notifications_func():
    return render_template('notifications.html', title="Notifications")

@main_bp.route('/settings')
@login_required
def settings_func():
    return render_template('settings.html', title="Settings")
