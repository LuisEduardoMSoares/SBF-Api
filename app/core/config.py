# Standard Imports
from os import getenv

# Authorization Configuration
JWT_SECRET = getenv("JWT_SECRET", default="The_quick_brown_fox_jumps_over_the_lazy_dog")
JWT_EXPIRATION_DAYS = int(getenv("JWT_EXPIRATION_DAYS", default=7))


# Database Configuration
DATABASE_URL = getenv("DATABASE_URL", default="sqlite:///:memory:")