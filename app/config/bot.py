from os import environ as env


WORK_DIR = env.get('WORK_DIR') or '/tmp'
PROXY = {"scheme": env.get("PROXY_SCHEME"),
         "hostname": env.get("PROXY_HOSTNAME"),
         "port": int(env.get("PROXY_PORT"))}
DEBUG = env.get('BOT_DEBUG')
REDIS_HOST = env.get('REDIS_HOST')
REDIS_PORT = env.get('REDIS_PORT')
REDIS_DB= env.get('REDIS_DB')
REDIS_PASS = env.get('REDIS_PASS')
API_URL = env.get('API_URL')
API_KEY= env.get('API_KEY')
CACHE_TTL=int(env.get('CACHE_TTL'))
ASK_TTL=int(env.get('ASK_TTL'))


from utils.connection import Connection

con = Connection(api_key=API_KEY, api_url=API_URL)
setting = con.setting.setting 
API_ID = int(setting.api_id)
API_HASH = setting.api_hash
BOT_TOKEN = setting.bot_token
BOT_SESSION = setting.session_string
BOT_USERNAME = setting.bot_username
