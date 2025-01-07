from flask import Flask



# Import the Blueprints
from asc_bulletin_api import asc_bulletin_bp
from trending_at_asc_api import asc_trending
from pastors_corner_api import pastor_corner
from staff_api import asc_staff
from top10api import asc_top_10
from mass_sacrement_api import asc_mass_and_sacraments

app = Flask(__name__)


# Register Blueprints
app.register_blueprint(asc_bulletin_bp, url_prefix='/asc_bulletin')
app.register_blueprint(asc_trending, url_prefix='/asc_trending')
app.register_blueprint(pastor_corner, url_prefix='/pastor_corner')
app.register_blueprint(asc_staff, url_prefix='/asc_staff')
app.register_blueprint(asc_top_10, url_prefix='/asc_top_10')
app.register_blueprint(asc_mass_and_sacraments, url_prefix='/asc_mass_and_sacraments')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
