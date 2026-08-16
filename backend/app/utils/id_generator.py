import random
import string
from datetime import datetime

def generate_complaint_id() -> str:
    """
    Generates a unique complaint ID in the format RISK-YYYY-XXXXXX
    """
    year = datetime.utcnow().year
    # Generate 6 random alphanumeric characters
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"RISK-{year}-{random_str}"
