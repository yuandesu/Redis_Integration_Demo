# Datadog Redis Integration Demo

這是一個完整的 Datadog 與 Redis 整合演示專案，展示如何收集 Redis 的 metrics 和 logs 並發送到 Datadog。

## 專案結構

```
Redis_Integration_Demo/
├── app/
│   ├── app.py              # Python 應用程式，連接 Redis 並發送 metrics
│   ├── Dockerfile          # App 容器化配置
│   └── requirements.txt    # Python 依賴套件
├── datadog/
│   ├── Dockerfile          # Datadog Agent 容器化配置
│   └── conf.d/
│       └── redisdb.yaml    # Redis 整合配置
├── docker-compose.yaml     # 容器編排配置
└── README.md   
```

## 架構

### 服務組成

1. **Redis (redis:6)**
   - 提供記憶體資料庫服務
   - 監聽端口 6379

2. **Python App (app/)**
   - 連接 Redis 並發送 metrics
   - 每 5 秒執行一次 Redis 操作
   - 自定義 metrics 發送到 Datadog

3. **Datadog Agent (datadog/)**
   - 收集系統 metrics、Redis metrics 和 logs
   - 將資料傳送到 Datadog 平台

### Docker Compose 配置

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

## Metrics 收集機制

### Datadog Agent 主動收集機制

Datadog Agent 採用**主動收集（Pull）**模式來收集 Redis metrics 和 logs。

1. **Metrics 收集流程**
   - Agent 每 15 秒主動連接到 Redis 服務
   - 執行 Redis INFO 命令獲取系統資訊
   - 解析回應內容並轉換為 Datadog metrics 格式
   - 將資料傳送到 Datadog 平台

2. **Logs 收集流程**
   - Agent 透過 Docker 容器日誌收集
   - 透過 Docker socket 存取容器 logs
   - 根據配置規則過濾和處理 logs
   - 將資料傳送到 Datadog 平台

### Redis Integration 配置

**配置檔案位置：** `datadog/conf.d/redisdb.yaml`

```yaml
init_config:

instances:
  - host: redis
    port: 6379
```

### 配置說明

1. **Metrics 收集參數**
   - `host: redis`：Agent 主動連接的服務名稱
   - `port: 6379`：Agent 連接的 Redis 端口
   - Agent 會定期執行 `redis-cli info` 命令獲取系統資訊
   - 自動解析 INFO 回應並轉換為標準 metrics

2. **主動收集流程**
   ```
   Datadog Agent 執行 Redis INFO 命令 → 解析回應內容 → 轉換為 Metrics → 傳送到 Datadog
   ```

3. **收集到的 Metrics 範例**
   - `redis.mem.used`：Redis 記憶體使用量
   - `redis.stats.total_commands_processed`：總命令處理數
   - `redis.stats.connected_clients`：連接客戶端數量
   - `redis.stats.keyspace_hits`：鍵空間命中次數
   - `redis.stats.keyspace_misses`：鍵空間未命中次數

### 自定義 Metrics

**配置檔案位置：** `app/app.py`

```python
# 自定義 metrics 發送到 Datadog
statsd.gauge("app.redis.page_views", count, tags=["env:yuan_env"])
```

## Logs 收集機制

### Datadog Agent 被動收集 Logs

Agent 透過以下機制收集容器 logs：

1. **Docker Socket 存取**
   - Agent 掛載 `/var/run/docker.sock` 來存取容器資訊
   - 直接讀取容器的 stdout/stderr 輸出
   - 自動識別容器標籤的 logs

2. **容器 Logs 收集流程**
   ```
   Redis 容器的 stdout/stderr → Docker daemon → Agent 讀取 → 傳送到 Datadog
   ```

### 環境變數配置

在 `docker-compose.yaml` 中：

```yaml
environment:
  - DD_LOGS_ENABLED=true                           # 啟用 logs 收集
  - DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL=true     # 收集所有容器 logs
```

## 操作指南

### 1. 啟動服務

```bash
# 啟動所有服務
docker-compose up -d

# 重新建構並啟動服務
docker-compose up --build -d

# 查看服務狀態
docker-compose ps
```

### 2. 檢查 Datadog Agent 容器

```bash
# 進入 agent 容器
docker exec -it datadog-agent /bin/bash

# 查看 agent 狀態
docker exec -it datadog-agent agent status

# 查看 Redis integration 狀態
docker exec -it datadog-agent agent status | grep -A 20 "redisdb"
```

### 3. 測試 Redis Integration

```bash
# 測試 Redis integration 功能（檢查 Agent 主動收集是否正常）
docker exec -it datadog-agent agent check redisdb

# 查看 Redis metrics 收集狀態（檢查是否有錯誤訊息）
docker exec -it datadog-agent agent status | grep -A 15 "redisdb"

# 查看 logs 收集狀態（檢查是否有讀取錯誤）
docker exec -it datadog-agent agent status | grep -A 20 "Logs Agent"

# 查看 Agent 主動收集的詳細資訊
docker exec -it datadog-agent agent check redisdb --verbose

# 測試 Agent 與 Redis 連接（檢查網路連接是否正常）
docker exec -it datadog-agent ping redis
```

### 4. 查看容器 Logs

