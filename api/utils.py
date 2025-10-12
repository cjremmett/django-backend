import redis
import requests
import time
REDIS_HOST = 'host.docker.internal'
BASE_URL = 'https://cjremmett.com/logging'


def get_redis_cursor(host='localhost', port=6379):
    return redis.Redis(host, port, db=0, decode_responses=True)


def get_secrets_dict():
    r = get_redis_cursor(host=REDIS_HOST)
    secrets_list = r.json().get('secrets', '$')
    return secrets_list[0]


def get_logging_microservice_token() -> str:
    return get_secrets_dict()['secrets']['logging_microservice']['api_token']


def append_to_log(level: str, message: str) -> requests.Response:
   json = {'table': 'cjremmett_logs', 'category': 'DJANGO', 'level': level, 'message': message}
   headers = {'token': get_logging_microservice_token()}
   response = requests.post(BASE_URL + '/append-to-log', json=json, headers=headers)
   return response
        

def log_resource_access(url: str, ip: str) -> requests.Response:
   json = {'resource': url, 'ip_address': ip}
   headers = {'token': get_logging_microservice_token()}
   response = requests.post(BASE_URL + '/log-resource-access', json=json, headers=headers)
   return response

def get_epoch_time():
   return str(time.time())


def get_calendar_datetime_utc_string():
   return time.datetime.now(time.timezone.utc).strftime('%m/%d/%y %H:%M:%S')