# Standard Imports
from os import getenv

# Typing Imports
from typing import List


# Authorization Configuration
JWT_SECRET = getenv("JWT_SECRET", default="The_quick_brown_fox_jumps_over_the_lazy_dog")
JWT_EXPIRATION_DAYS = int(getenv("JWT_EXPIRATION_DAYS", default=7))


# Database Configuration
DATABASE_URL = getenv("DATABASE_URL", default="sqlite:///:memory:")


# Get CORS Origins
def get_cors_origins() -> List[str]:
    _cors = getenv("PROD_CORS", default=False)
    if _cors == True:
        return ["https://sbf-frontend.herokuapp.com"]
    else:
        return [
            "https://sbf-frontend.herokuapp.com",
            "http://localhost:3000",
            "http://127.0.0.1:3000"
        ]