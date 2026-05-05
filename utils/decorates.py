# will contains all the decorator
def log_action(func):
    def wrapper(*args, **kwargs):
        print(f"[INFO] Running {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
