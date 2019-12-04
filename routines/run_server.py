import threading

def exec(locator):
    server_runnable = locator.get_server_runnable()
    thread = threading.Thread(target=server_runnable)
    thread.start()

