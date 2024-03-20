import traceback


def log_and_raise_exception(msg):
    print(f'{msg}')
    traceback.print_exc()
    raise Exception(msg)
