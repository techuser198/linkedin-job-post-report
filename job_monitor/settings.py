import os

from dotenv import load_dotenv

load_dotenv()

LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL", "")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD", "")


def validate_linkedin_credentials(email: str, password: str) -> None:
    if not email or not password:
        raise ValueError(
            "Missing LinkedIn credentials. Set LINKEDIN_EMAIL and LINKEDIN_PASSWORD in .env."
        )


def get_default_linkedin_credentials() -> tuple[str, str]:
    return LINKEDIN_EMAIL, LINKEDIN_PASSWORD
