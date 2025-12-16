
import string
from secrets import choice

alphaabet: str = string.ascii_letters + string.digits

def generate_slug() -> str:
    """Генерирует случайный slug длиной 6 символов из букв и цифр."""
    return ''.join(choice(alphaabet) for _ in range(6))