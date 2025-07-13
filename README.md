# Datadog Redis Integration Demo

ÇçÀ§°ì¸Ä´°À°Åª Datadog çĞ Redis À°¹ç±é¼¨Õó°Æ¡¤Å¸¼¨Ç¡²¿ÚÀ½¸ Redis Åª metrics ÏÂ logs ÊÂâ¤Á÷Åş Datadog¡£

## Õó°Æ·ë¹½

```
Redis_Integration_Demo/
¨§¨¡¨¡ app/
¨¢   ¨§¨¡¨¡ app.py              # Python ØæÍÑÄø¼°¡¤Ï¢ÀÜ Redis ÊÂâ¤Á÷ metrics
¨¢   ¨§¨¡¨¡ Dockerfile          # App ÍÆ´ï²½ÇÛÃÖ
¨¢   ¨¦¨¡¨¡ requirements.txt    # Python °ÍûòÅå·ï
¨§¨¡¨¡ datadog/
¨¢   ¨§¨¡¨¡ Dockerfile          # Datadog Agent ÍÆ´ï²½ÇÛÃÖ
¨¢   ¨¦¨¡¨¡ conf.d/
¨¢       ¨¦¨¡¨¡ redisdb.yaml    # Redis À°¹çÇÛÃÖ
¨§¨¡¨¡ docker-compose.yaml     # ÍÆ´ïÊÔÇÓÇÛÃÖ
¨¦¨¡¨¡ README.md              # Õó°Æ?ÌÀÊ¸·ï
```

## ²Í¹½?ÌÀ

### ÉşÌ³ÁÈÀ®

1. **Redis (redis:6)**
   - Äó¶¡µ­²±ñó»ñÎÁ¸ËÉşÌ³
   - ´ÆæåÃ¼¸ı 6379

2. **Python App (app/)**
   - Ï¢ÀÜ Redis ÊÂâ¤Á÷ metrics
   - ? 5 ÉÃ¼¹¹Ô°ì¼¡ Redis Áàºî
   - ¼«ÄêµÁ metrics â¤Á÷Åş Datadog

3. **Datadog Agent (datadog/)**
   - ÚÀ½¸·ÏÅı metrics¡¢Redis metrics ÏÂ logs
   - Õò»ñÎÁÑ£Á÷Åş Datadog Ê¿Âæ

### Docker Compose ÇÛÃÖ

```yaml
version: '3'
services:
  redis:
    image: redis:6

  app:
    build: ./app
    depends_on:
      - redis
    environment:
      - DD_AGENT_HOST=datadog-agent

  datadog-agent:
    build: ./datadog
    container_name: datadog-agent
    environment:
      - DD_API_KEY=your_api_key
      - DD_SITE=datadoghq.com
      - DD_DOGSTATSD_NON_LOCAL_TRAFFIC=true
      - DD_LOGS_ENABLED=true
      - DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL=true
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /proc/:/host/proc/:ro
      - /sys/fs/cgroup:/host/sys/fs/cgroup:ro
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
    depends_on:
      - redis
```

## Metrics ÚÀ½¸µ¡À©

### Datadog Agent ¼çÆ°ÚÀ½¸µ¡À©

Datadog Agent ºÎÍÑ**¼çÆ°ÚÀ½¸¡ÊPull¡Ë**ÌÏ¼°ĞÔÚÀ½¸ Redis metrics ÏÂ logs¡£

1. **Metrics ÚÀ½¸Î®Äø**
   - Agent ? 15 ÉÃ¼çÆ°Ï¢ÀÜÅş Redis ÉşÌ³
   - ¼¹¹Ô Redis INFO Ì¿Îá³Í¼è·ÏÅı»ñ¿Ö
   - ²òÀÏ²óØæ?ÍÆÊÂíÛ´¹°Ù Datadog metrics ³Ê¼°
   - Õò»ñÎÁÑ£Á÷Åş Datadog Ê¿Âæ

2. **Logs ÚÀ½¸Î®Äø**
   - Agent Æ©²á Docker ÍÆ´ïÆü»ïÚÀ½¸
   - Æ©²á Docker socket Â¸¼èÍÆ´ï logs
   - º¬Ú¡ÇÛÃÖµ¬Â§²áßÉÏÂÑİÍı logs
   - Õò»ñÎÁÑ£Á÷Åş Datadog Ê¿Âæ

### Redis Integration ÇÛÃÖ

