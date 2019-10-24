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

        try:
            driver.set_sail(data['sail_angle'])
        except ValueError:
            return 'Invalid sail angle'
        try:
            driver.set_rudder(data['rudder_angle'])
        except ValueError:
            return 'Invalid rudder angle'

        return 'Set rudder to {} and sail to {}'.format(data['rudder_angle'], data['sail_angle'])

    @app.route('/helmsman', methods=['PUT'])
    @cross_origin()
    def rudder_controller():
        data = request.json
        helmsman.rudder_controller_enabled = data['rudder_controller']['enabled']
        helmsman.sail_controller_enabled = data['sail_controller']['enabled']
        return 'Rudder Controller is {}\n Sail Controller is {}'.format(helmsman.rudder_controller_enabled, helmsman.sail_controller_enabled)

    @app.route('/shutdown', methods=['PUT'])
    @cross_origin()
    def shutdown():
        driver.close()
        request.environ.get('werkzeug.server.shutdown')()
        print('Shutting down server')
        return 'Server shut down'

    return app
