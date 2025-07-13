import asyncio

def async_retry(max_retries=3, delay=1):
    """
    Decorator to retry an async function with a specified number of retries and delay.
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt < max_retries - 1:
                        await asyncio.sleep(delay)
                    else:
                        raise e
        return wrapper
    return decorator