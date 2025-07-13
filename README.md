# Datadog Redis Integration Demo

������Ĵ���Ū Datadog �� Redis ����鼨��ơ�Ÿ��ǡ������ Redis Ū metrics �� logs ������� Datadog��

## ��Ʒ빽

```
Redis_Integration_Demo/
������ app/
��   ������ app.py              # Python ����������Ϣ�� Redis ����� metrics
��   ������ Dockerfile          # App �ƴﲽ����
��   ������ requirements.txt    # Python �������
������ datadog/
��   ������ Dockerfile          # Datadog Agent �ƴﲽ����
��   ������ conf.d/
��       ������ redisdb.yaml    # Redis ��������
������ docker-compose.yaml     # �ƴ���������
������ README.md              # ���?��ʸ��
```

## �͹�?��

### ��̳����

1. **Redis (redis:6)**
   - �󶡵������������̳
   - ����ü�� 6379

2. **Python App (app/)**
   - Ϣ�� Redis ����� metrics
   - ? 5 �ü��԰켡 Redis ���
   - ����� metrics ����� Datadog

3. **Datadog Agent (datadog/)**
   - �������� metrics��Redis metrics �� logs
   - �����ѣ���� Datadog ʿ��

### Docker Compose ����

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

## Metrics ��������

### Datadog Agent ��ư��������

Datadog Agent ����**��ư������Pull��**�ϼ������� Redis metrics �� logs��

1. **Metrics ����ή��**
   - Agent ? 15 �ü�ưϢ���� Redis ��̳
   - ���� Redis INFO ̿��ͼ�������
   - ���ϲ���?�����۴��� Datadog metrics �ʼ�
   - �����ѣ���� Datadog ʿ��

2. **Logs ����ή��**
   - Agent Ʃ�� Docker �ƴ���������
   - Ʃ�� Docker socket ¸���ƴ� logs
   - ��ڡ���ֵ�§���������� logs
   - �����ѣ���� Datadog ʿ��

### Redis Integration ����

**����?�ư��֡�** `datadog/conf.d/redisdb.yaml`

```yaml
init_config:

instances:
  - host: redis
    port: 6379
```

### ����?��

1. **Metrics ��������**
   - `host: redis`��Agent ��ưϢ��Ū��̳̾��
   - `port: 6379`��Agent Ϣ��Ū Redis ü��
   - Agent ��������� `redis-cli info` ̿��ͼ�������
   - ��ư���� INFO �������۴���ɸ�� metrics

2. **��ư����ή��**
   ```
   Datadog Agent ���� Redis INFO ̿�� �� ���ϲ���?�� �� �۴��� Metrics �� ѣ���� Datadog
   ```

3. **������Ū Metrics ����**
   - `redis.mem.used`��Redis �����������
   - `redis.stats.total_commands_processed`����̿��������
   - `redis.stats.connected_clients`��Ϣ�ܵ�?ü����
   - `redis.stats.keyspace_hits`��������̿�漡��
   - `redis.stats.keyspace_misses`��������̤̿�漡��

### ����� Metrics

**����?�ư��֡�** `app/app.py`

```python
# ����� metrics ����� Datadog
statsd.gauge("app.redis.page_views", count, tags=["env:yuan_env"])
```

## Logs ��������

### Datadog Agent ��ư���� Logs

Agent Ʃ��ʲ����������ƴ� logs��

1. **Docker Socket ¸��**
   - Agent �ݺ� `/var/run/docker.sock` ��¸���ƴ���
   - ľ��즼��ƴ�Ū stdout/stderr ͢��
   - ��ư�����ƴ�ɸ��Ū logs

2. **�ƴ� Logs ����ή��**
   ```
   Redis �ƴ�Ū stdout/stderr �� Docker daemon �� Agent 즼� �� ѣ���� Datadog
   ```

### �Ķ���������

�� `docker-compose.yaml` �桧

```yaml
environment:
  - DD_LOGS_ENABLED=true                           # ?�� logs ����
  - DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL=true     # ������ͭ�ƴ� logs
```

## ������

### 1. ?ư��̳

```bash
# ?ư��ͭ��̳
docker-compose up -d

# �ſ�������?ư��̳
docker-compose up --build -d

# ?����̳?��
docker-compose ps
```

### 2. ��? Datadog Agent �ƴ�

```bash
# ���� agent �ƴ�
docker exec -it datadog-agent /bin/bash

# ?�� agent ?��
docker exec -it datadog-agent agent status

# ?�� Redis integration ?��
docker exec -it datadog-agent agent status | grep -A 20 "redisdb"
```

### 3. ¬�� Redis Integration

```bash
# ¬�� Redis integration ��ǽ����? Agent ��ư�������������
docker exec -it datadog-agent agent check redisdb

# ?�� Redis metrics ����?�֡���?����ͭ�����©��
docker exec -it datadog-agent agent status | grep -A 15 "redisdb"

# ?�� logs ����?�֡���?����ͭ즼�����
docker exec -it datadog-agent agent status | grep -A 20 "Logs Agent"

# ?�� Agent ��ư����Ū�ܺٻ��
docker exec -it datadog-agent agent check redisdb --verbose

# ¬�� Agent �� Redis Ϣ�ܡ���?��ϩϢ�����������
docker exec -it datadog-agent ping redis
```

### 4. ?���ƴ� Logs

