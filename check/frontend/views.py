from flask import (
    Blueprint,
    render_template,
    request,
    current_app,
    flash,
    abort,
    redirect,
    url_for
)

import requests

from check.frontend.forms import CheckForm

headers = {'Content-Type': 'application/json'}

frontend = Blueprint('frontend', __name__, template_folder='templates')


@frontend.route('/')
def index():
    form = CheckForm()
    return render_template('index.html', form=form)

@frontend.route('/check', methods=['POST'])
def check():
    form = CheckForm()
    if form.validate_on_submit():
        register, key = form.data['register_id'].split(':')
        try:
            url = _get_url(register, key)
            resp = requests.get(url, headers=headers)
            if resp.status_code == 200:
                #TODO get address data
                return render_template('check.html', entry=resp.json())
            else:
                message = "There was a problem checking the %s register" % register
                flash(message)
                abort(resp.status_code)
        except KeyError as e:
            message = "This application is not yet configured to check the %s register" % register
            flash(message)
            return redirect(url_for('.index'))
    else:
        return render_template('index.html', form=form)

def _get_url(register, key):
    config_name = register.replace('-','_').upper()
    reg_url = current_app.config[config_name]
    url = '%s/%s/%s.json' % (reg_url, register, key)
    return url
