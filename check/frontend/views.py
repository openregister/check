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


@frontend.route('/', methods=['GET', 'POST'])
def index():
    form = CheckForm()
    if form.validate_on_submit():
        try:
            register, key = form.data['register_id'].split(':')
            return redirect(url_for('frontend.check', register=register, key=key))
        except KeyError as e:
            message = "This application is not yet configured to check the %s register" % register
            flash(message)
            return redirect(url_for('.index'))

    return render_template('index.html', form=form)


@frontend.route('/check/<register>/<key>')
def check(register, key):
    try:
        url = _get_url(register, key)
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            entry = resp.json()
            address = _get_address(entry)
            return render_template('check.html', entry=entry, address=address)
        else:
            message = "There was a problem checking the %s register" % register
            flash(message)
            abort(resp.status_code)
    except KeyError as e:
        message = "This application is not yet configured to check the %sregister" % register
        flash(message)
    return redirect(url_for('.index'))


def _get_url(register, key):
    config_name = register.replace('-', '_').upper()
    reg_url = current_app.config[config_name]
    url = '%s/%s/%s.json' % (reg_url, register, key)
    return url


def _get_address(entry):
    address_key = entry['entry']['address']
    address_register_url = current_app.config['ADDRESS_REGISTER']
    url = '%s/address/%s.json' % (address_register_url, address_key)
    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return None
