from flask import Flask
import json

def create_app(driver, helmsman):
    app = Flask(__name__)

    @app.route('/status')
    def status():
        return json.dumps(driver.get_status())
    