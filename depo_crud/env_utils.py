import os


def get_env_list(name: str, default: str = "", required: bool = False) -> list[str]:
    """Helper function to read a comma-separated list from an environment variable."""
    value = os.getenv(name, default)

    if required and not value:
        raise ValueError(f"{name} environment variable not set")

    return [item.strip() for item in value.split(",") if item.strip()]
