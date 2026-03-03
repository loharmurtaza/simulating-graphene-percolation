from dotenv import load_dotenv


# -------------------------------------------------
# Load Environment Variables
# -------------------------------------------------
def load_dotenv_variables() -> None:
    """
    Load environment variables from .env file.
    """
    load_dotenv()
