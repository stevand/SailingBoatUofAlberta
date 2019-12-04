import threading

def exec(locator):
    """
    Begins a flask server in a deamon thread.
    Returns is_done method, which will always return false.
    """
    server_runnable = locator.get_server_runnable()
    thread = threading.Thread(target=server_runnable, daemon=True)
    thread.start()

    blocking = False

    def is_done():
        # server runs indefinitely
        return False

    def cleanup():
        pass

    return blocking, is_done, cleanup