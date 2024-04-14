import logging

from flask import Flask
from flask_admin import Admin
from flask_basicauth import BasicAuth

from configuration import DB_URL, ADMIN_PANEL_SECRET_KEY, ADMIN_PANEL_BASIC_AUTH_PASSWORD, \
    ADMIN_PANEL_BASIC_AUTH_USERNAME

from database.base import current_session
from database.models.user import User, UserView
from database.models.region import Region, RegionView
from database.models.user_region import UserRegion, UserRegionView
from database.models.evacuation_requests import EvacuationRequestView, EvacuationRequest
from database.models.request import Request, RequestView

app = Flask(__name__)
logger = logging.getLogger(__name__)

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(app, name='Хелпарик', template_mode='bootstrap3', url='/extra-wh-2020/')
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SECRET_KEY'] = ADMIN_PANEL_SECRET_KEY
app.config['BASIC_AUTH_USERNAME'] = ADMIN_PANEL_BASIC_AUTH_USERNAME
app.config['BASIC_AUTH_PASSWORD'] = ADMIN_PANEL_BASIC_AUTH_PASSWORD
app.config['BASIC_AUTH_FORCE'] = True


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


basic_auth = BasicAuth(app)

# admin.add_view(UserView(User, current_session))
# admin.add_view(RegionView(Region, current_session))
# admin.add_view(UserRegionView(UserRegion, current_session))
admin.add_view(EvacuationRequestView(EvacuationRequest, current_session))
admin.add_view(RequestView(Request, current_session))

if __name__ == '__main__':
    from gevent.pywsgi import WSGIServer

    logger.error("Starting admin panel")
    http_server = WSGIServer(('', 4000), app)
    logger.error("Http server configured")
    http_server.serve_forever()
