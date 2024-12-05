from flask import render_template, Blueprint
main_bp = Blueprint('main_controller', __name__)

@main_bp.route('/')
def home_func():
    return render_template('home.html')

@main_bp.route('/graphs')
def graphs_func():
    return render_template('graphs.html')

@main_bp.route('/live')
def live_func():
    return render_template('live.html')

@main_bp.route('/notifications')
def notifications_func():
    return render_template('notifications.html')

@main_bp.route('/settings')
def settings_func():
    return render_template('settings.html')