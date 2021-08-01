import random
import string

import redis as r

redis = r.Redis(host='localhost', port=6379, decode_responses=True)
token_expire = 259800


def genetate_token(user_id):
    count = 32
    str_from = string.ascii_letters + string.digits
    token_list = [random.choice(str_from) for _ in range(count)]
    token = "".join(token_list)
    redis.set(token, str(user_id), ex=token_expire)
    return token
