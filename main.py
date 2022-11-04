import time
from flask import Flask, jsonify
import os
import quickfix as qf
import redis
import json
import requests

from dotenv import load_dotenv

load_dotenv()

cache = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
db_conn_url = os.getenv("POSTGRES_URL")
ta_patt_url = os.getenv("TA_PATT_URL")
print(ta_patt_url)

#cache = redis.Redis(host='redis', port=6379)
app = Flask(__name__)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def index():
    count = get_hit_count()
    ta_patterns = json.loads(requests.get(ta_patt_url).text)
    #return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})
    result = {"Hits": count,
            "ta_patterns" : ta_patterns,
            "quickfix": dir(qf)
            }
    return json.dumps(result, sort_keys=True, indent=4)
    #return  jsonify({"count": count})


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
