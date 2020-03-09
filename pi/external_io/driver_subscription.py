import locator

driver = locator.get_driver()

dependency = ['driver']
def callback(driver_data):
    driver.set_rudder(driver_data['rudder'])
    driver.set_sail(driver_data['sail'])

driver_subscription = (callback, dependency)