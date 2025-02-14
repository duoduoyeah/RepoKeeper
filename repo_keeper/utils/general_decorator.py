import functools

def exception_handler(exception: Exception = Exception):
    """
    Decorator to wrap exceptions in custom error types while preserving context.
    
    Args:
        exception: Exception type to raise
    Returns:
        Wrapped function that raises specified exception type
    Raises:
        exception: Original error wrapped in specified exception type
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                raise exception(f"{func.__name__} failed: {str(e)}") from e
        return wrapper
    return decorator