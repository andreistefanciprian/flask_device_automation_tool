from flask import render_template,request,Blueprint

core_blueprint = Blueprint('core',__name__)

@core_blueprint.route('/')
def index():
    return render_template('home.html')

'''
@core_blueprint.route('/info')
def info():
    return render_template('info.html')
'''
