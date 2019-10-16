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

    @app.route('/control', methods=['PUT'])
    @cross_origin()
    def control():
        data = request.json
        print(data)
        driver.set_sail(data['sail_angle'])
        driver.set_rudder(data['rudder_angle'])
        return 'Set rudder to {} and sail to {}'.format(data['rudder_angle'], data['sail_angle'])

    @app.route('/rudder_controller', methods=['PUT'])
    @cross_origin()
    def rudder_controller():
        data = request.json
        helmsman.rudder_controller_enabled = data['enabled']
        return 'Rudder enabled is {}'.format(data['enabled'])
    
    return app