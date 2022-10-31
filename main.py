import time
from flask import Flask, jsonify
import os
import quickfix as qf
import redis
import json

cache = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))

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

    #return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})
    return json.dumps(dir(qf))
    #return  jsonify({"count": count})


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
