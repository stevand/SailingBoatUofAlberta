import locator

driver = locator.get_driver()

dependency = ['driver']
def callback(driver_data):
    if 'rudder' in driver_data:
        driver.set_rudder(driver_data['rudder'])
    if 'sail' in driver_data:
        driver.set_sail(driver_data['sail'])

driver_subscription = (callback, dependency)