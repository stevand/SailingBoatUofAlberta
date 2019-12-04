import sys
import locator
import routines.run_server as run_server

config_path = sys.argv[1]
locator.load_config(config_path)

goals = locator.get_config()['goals']

if 'run_server' in goals:
    run_server.exec(locator)