```bash
# ?�� Redis �ƴ� logs
docker logs integration_demo-redis-1 --tail 20

# ?�� App �ƴ� logs
docker logs integration_demo-app-1 --tail 20

# ?�� Datadog Agent logs
docker logs datadog-agent --tail 20

# ?���ƴ�����Ū logs
docker logs datadog-agent | grep -i redis
```

### 5. ¬�� Redis Ϣ��

```bash
# ���� Redis �ƴ�
docker exec -it integration_demo-redis-1 /bin/bash

# ���� redis-cli ¬��
docker exec -it integration_demo-redis-1 redis-cli ping
docker exec -it integration_demo-redis-1 redis-cli info memory
docker exec -it integration_demo-redis-1 redis-cli monitor
```

### 6. ¬�� App ��ǽ

```bash
# ���� App �ƴ�
docker exec -it integration_demo-app-1 /bin/bash

# ��ư���� app.py
docker exec -it integration_demo-app-1 python app.py

# ¬�� Python ���
docker exec -it integration_demo-app-1 python -c "import redis; print('Redis OK')"
docker exec -it integration_demo-app-1 python -c "from datadog import initialize, statsd; print('Datadog OK')"
```

### 7. ��?��̳

```bash
# ��?������̳
docker-compose restart redis
docker-compose restart app
docker-compose restart datadog-agent

# ��?��ͭ��̳
docker-compose restart
```

### 8. �����Ķ�

```bash
# ����°ܽ���ͭ�ƴ�
docker-compose down

# ����°ܽ���ͭ�ƴ�����ϩ
docker-compose down --remove-orphans

# ������ͭ����Ū����?
docker-compose down --rmi all
```

## �ƹ�����

### �� Datadog ʿ��?�ǻ���

1. **Metrics Explorer**
   - �ӿ� `redis.mem.used` ?�ǵ����������
   - �ӿ� `app.redis.page_views` ?�Ǽ���� metrics
   - �ӿ� `redis.stats.total_commands_processed` ?��̿��������

2. **Logs**
   - �ӿ� `service:redis` ?�� Redis logs
   - �ӿ� `source:redis` ?�� Redis ���� logs

3. **Infrastructure**
   - ?�� Redis ��̳��?��
   - ��? Datadog Agent Ϣ��?��

### �ξ��ӽ�����

1. **Redis metrics ̵ˡ������Agent ��ư�������ԡ�**
   ```bash
   # ��? Agent ��ư������������
   docker exec -it datadog-agent agent check redisdb
   
   # ��? Agent �� Redis Ū��ϩϢ��
   docker exec -it datadog-agent ping redis
   
   # ��? Agent ����ǽ���� Redis INFO ̿��
   docker exec -it datadog-agent redis-cli -h redis info
   
   # ?�� Agent ��ư����Ū�ܺٺ����©
   docker exec -it datadog-agent agent check redisdb --verbose
   ```

2. **Logs ̵ˡ������Agent ��ư�������ԡ�**
   ```bash
   # ��? Agent ��ư����?��
   docker exec -it datadog-agent agent status | grep -A 20 "Logs Agent"
   
   # ��? Docker socket �������γݺ�
   docker exec -it datadog-agent ls -la /var/run/docker.sock
   
   # ��?�ƴ� logs ����ͭ͢��
   docker logs integration_demo-redis-1
   
   # ��? Agent ����ǽ즼����ƴ�Ū logs
   docker exec -it datadog-agent agent status | grep "Logs Agent"
   ```

3. **Agent Ϣ������**
   ```bash
   # ��? API key ������������
   docker logs datadog-agent | grep -i "api key"
   
   # ��? Agent �� Datadog ʿ��ŪϢ��
   docker exec -it datadog-agent ping app.datadoghq.com
   
   # ��? Agent ����?��
   docker exec -it datadog-agent cat /etc/datadog-agent/datadog.yaml
   ```

## �ʳ�����

### ����� Redis ����

�İʽ��� `docker-compose.yaml`��

```yaml
redis:
  image: redis:6
  command: redis-server --loglevel verbose --maxmemory 256mb
  environment:
    - REDIS_PASSWORD=your_password
```

### ����� Datadog Agent ����

�� `datadog/Dockerfile` ��ź�ü�������֡�

```dockerfile
FROM gcr.io/datadoghq/agent:latest
COPY conf.d/redisdb.yaml /etc/datadog-agent/conf.d/redisdb.yaml
COPY datadog.yaml /etc/datadog-agent/datadog.yaml
```

### Agent ��ư������ΨĴ��

�İ�Ĵ���Ķ������Թ��� Agent ��ư����Ū��Ψ��

```yaml
environment:
  - DD_LOGS_CONFIG_PROCESSING_ENABLED=true
  - DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL=true
  # Ĵ�� metrics ������Ψ���á�
  - DD_LOGS_CONFIG_PROCESSING_TIMEOUT=10
```

## ��ջ���

1. **API Key ������**
   - ������ `DD_API_KEY` �Ķ����������ͭ��Ū Datadog API Key
   - ���Ļ��� Docker secrets ���Ķ�����?��

2. **��ϩϢ��**
   - �����ƴ��Ū��ϩϢ������
   - ��?�ɲ������

3. **�񸻻���**
   - �ƹ��ƴ�񸻻��Ѿ�
   - Ŭ��Ĵ���������� CPU ����

4. **������α**
   - Datadog ʿ��ͭ������α����
   - ��� logs ��¸����
