from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


#TODO validate register id is in form register:key and register is
# one we know about

class CheckForm(Form):
    register_id = StringField('Register ID', validators=[DataRequired()])
