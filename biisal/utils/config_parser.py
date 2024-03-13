from os import environ
from typing import Dict, Optional

class EnvironmentTokenParser:
    """
    A class for parsing tokens from environment variables.
    """

    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize the EnvironmentTokenParser instance.

        :param config_file: The path to the config file. Not used in this version.
        """
        self.tokens: Dict[int, str] = {}
        self.config_file = config_file

    def parse_from_env(self) -> Dict[int, str]:
        """
        Parse tokens from environment variables.

        :return: A dictionary containing the tokens.
        """
        self.tokens = dict((c + 1, t) for c, (k, t) in enumerate(filter(
            lambda n: n[0].startswith("MULTI_TOKEN"), sorted(environ.items()))))

        # Add error handling for missing environment variables
        missing_tokens = [k for k in self.tokens.keys() if k not in environ]
        if missing_tokens:
            raise KeyError(f"Missing environment variables: {missing_tokens}")

        return self.tokens

    def get_token(self, token_id: int) -> str:
        """
        Get the token by its id.

        :param token_id: The id of the token.
        :return: The token value.
        """
        return self.tokens.get(token_id, "")
