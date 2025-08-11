import datetime


def get_current_time():
    """Returns the current time in H:MM AM/PM format."""
    now = datetime.datetime.now()  # Get current time
    now = now.strftime("%I:%M %p")  # Format time in H:MM AM/PM format
    return now


def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b
