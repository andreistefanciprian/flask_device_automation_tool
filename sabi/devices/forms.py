from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, IPAddress

class AddForm(FlaskForm):

    #validators = [DataRequired(message='This field is required!'), IPAddress(message='Must be an IP Address. Eg 192.168.1.11')

    hostname = StringField('Hostname of Device:',validators=[DataRequired(message='Hostname field is required!')])
    nasid = StringField('NASID of Device:',validators=[DataRequired()])
    ip = StringField('IP Address of Device:',validators=[IPAddress(message='IP Address of Device field has to be an IP Address. Eg: 192.168.0.11 or 1.1.1.1 127.162.10.1, etc')])
    gateway = StringField('Gateway of Device:',validators=[DataRequired()])
    wan = StringField('WAN of Device:',validators=[DataRequired()])
    location = StringField('Location of Device:',validators=[DataRequired()])
    submit = SubmitField('Add Device',validators=[DataRequired()])

class DelForm(FlaskForm):

    id = IntegerField('Id Number of Device to Remove:')
    submit = SubmitField('Remove Device')



