from os import environ  # Importing os.environ to access environment variables
from typing import Dict, Optional  # Importing required types for type hinting

class EnvironmentTokenParser:
    """
    A class for parsing tokens from environment variables.
    This class provides methods to initialize, parse tokens from environment variables, and retrieve tokens by their id.
    """

    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize the EnvironmentTokenParser instance.

        :param config_file: The path to the config file. Not used in this version.
        """
        # Initializing an empty dictionary to store token id and token value pairs
        self.tokens: Dict[int, str] = {}
        self.config_file = config_file  # Not used in this version, but left for future use

    def parse_from_env(self) -> Dict[int, str]:
        """
        Parse tokens from environment variables.

        :return: A dictionary containing the tokens.
        """
        # Creating a new dictionary with sorted environment variables starting with 'MULTI_TOKEN'
        self.tokens = dict((c + 1, t) for c, (k, t) in enumerate(filter(
            lambda n: n[0].startswith("MULTI_TOKEN"), sorted(environ.items()))))

        # Adding error handling for missing environment variables
        missing_tokens = [k for k in self.tokens.keys() if k not in environ]
        if missing_tokens:
            raise KeyError(f"Missing environment variables: {missing_tokens}")

        return self.tokens  # Returning the parsed tokens

    def get_token(self, token_id: int) -> str:
        """
        Get the token by its id.

        :param token_id: The id of the token.
        :return: The token value.
        """
        return self.tokens.get(token_id, "")  # Returning the token value or an empty string if not found
