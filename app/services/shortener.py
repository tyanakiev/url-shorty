import string
import random

def generate_short_code(length: int = 7) -> str:
    """Generate a random Base62-like short code."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))
