from flask import Blueprint, render_template, redirect, url_for
from sabi import db
from sabi.models import Device
from sabi.devices.forms import AddForm, DelForm
from sqlalchemy.exc import IntegrityError

devices_blueprint = Blueprint('devices', __name__, template_folder = 'templates')



@devices_blueprint.route('/add', methods=['GET', 'POST'])
def add():
    form = AddForm()

    if form.validate_on_submit():
        hostname = form.hostname.data
        nasid = form.nasid.data
        ip = form.ip.data
        gateway = form.gateway.data
        wan = form.wan.data
        location = form.location.data

        # Add new Device to database
        try:
            new_device = Device(hostname,nasid,ip,gateway,wan,location)
            db.session.add(new_device)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return '<h1>This member already exists!</h1>'
        return redirect(url_for('devices.list'))

    return render_template('add.html',form=form)


@devices_blueprint.route('/list')
def list():
    # Grab a list of Devices from database.
    devices = Device.query.all()
    return render_template('list.html', devices=devices)



@devices_blueprint.route('/delete', methods=['GET', 'POST'])
def delete():

    form = DelForm()

    if form.validate_on_submit():
        id = form.id.data
        device = Device.query.get(id)
        db.session.delete(device)
        db.session.commit()

        return redirect(url_for('devices.list'))
    return render_template('delete.html',form=form)
