from flask import Flask, request
from flask_cors import CORS, cross_origin
import json

def create_app(driver, helmsman=None):
    app = Flask(__name__)
    cors = CORS(app)
    app.config['CORS_HEADRS'] = 'Content-Type'

    @app.route('/status')
    @cross_origin()
    def status():
        return json.dumps(driver.status())
    

    @app.route('/rudder', methods=['PUT'])
    @cross_origin()
    def rudder():
        angle = int(request.args.get('angle'))
        driver.set_rudder(angle)
        return 'rudder set to {}'.format(angle)


    @app.route('/sail', methods=['PUT'])
    @cross_origin()
    def sail():
        angle = int(request.args.get('angle'))
        driver.set_sail(angle)
        return 'sail set to {}'.format(angle)

    return app