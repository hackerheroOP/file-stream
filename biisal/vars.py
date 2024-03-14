import os

class Var():
    """Configuration variables for the bot."""

    def __init__(self):
        # Flag to enable or disable multiple clients
        self.MULTI_CLIENT = False

        # API credentials
        self.API_ID = self.get_env('API_ID', 0)
        self.API_HASH = self.get_env('API_HASH', '')
        self.BOT_TOKEN = self.get_env('BOT_TOKEN', '')

        # Bot settings
        self.name = self.get_env('name', 'FileToLinkWalaBot')
        self.SLEEP_THRESHOLD = self.get_env('SLEEP_THRESHOLD', 60)
        self.WORKERS = self.get_env('WORKERS', 4)
        self.BIN_CHANNEL = self.get_env('BIN_CHANNEL', 0)
        self.NEW_USER_LOG = self.get_env('NEW_USER_LOG', 0)
        self.PORT = self.get_env('PORT', 8080)
        self.BIND_ADRESS = self.get_env('WEB_SERVER_BIND_ADDRESS', '0.0.0.0')
        self.PING_INTERVAL = self.get_env('PING_INTERVAL', 1200)  # 20 minutes

        # Owner settings
        self.OWNER_ID = self.get_list_env('OWNER_ID', [1251111009])
        self.NO_PORT = self.get_env('NO_PORT', False)
        self.OWNER_USERNAME = self.get_env('OWNER_USERNAME', 'biisal')

        # Heroku settings
        self.ON_HEROKU = 'DYNO' in os.environ
        self.FQDN = self.get_env('FQDN', self.BIND_ADRESS + ':' + str(self.PORT)) if not self.ON_HEROKU else self.APP_NAME + '.herokuapp.com'

        # SSL settings
        self.HAS_SSL = self.get_env('HAS_SSL', True)
        self.URL = 'https://{}/'.format(self.FQDN) if self.HAS_SSL else 'http://{}/'.format(self.FQDN)

        # Database settings
        self.DATABASE_URL = self.get_env('DATABASE_URL', '')

        # Channel settings
        self.UPDATES_CHANNEL = self.get_env('UPDATES_CHANNEL', 'movies_unloaded2')
        self.BANNED_CHANNELS = list(set(self.get_list_env('BANNED_CHANNELS', [])))
        self.BAN_CHNL = list(
