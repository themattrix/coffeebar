import collections

import flask
import flask_limiter.util
import wtforms

from . import drinks
from . import twilio_sms


app = flask.Flask(__name__)

limiter = flask_limiter.Limiter(
    app=app,
    key_func=flask_limiter.util.get_remote_address)

rate_limit_post = limiter.limit('5/day', exempt_when=lambda: flask.request.method != 'POST')


class OrderForm(wtforms.Form):
    customer = wtforms.StringField('customer', [wtforms.validators.InputRequired()])
    drink = wtforms.StringField('drink', [wtforms.validators.InputRequired()])

    # noinspection PyMethodMayBeStatic
    def validate_drink(self, field):
        if field.data not in drinks.DRINKS:
            raise wtforms.validators.ValidationError('Invalid drink')


@app.route('/', methods=('GET', 'POST'))
@rate_limit_post
def order():
    if flask.request.method == 'GET':
        return flask.render_template(
            'drinks.html',
            drinks=drinks.DRINKS,
            customer=flask.request.cookies.get('customer'))

    form = OrderForm(flask.request.form)

    if not form.validate():
        flask.abort(400)

    twilio_sms.TwilioMessage().send('{customer} has ordered {article} {singular}.'.format(
        customer=form.customer.data,
        article=drinks.DRINKS[form.drink.data]['article'],
        singular=drinks.DRINKS[form.drink.data]['singular']))

    response = flask.make_response(flask.redirect(flask.url_for('thanks')))
    set_previous_order(response=response, previous_order=Order(customer=form.customer.data, drink=form.drink.data))
    return response


@app.route('/thanks', methods=('GET',))
def thanks():
    previous_order = get_previous_order()

    return flask.render_template(
        'thanks.html',
        customer=previous_order.customer,
        drink_details=drinks.DRINKS[previous_order.drink])


@app.route('/cancel', methods=('GET', 'POST'))
@rate_limit_post
def cancel():
    previous_order = get_previous_order()

    if flask.request.method == 'POST':
        twilio_sms.TwilioMessage().send('CANCEL {singular} for {customer}.'.format(
            singular=drinks.DRINKS[previous_order.drink]['singular'],
            customer=previous_order.customer))

    return flask.render_template('cancel.html')


Order = collections.namedtuple('Order', 'customer drink')


class NoPreviousOrderException(Exception):
    """Raised if no previous order exists."""


def set_previous_order(response, previous_order):
    response.set_cookie('customer', previous_order.customer)
    response.set_cookie('drink', previous_order.drink)


def get_previous_order():
    previous_order = Order(
        customer=flask.request.cookies.get('customer'),
        drink=flask.request.cookies.get('drink'))

    if not previous_order.customer or not previous_order.drink:
        raise NoPreviousOrderException()

    return previous_order


# noinspection PyUnusedLocal
@app.errorhandler(NoPreviousOrderException)
def handle_no_previous_order(error):
    return flask.redirect(flask.url_for('order'))