**ÇÛÃÖ?°Æ°ÌÃÖ¡§** `datadog/conf.d/redisdb.yaml`

```yaml
init_config:

instances:
  - host: redis
    port: 6379
```

### ÇÛÃÖ?ÌÀ

1. **Metrics ÚÀ½¸ÒÔÚË**
   - `host: redis`¡§Agent ¼çÆ°Ï¢ÀÜÅªÉşÌ³Ì¾ãÊ
   - `port: 6379`¡§Agent Ï¢ÀÜÅª Redis Ã¼¸ı
   - Agent ĞòÄê´ü¼¹¹Ô `redis-cli info` Ì¿Îá³Í¼è·ÏÅı»ñ¿Ö
   - ¼«Æ°²òÀÏ INFO ²óØæÊÂíÛ´¹°ÙÉ¸½à metrics

2. **¼çÆ°ÚÀ½¸Î®Äø**
   ```
   Datadog Agent ¼¹¹Ô Redis INFO Ì¿Îá ¢ª ²òÀÏ²óØæ?ÍÆ ¢ª íÛ´¹°Ù Metrics ¢ª Ñ£Á÷Åş Datadog
   ```

3. **ÚÀ½¸ÅşÅª Metrics ÈÏÎã**
   - `redis.mem.used`¡§Redis µ­²±ñó»ÈÍÑÎÌ
   - `redis.stats.total_commands_processed`¡§åÁÌ¿ÎáÑİÍıÚË
   - `redis.stats.connected_clients`¡§Ï¢ÀÜµÒ?Ã¼ÚËÎÌ
   - `redis.stats.keyspace_hits`¡§¸°¶õ´ÖÌ¿Ãæ¼¡ÚË
   - `redis.stats.keyspace_misses`¡§¸°¶õ´ÖÌ¤Ì¿Ãæ¼¡ÚË

### ¼«ÄêµÁ Metrics

**ÇÛÃÖ?°Æ°ÌÃÖ¡§** `app/app.py`

```python
# ¼«ÄêµÁ metrics â¤Á÷Åş Datadog
statsd.gauge("app.redis.page_views", count, tags=["env:yuan_env"])
```

## Logs ÚÀ½¸µ¡À©

### Datadog Agent ÈïÆ°ÚÀ½¸ Logs

Agent Æ©²á°Ê²¼µ¡À©ÚÀ½¸ÍÆ´ï logs¡§

1. **Docker Socket Â¸¼è**
   - Agent ³İºÜ `/var/run/docker.sock` ĞÔÂ¸¼èÍÆ´ï»ñ¿Ö
   - Ä¾ÀÜì¦¼èÍÆ´ïÅª stdout/stderr Í¢½Ğ
   - ¼«Æ°¼±ÊÌÍÆ´ïÉ¸äŞÅª logs

2. **ÍÆ´ï Logs ÚÀ½¸Î®Äø**
   ```
   Redis ÍÆ´ïÅª stdout/stderr ¢ª Docker daemon ¢ª Agent ì¦¼è ¢ª Ñ£Á÷Åş Datadog
   ```

### ´Ä¶­ÚÎÚËÇÛÃÖ

ºß `docker-compose.yaml` Ãæ¡§

```yaml
environment:
  - DD_LOGS_ENABLED=true                           # ?ÍÑ logs ÚÀ½¸
  - DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL=true     # ÚÀ½¸½êÍ­ÍÆ´ï logs
```

## Áàºî»ØÆî

### 1. ?Æ°ÉşÌ³

```bash
# ?Æ°½êÍ­ÉşÌ³
docker-compose up -d

# ½Å¿··ú¹½ÊÂ?Æ°ÉşÌ³
docker-compose up --build -d

# ?´ÇÉşÌ³?ÂÖ
docker-compose ps
```

### 2. Üı? Datadog Agent ÍÆ´ï

```bash
# ¿ÊÆş agent ÍÆ´ï
docker exec -it datadog-agent /bin/bash

# ?´Ç agent ?ÂÖ
docker exec -it datadog-agent agent status

# ?´Ç Redis integration ?ÂÖ
docker exec -it datadog-agent agent status | grep -A 20 "redisdb"
```

### 3. Â¬»î Redis Integration

