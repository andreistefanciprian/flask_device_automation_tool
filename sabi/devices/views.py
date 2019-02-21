from flask import Blueprint, render_template, redirect, url_for, request
from sabi import db
from sabi.models import Device
from sabi.devices.forms import AddForm, DelForm, UpdateForm
from sqlalchemy.exc import IntegrityError

import os

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
        # Other Db errors to be added here
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


# Delete Records separate page
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

# Delete records
@devices_blueprint.route('/<int:device_id>/delete', methods=['POST'])
def delete_device(device_id):
    device_id = Device.query.get_or_404(device_id)
    db.session.delete(device_id)
    db.session.commit()
    return redirect(url_for('devices.list'))

# Update records
@devices_blueprint.route('/<int:device_id>/update', methods=['GET', 'POST'])
def update(device_id):

    device = Device.query.get_or_404(device_id)

    form = UpdateForm()

    if form.validate_on_submit():
        device.hostname = form.hostname.data
        device.nasid = form.nasid.data
        device.ip = form.ip.data
        device.gateway = form.gateway.data
        device.wan = form.wan.data
        device.location = form.location.data

        db.session.commit()

        return redirect(url_for('devices.list', device_id=device.id))

    elif request.method == 'GET':
        form.hostname.data = device.hostname
        form.nasid.data = device.nasid
        form.ip.data = device.ip
        form.gateway.data = device.gateway
        form.wan.data = device.wan
        form.location.data = device.location
    return render_template('update.html',form=form)

# Show Status
@devices_blueprint.route('/<int:device_id>/status', methods=['GET', 'POST'])
def ops_status(device_id):

    device = Device.query.get_or_404(device_id)

    device_wan = device.wan
    device_hostname = device.hostname
    device_nasid = device.nasid
    device_location = device.location

    # Device commands (to be optimized with dictionaries via python and jinja + API/paramiko)
    export_out = os.popen(f"sshpass -p 'Simpl3Passw0rd' ssh -o StrictHostKeyChecking=no admin@{device.wan} 'export'").read()
    file_out = os.popen(f"sshpass -p 'Simpl3Passw0rd' ssh -o StrictHostKeyChecking=no admin@{device.wan} 'file print'").read()
    system_routerboard_out  = os.popen(f"sshpass -p 'Simpl3Passw0rd' ssh -o StrictHostKeyChecking=no admin@{device.wan} 'system routerboard print'").read()
    system_package_out  = os.popen(f"sshpass -p 'Simpl3Passw0rd' ssh -o StrictHostKeyChecking=no admin@{device.wan} 'system package print'").read()
    ip_route_out  = os.popen(f"sshpass -p 'Simpl3Passw0rd' ssh -o StrictHostKeyChecking=no admin@{device.wan} 'ip route print'").read()

    return render_template('ops_status.html',
        device_wan=device_wan,
        device_hostname=device_hostname,
        device_nasid=device_nasid,
        device_location=device_location,
        export_out=export_out,
        file_out=file_out,
        system_routerboard_out=system_routerboard_out,
        system_package_out=system_package_out,
        ip_route_out=ip_route_out)


# Build config

from sabi.devices.device_ops import build_config

@devices_blueprint.route('/<int:device_id>/build_config', methods=['GET', 'POST'])
def ops_build_config(device_id):

    device = Device.query.get_or_404(device_id)

    config_template = "/tmp/mikrotik_config.rsc" # config template file path can also be specified in the db when device of this type is instantiated
    device_wan = device.wan
    device_hostname = device.hostname
    device_gateway = device.gateway

    cfg_output = build_config(config_template, VHOSTNAME=device_hostname, VMKTWANIP=device_wan, VMKTWANGW=device_gateway)

    return render_template('ops_config.html',
        device_wan=device_wan,
        device_hostname=device_hostname,
        device_gateway=device_gateway,
        cfg_output=cfg_output)
