import redis
import time
from datadog import initialize, statsd

initialize(statsd_host="datadog-agent", statsd_port=8125)
r = redis.Redis(host='redis', port=6379)

while True:
    r.incr("page_view")
    count = int(r.get("page_view"))
    print(f"Current page views: {count}")
    statsd.gauge("app.redis.page_views", count, tags=["env:yuan_env"])
    time.sleep(5)