```bash
# Â¬»î Redis integration ¸ùÇ½¡ÊÜı? Agent ¼çÆ°ÚÀ½¸À§ÈİÀµ¾ï¡Ë
docker exec -it datadog-agent agent check redisdb

# ?´Ç Redis metrics ÚÀ½¸?ÂÖ¡ÊÜı?À§ÈİÍ­ºø¸í¿ÖÂ©¡Ë
docker exec -it datadog-agent agent status | grep -A 15 "redisdb"

# ?´Ç logs ÚÀ½¸?ÂÖ¡ÊÜı?À§ÈİÍ­ì¦¼èºø¸í¡Ë
docker exec -it datadog-agent agent status | grep -A 20 "Logs Agent"

# ?´Ç Agent ¼çÆ°ÚÀ½¸Åª¾ÜºÙ»ñ¿Ö
docker exec -it datadog-agent agent check redisdb --verbose

# Â¬»î Agent çĞ Redis Ï¢ÀÜ¡ÊÜı?ÌÖÏ©Ï¢ÀÜÀ§ÈİÀµ¾ï¡Ë
docker exec -it datadog-agent ping redis
```

### 4. ?´ÇÍÆ´ï Logs

```bash
# ?´Ç Redis ÍÆ´ï logs
docker logs integration_demo-redis-1 --tail 20

# ?´Ç App ÍÆ´ï logs
docker logs integration_demo-app-1 --tail 20

# ?´Ç Datadog Agent logs
docker logs datadog-agent --tail 20

# ?´ÇÍÆ´ïÁêïğÅª logs
docker logs datadog-agent | grep -i redis
```

### 5. Â¬»î Redis Ï¢ÀÜ

```bash
# ¿ÊÆş Redis ÍÆ´ï
docker exec -it integration_demo-redis-1 /bin/bash

# »ÈÍÑ redis-cli Â¬»î
docker exec -it integration_demo-redis-1 redis-cli ping
docker exec -it integration_demo-redis-1 redis-cli info memory
docker exec -it integration_demo-redis-1 redis-cli monitor
```

### 6. Â¬»î App ¸ùÇ½

```bash
# ¿ÊÆş App ÍÆ´ï
docker exec -it integration_demo-app-1 /bin/bash

# ¼êÆ°¼¹¹Ô app.py
docker exec -it integration_demo-app-1 python app.py

# Â¬»î Python Åå·ï
docker exec -it integration_demo-app-1 python -c "import redis; print('Redis OK')"
docker exec -it integration_demo-app-1 python -c "from datadog import initialize, statsd; print('Datadog OK')"
```

### 7. ½Å?ÉşÌ³

```bash
# ½Å?ÆÃÄêÉşÌ³
docker-compose restart redis
docker-compose restart app
docker-compose restart datadog-agent

# ½Å?½êÍ­ÉşÌ³
docker-compose restart
```

### 8. À¶Íı´Ä¶­

```bash
# Ää»ßÊÂ°Ü½ü½êÍ­ÍÆ´ï
docker-compose down

# Ää»ßÊÂ°Ü½ü½êÍ­ÍÆ´ïÏÂÌÖÏ©
docker-compose down --remove-orphans

# À¶Íı½êÍ­ÁêïğÅª±ÇÁü?
docker-compose down --rmi all
```

## ´Æ¹µÌÌÈÄ

### ºß Datadog Ê¿Âæ?´Ç»ñÎÁ

1. **Metrics Explorer**
   - ÙÓ¿Ò `redis.mem.used` ?´Çµ­²±ñó»ÈÍÑÎÌ
   - ÙÓ¿Ò `app.redis.page_views` ?´Ç¼«ÄêµÁ metrics
   - ÙÓ¿Ò `redis.stats.total_commands_processed` ?´ÇÌ¿ÎáÑİÍıÚË

2. **Logs**
   - ÙÓ¿Ò `service:redis` ?´Ç Redis logs
   - ÙÓ¿Ò `source:redis` ?´Ç Redis Áêïğ logs

3. **Infrastructure**
   - ?´Ç Redis ÉşÌ³·ò¹¯?ÂÖ
   - Üı? Datadog Agent Ï¢ÀÜ?ÂÖ

### ¸Î¾ãÇÓ½ü»ØÆî