```bash
# 查看 Redis 容器 logs
docker logs integration_demo-redis-1 --tail 20

# 查看 App 容器 logs
docker logs integration_demo-app-1 --tail 20

# 查看 Datadog Agent logs
docker logs datadog-agent --tail 20

# 查看容器相關的 logs
docker logs datadog-agent | grep -i redis
```

### 5. 測試 Redis 連接

```bash
# 進入 Redis 容器
docker exec -it integration_demo-redis-1 /bin/bash

# 使用 redis-cli 測試
docker exec -it integration_demo-redis-1 redis-cli ping
docker exec -it integration_demo-redis-1 redis-cli info memory
docker exec -it integration_demo-redis-1 redis-cli monitor
```

### 6. 測試 App 功能

```bash
# 進入 App 容器
docker exec -it integration_demo-app-1 /bin/bash

# 手動執行 app.py
docker exec -it integration_demo-app-1 python app.py

# 測試 Python 套件
docker exec -it integration_demo-app-1 python -c "import redis; print('Redis OK')"
docker exec -it integration_demo-app-1 python -c "from datadog import initialize, statsd; print('Datadog OK')"
```

### 7. 重啟服務

```bash
# 重啟特定服務
docker-compose restart redis
docker-compose restart app
docker-compose restart datadog-agent

# 重啟所有服務
docker-compose restart
```

### 8. 清理環境

```bash
# 停止並移除所有容器
docker-compose down

# 停止並移除所有容器和網路
docker-compose down --remove-orphans

# 清理所有相關的映像檔
docker-compose down --rmi all
```

## 監控面板

### 在 Datadog 平台查看資料

1. **Metrics Explorer**
   - 搜尋 `redis.mem.used` 查看記憶體使用量
   - 搜尋 `app.redis.page_views` 查看自定義 metrics
   - 搜尋 `redis.stats.total_commands_processed` 查看命令處理數

2. **Logs**
   - 搜尋 `service:redis` 查看 Redis logs
   - 搜尋 `source:redis` 查看 Redis 相關 logs

3. **Infrastructure**
   - 查看 Redis 服務健康狀態
   - 檢查 Datadog Agent 連接狀態

### 故障排除指南

1. **Redis metrics 無法收集（Agent 主動收集失敗）**
   ```bash
   # 檢查 Agent 主動收集是否正常
   docker exec -it datadog-agent agent check redisdb
   
   # 檢查 Agent 與 Redis 的網路連接
   docker exec -it datadog-agent ping redis
   
   # 檢查 Agent 是否能執行 Redis INFO 命令
   docker exec -it datadog-agent redis-cli -h redis info
   
   # 查看 Agent 主動收集的詳細錯誤訊息
   docker exec -it datadog-agent agent check redisdb --verbose
   ```

2. **Logs 無法收集（Agent 被動收集失敗）**
   ```bash
   # 檢查 Agent 被動收集狀態
   docker exec -it datadog-agent agent status | grep -A 20 "Logs Agent"
   
   # 檢查 Docker socket 是否正確掛載
   docker exec -it datadog-agent ls -la /var/run/docker.sock
   
   # 檢查容器 logs 是否有輸出
   docker logs integration_demo-redis-1
   
   # 檢查 Agent 是否能讀取到容器的 logs
   docker exec -it datadog-agent agent status | grep "Logs Agent"
   ```

3. **Agent 連接問題**
   ```bash
   # 檢查 API key 是否正確設定
   docker logs datadog-agent | grep -i "api key"
   
   # 檢查 Agent 與 Datadog 平台的連接
   docker exec -it datadog-agent ping app.datadoghq.com
   
   # 檢查 Agent 配置檔案
   docker exec -it datadog-agent cat /etc/datadog-agent/datadog.yaml
   ```

## 進階配置

### 自定義 Redis 配置

可以修改 `docker-compose.yaml`：

```yaml
redis:
  image: redis:6
  command: redis-server --loglevel verbose --maxmemory 256mb
  environment:
    - REDIS_PASSWORD=your_password
```

### 自定義 Datadog Agent 配置

在 `datadog/Dockerfile` 中添加自定義配置：

```dockerfile
FROM gcr.io/datadoghq/agent:latest
COPY conf.d/redisdb.yaml /etc/datadog-agent/conf.d/redisdb.yaml
COPY datadog.yaml /etc/datadog-agent/datadog.yaml
```

### Agent 主動收集頻率調整

可以調整環境變數來控制 Agent 主動收集的頻率：

```yaml
environment:
  - DD_LOGS_CONFIG_PROCESSING_ENABLED=true
  - DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL=true
  # 調整 metrics 收集頻率（秒）
  - DD_LOGS_CONFIG_PROCESSING_TIMEOUT=10
```

## 注意事項

1. **API Key 安全性**
   - 請確保 `DD_API_KEY` 環境變數設定為有效的 Datadog API Key
   - 建議使用 Docker secrets 或環境變數檔案

2. **網路連接**
   - 確保容器間的網路連接正常
   - 檢查防火牆設定

3. **資源使用**
   - 監控容器資源使用情況
   - 適當調整記憶體和 CPU 限制

4. **資料保留**
   - Datadog 平台有資料保留期限
   - 注意 logs 儲存成本