1. **Redis metrics ÌµË¡ÚÀ½¸¡ÊAgent ¼çÆ°ÚÀ½¸¼ºÇÔ¡Ë**
   ```bash
   # Üı? Agent ¼çÆ°ÚÀ½¸À§ÈİÀµ¾ï
   docker exec -it datadog-agent agent check redisdb
   
   # Üı? Agent çĞ Redis ÅªÌÖÏ©Ï¢ÀÜ
   docker exec -it datadog-agent ping redis
   
   # Üı? Agent À§ÈİÇ½¼¹¹Ô Redis INFO Ì¿Îá
   docker exec -it datadog-agent redis-cli -h redis info
   
   # ?´Ç Agent ¼çÆ°ÚÀ½¸Åª¾ÜºÙºø¸í¿ÖÂ©
   docker exec -it datadog-agent agent check redisdb --verbose
   ```

2. **Logs ÌµË¡ÚÀ½¸¡ÊAgent ÈïÆ°ÚÀ½¸¼ºÇÔ¡Ë**
   ```bash
   # Üı? Agent ÈïÆ°ÚÀ½¸?ÂÖ
   docker exec -it datadog-agent agent status | grep -A 20 "Logs Agent"
   
   # Üı? Docker socket À§ÈİÀµ³Î³İºÜ
   docker exec -it datadog-agent ls -la /var/run/docker.sock
   
   # Üı?ÍÆ´ï logs À§ÈİÍ­Í¢½Ğ
   docker logs integration_demo-redis-1
   
   # Üı? Agent À§ÈİÇ½ì¦¼èÅşÍÆ´ïÅª logs
   docker exec -it datadog-agent agent status | grep "Logs Agent"
   ```

3. **Agent Ï¢ÀÜÌäÂê**
   ```bash
   # Üı? API key À§ÈİÀµ³ÎÀßÄê
   docker logs datadog-agent | grep -i "api key"
   
   # Üı? Agent çĞ Datadog Ê¿ÂæÅªÏ¢ÀÜ
   docker exec -it datadog-agent ping app.datadoghq.com
   
   # Üı? Agent ÇÛÃÖ?°Æ
   docker exec -it datadog-agent cat /etc/datadog-agent/datadog.yaml
   ```

## ¿Ê³¬ÇÛÃÖ

### ¼«ÄêµÁ Redis ÇÛÃÖ

²Ä°Ê½¤²ş `docker-compose.yaml`¡§

```yaml
redis:
  image: redis:6
  command: redis-server --loglevel verbose --maxmemory 256mb
  environment:
    - REDIS_PASSWORD=your_password
```

### ¼«ÄêµÁ Datadog Agent ÇÛÃÖ

ºß `datadog/Dockerfile` ÃæÅº²Ã¼«ÄêµÁÇÛÃÖ¡§

```dockerfile
FROM gcr.io/datadoghq/agent:latest
COPY conf.d/redisdb.yaml /etc/datadog-agent/conf.d/redisdb.yaml
COPY datadog.yaml /etc/datadog-agent/datadog.yaml
```

### Agent ¼çÆ°ÚÀ½¸ÉÑÎ¨Ä´À°

²Ä°ÊÄ´À°´Ä¶­ÚÎÚËĞÔ¹µÀ© Agent ¼çÆ°ÚÀ½¸ÅªÉÑÎ¨¡§

```yaml
environment:
  - DD_LOGS_CONFIG_PROCESSING_ENABLED=true
  - DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL=true
  # Ä´À° metrics ÚÀ½¸ÉÑÎ¨¡ÊÉÃ¡Ë
  - DD_LOGS_CONFIG_PROCESSING_TIMEOUT=10
```

## Ãí°Õ»ö¹à

1. **API Key °ÂÁ´À­**
   - ÀÁ³ÎÊİ `DD_API_KEY` ´Ä¶­ÚÎÚËÀßÄê°ÙÍ­ÚÃÅª Datadog API Key
   - ·úµÄ»ÈÍÑ Docker secrets °¿´Ä¶­ÚÎÚË?°Æ

2. **ÌÖÏ©Ï¢ÀÜ**
   - ³ÎÊİÍÆ´ï´ÖÅªÌÖÏ©Ï¢ÀÜÀµ¾ï
   - Üı?ËÉ²Ğà¯ÀßÄê

3. **»ñ¸»»ÈÍÑ**
   - ´Æ¹µÍÆ´ï»ñ¸»»ÈÍÑ¾ğ¶·
   - Å¬áÄÄ´À°µ­²±ñóÏÂ CPU ¸ÂÀ©

4. **»ñÎÁÊİÎ±**
   - Datadog Ê¿ÂæÍ­»ñÎÁÊİÎ±´ü¸Â
   - Ãí°Õ logs ÌÙÂ¸À®ËÜ
