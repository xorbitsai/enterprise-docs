.. _langfuse_usage:

========================
企业版链路日志使用
========================

本文档介绍如何使用Xinference企业版的链路日志功能，基于Langfuse服务实现调用链路追踪和监控。

.. contents:: 目录
   :local:
   :depth: 2

前置要求
========

系统要求
--------

在部署Langfuse服务之前，请确保：

* **Docker**：Docker 20.10+ 和 Docker Compose v2+
* **内存**：建议至少4GB可用内存
* **存储**：至少10GB可用磁盘空间
* **网络**：确保相关端口未被占用

端口要求
--------

Langfuse服务需要以下端口：

* **3000**：Langfuse Web界面
* **5432**：PostgreSQL数据库
* **6379**：Redis缓存
* **8123/9000**：ClickHouse数据库
* **9090/9091**：MinIO对象存储

.. code-block:: bash

   # 检查端口占用情况
   netstat -tlnp | grep -E "(3000|5432|6379|8123|9000|9090|9091)"

概览
====

链路以及模型使用情况等相关的功能依赖于Langfuse服务，因此在启动Xinference后，还需要启动Langfuse服务。

Langfuse是一个开源的LLM工程平台，提供：

* **链路追踪**：完整的模型调用链路记录
* **性能监控**：延迟、Token使用量等指标统计
* **调用分析**：模型使用情况和趋势分析
* **调试支持**：详细的输入输出日志

服务启动
========

使用Docker Compose启动Langfuse服务。将以下代码保存为 ``docker-compose.yaml`` 文件，xinference即可自动接入Langfuse服务。

.. warning::
   **安全配置重要提醒**：
   
   配置文件中包含多个需要修改的安全参数，标记为 ``# CHANGEME``：
   
   * 数据库密码
   * Redis认证密码  
   * MinIO访问密钥
   * ClickHouse密码
   * 加密密钥等
   
   **生产环境部署前务必修改这些默认值！**

Docker Compose配置
------------------

.. code-block:: yaml

  version: '3.8'

  services:
    langfuse-worker:
      image: docker.io/langfuse/langfuse-worker:3
      restart: always
      depends_on: &langfuse-depends-on
        postgres:
          condition: service_healthy
        minio:
          condition: service_healthy
        redis:
          condition: service_healthy
        clickhouse:
          condition: service_healthy
      ports:
        - 127.0.0.1:3030:3030
      environment: &langfuse-worker-env
        NEXTAUTH_URL: http://localhost:3000
        DATABASE_URL: postgresql://postgres:postgres@postgres:5432/postgres # CHANGEME
        SALT: "mysalt" # CHANGEME
        ENCRYPTION_KEY: "0000000000000000000000000000000000000000000000000000000000000000" # CHANGEME: generate via `openssl rand -hex 32`
        TELEMETRY_ENABLED: ${TELEMETRY_ENABLED:-true}
        LANGFUSE_ENABLE_EXPERIMENTAL_FEATURES: ${LANGFUSE_ENABLE_EXPERIMENTAL_FEATURES:-true}
        CLICKHOUSE_MIGRATION_URL: ${CLICKHOUSE_MIGRATION_URL:-clickhouse://clickhouse:9000}
        CLICKHOUSE_URL: ${CLICKHOUSE_URL:-http://clickhouse:8123}
        CLICKHOUSE_USER: ${CLICKHOUSE_USER:-clickhouse}
        CLICKHOUSE_PASSWORD: ${CLICKHOUSE_PASSWORD:-clickhouse} # CHANGEME
        CLICKHOUSE_CLUSTER_ENABLED: ${CLICKHOUSE_CLUSTER_ENABLED:-false}
        LANGFUSE_USE_AZURE_BLOB: ${LANGFUSE_USE_AZURE_BLOB:-false}
        LANGFUSE_S3_EVENT_UPLOAD_BUCKET: ${LANGFUSE_S3_EVENT_UPLOAD_BUCKET:-langfuse}
        LANGFUSE_S3_EVENT_UPLOAD_REGION: ${LANGFUSE_S3_EVENT_UPLOAD_REGION:-auto}
        LANGFUSE_S3_EVENT_UPLOAD_ACCESS_KEY_ID: ${LANGFUSE_S3_EVENT_UPLOAD_ACCESS_KEY_ID:-minio}
        LANGFUSE_S3_EVENT_UPLOAD_SECRET_ACCESS_KEY: ${LANGFUSE_S3_EVENT_UPLOAD_SECRET_ACCESS_KEY:-miniosecret} # CHANGEME
        LANGFUSE_S3_EVENT_UPLOAD_ENDPOINT: ${LANGFUSE_S3_EVENT_UPLOAD_ENDPOINT:-http://minio:9000}
        LANGFUSE_S3_EVENT_UPLOAD_FORCE_PATH_STYLE: ${LANGFUSE_S3_EVENT_UPLOAD_FORCE_PATH_STYLE:-true}
        LANGFUSE_S3_EVENT_UPLOAD_PREFIX: ${LANGFUSE_S3_EVENT_UPLOAD_PREFIX:-events/}
        LANGFUSE_S3_MEDIA_UPLOAD_BUCKET: ${LANGFUSE_S3_MEDIA_UPLOAD_BUCKET:-langfuse}
        LANGFUSE_S3_MEDIA_UPLOAD_REGION: ${LANGFUSE_S3_MEDIA_UPLOAD_REGION:-auto}
        LANGFUSE_S3_MEDIA_UPLOAD_ACCESS_KEY_ID: ${LANGFUSE_S3_MEDIA_UPLOAD_ACCESS_KEY_ID:-minio}
        LANGFUSE_S3_MEDIA_UPLOAD_SECRET_ACCESS_KEY: ${LANGFUSE_S3_MEDIA_UPLOAD_SECRET_ACCESS_KEY:-miniosecret} # CHANGEME
        LANGFUSE_S3_MEDIA_UPLOAD_ENDPOINT: ${LANGFUSE_S3_MEDIA_UPLOAD_ENDPOINT:-http://localhost:9090}
        LANGFUSE_S3_MEDIA_UPLOAD_FORCE_PATH_STYLE: ${LANGFUSE_S3_MEDIA_UPLOAD_FORCE_PATH_STYLE:-true}
        LANGFUSE_S3_MEDIA_UPLOAD_PREFIX: ${LANGFUSE_S3_MEDIA_UPLOAD_PREFIX:-media/}
        LANGFUSE_S3_BATCH_EXPORT_ENABLED: ${LANGFUSE_S3_BATCH_EXPORT_ENABLED:-false}
        LANGFUSE_S3_BATCH_EXPORT_BUCKET: ${LANGFUSE_S3_BATCH_EXPORT_BUCKET:-langfuse}
        LANGFUSE_S3_BATCH_EXPORT_PREFIX: ${LANGFUSE_S3_BATCH_EXPORT_PREFIX:-exports/}
        LANGFUSE_S3_BATCH_EXPORT_REGION: ${LANGFUSE_S3_BATCH_EXPORT_REGION:-auto}
        LANGFUSE_S3_BATCH_EXPORT_ENDPOINT: ${LANGFUSE_S3_BATCH_EXPORT_ENDPOINT:-http://minio:9000}
        LANGFUSE_S3_BATCH_EXPORT_EXTERNAL_ENDPOINT: ${LANGFUSE_S3_BATCH_EXPORT_EXTERNAL_ENDPOINT:-http://localhost:9090}
        LANGFUSE_S3_BATCH_EXPORT_ACCESS_KEY_ID: ${LANGFUSE_S3_BATCH_EXPORT_ACCESS_KEY_ID:-minio}
        LANGFUSE_S3_BATCH_EXPORT_SECRET_ACCESS_KEY: ${LANGFUSE_S3_BATCH_EXPORT_SECRET_ACCESS_KEY:-miniosecret} # CHANGEME
        LANGFUSE_S3_BATCH_EXPORT_FORCE_PATH_STYLE: ${LANGFUSE_S3_BATCH_EXPORT_FORCE_PATH_STYLE:-true}
        LANGFUSE_INGESTION_QUEUE_DELAY_MS: ${LANGFUSE_INGESTION_QUEUE_DELAY_MS:-}
        LANGFUSE_INGESTION_CLICKHOUSE_WRITE_INTERVAL_MS: ${LANGFUSE_INGESTION_CLICKHOUSE_WRITE_INTERVAL_MS:-}
        REDIS_HOST: ${REDIS_HOST:-redis}
        REDIS_PORT: ${REDIS_PORT:-6379}
        REDIS_AUTH: ${REDIS_AUTH:-myredissecret} # CHANGEME
        REDIS_TLS_ENABLED: ${REDIS_TLS_ENABLED:-false}
        REDIS_TLS_CA: ${REDIS_TLS_CA:-/certs/ca.crt}
        REDIS_TLS_CERT: ${REDIS_TLS_CERT:-/certs/redis.crt}
        REDIS_TLS_KEY: ${REDIS_TLS_KEY:-/certs/redis.key}
        EMAIL_FROM_ADDRESS: ${EMAIL_FROM_ADDRESS:-}
        SMTP_CONNECTION_URL: ${SMTP_CONNECTION_URL:-}

    langfuse-web:
      image: docker.io/langfuse/langfuse:3
      restart: always
      depends_on: *langfuse-depends-on
      ports:
        - 3000:3000
      environment:
        <<: *langfuse-worker-env
        NEXTAUTH_SECRET: mysecret # CHANGEME
        LANGFUSE_INIT_ORG_ID: 20250101
        LANGFUSE_INIT_ORG_NAME: orbitAI
        LANGFUSE_INIT_PROJECT_ID: 20250101
        LANGFUSE_INIT_PROJECT_NAME: xinference
        LANGFUSE_INIT_PROJECT_PUBLIC_KEY: pk-lf-8a79d84e-5537-47b7-86bb-ba36257684f2
        LANGFUSE_INIT_PROJECT_SECRET_KEY: sk-lf-d1d41a0b-672e-49c9-aece-f9a2b40828de
        LANGFUSE_INIT_USER_EMAIL: administrator@orbitai.com
        LANGFUSE_INIT_USER_NAME: administrator
        LANGFUSE_INIT_USER_PASSWORD: administrator

    clickhouse:
      image: docker.io/clickhouse/clickhouse-server
      restart: always
      user: "101:101"
      environment:
        CLICKHOUSE_DB: default
        CLICKHOUSE_USER: clickhouse
        CLICKHOUSE_PASSWORD: clickhouse # CHANGEME
      volumes:
        - langfuse_clickhouse_data:/var/lib/clickhouse
        - langfuse_clickhouse_logs:/var/log/clickhouse-server
      ports:
        - 127.0.0.1:8123:8123
        - 127.0.0.1:9000:9000
      healthcheck:
        test: wget --no-verbose --tries=1 --spider http://localhost:8123/ping || exit 1
        interval: 5s
        timeout: 5s
        retries: 10
        start_period: 1s

    minio:
      image: docker.io/minio/minio
      restart: always
      entrypoint: sh
      # create the 'langfuse' bucket before starting the service
      command: -c 'mkdir -p /data/langfuse && minio server --address ":9000" --console-address ":9001" /data'
      environment:
        MINIO_ROOT_USER: minio
        MINIO_ROOT_PASSWORD: miniosecret # CHANGEME
      ports:
        - 9090:9000
        - 127.0.0.1:9091:9001
      volumes:
        - langfuse_minio_data:/data
      healthcheck:
        test: ["CMD", "mc", "ready", "local"]
        interval: 1s
        timeout: 5s
        retries: 5
        start_period: 1s

    redis:
      image: docker.io/redis:7
      restart: always
      # CHANGEME: row below to secure redis password
      command: >
        --requirepass ${REDIS_AUTH:-myredissecret}
      ports:
        - 127.0.0.1:6379:6379
      healthcheck:
        test: ["CMD", "redis-cli", "ping"]
        interval: 3s
        timeout: 10s
        retries: 10

    postgres:
      image: docker.io/postgres:${POSTGRES_VERSION:-latest}
      restart: always
      healthcheck:
        test: ["CMD-SHELL", "pg_isready -U postgres"]
        interval: 3s
        timeout: 3s
        retries: 10
      environment:
        POSTGRES_USER: postgres
        POSTGRES_PASSWORD: postgres # CHANGEME
        POSTGRES_DB: postgres
      ports:
        - 5432:5432
      volumes:
        - langfuse_postgres_data:/var/lib/postgresql/data

  volumes:
    langfuse_postgres_data:
      driver: local
    langfuse_clickhouse_data:
      driver: local
    langfuse_clickhouse_logs:
      driver: local
    langfuse_minio_data:
      driver: local


启动服务
--------

.. code-block:: bash

   # 启动所有服务
   docker-compose up -d
   
   # 查看服务状态
   docker-compose ps
   
   # 查看服务日志
   docker-compose logs -f

验证部署
--------

**检查服务状态**：

.. code-block:: bash

   # 检查所有容器是否正常运行
   docker-compose ps
   
   # 检查各服务健康状态
   docker-compose exec langfuse-web curl -f http://localhost:3000/api/public/health
   docker-compose exec postgres pg_isready -U postgres
   docker-compose exec redis redis-cli ping

**访问Web界面**：

1. **打开浏览器**：访问 ``http://localhost:3000``
2. **首次登录**：使用配置的默认凭据
   
   * 邮箱：``administrator@orbitai.com``
   * 密码：``administrator``

3. **验证功能**：
   
   * 确认可以正常登录
   * 检查项目配置是否正确
   * 验证数据库连接状态

.. note::
   服务完全启动可能需要1-2分钟，请耐心等待所有容器状态变为健康。

设置Langfuse
============

配置连接
--------

在Xinference WebUI中配置Langfuse连接参数：

配置步骤
~~~~~~~~

1. **访问Xinference WebUI**：打开浏览器访问 ``http://<xinference-ip>:8000``
2. **进入设置页面**：点击右上角设置按钮
3. **选择链路配置**：选择"链路"标签页
4. **配置连接参数**：填写Langfuse服务信息

配置参数
~~~~~~~~

**同机部署（默认配置）**：

* **主机地址**：``http://localhost:3000``
* **项目公钥**：``pk-lf-8a79d84e-5537-47b7-86bb-ba36257684f2``
* **项目私钥**：``sk-lf-d1d41a0b-672e-49c9-aece-f9a2b40828de``

**跨机部署配置**：

如果Langfuse与Xinference不在同一台机器：

* **主机地址**：``http://<langfuse-server-ip>:3000``
* **项目公钥**：保持不变或使用自定义项目的公钥
* **项目私钥**：保持不变或使用自定义项目的私钥

.. important::
   **配置注意事项**：
   
   * 确保Xinference服务可以访问Langfuse服务地址
   * 如果修改了Docker Compose中的端口，需要相应调整主机地址
   * 生产环境建议创建专用的项目和密钥对

测试连接
~~~~~~~~

配置完成后，可以通过以下方式验证连接：

1. **保存配置**：点击保存按钮
2. **执行模型调用**：进行一次模型推理测试
3. **检查Langfuse**：在Langfuse界面查看是否有新的调用记录

模型调用监控
============

概览页面
--------

模型调用监控页面提供以下功能：

.. note::
   * 页面已实现轮询逻辑，无需手动刷新
   * 模型调用显示的是今日各个模型调用次数
   * tokens每日总数变化为最近一周，如需查看往日数据，请移步至 监控运维->模型调用

主要指标
--------

.. note::
   * 右上角支持日期筛选
   * 提供指标：大模型调用次数总数及各个模型调用次数、输入/输出tokens总数及各个模型输入/输出tokens总数、大模型每日调用次数变化、tokens每日总数变化

监控指标包括：

**调用统计**
  * 大模型调用次数总数
  * 各个模型调用次数分布
  * 大模型每日调用次数变化趋势

**Token统计**
  * 输入tokens总数
  * 输出tokens总数  
  * 各个模型输入/输出tokens分布
  * tokens每日总数变化趋势

链路状态
========

链路追踪功能提供详细的调用链路信息：

.. note::
   * 数据来源：运行实例详情 / 批处理
   * 链路列表：支持日期/User筛选，查看某链路详情

功能特性：

* **日期筛选**：按时间范围查看链路记录
* **用户筛选**：按用户维度分析调用情况
* **详情查看**：点击链路可查看完整调用详情

链路详情
========

链路详情页面提供两种展示格式：

展示格式
--------

**Tree格式**
  以树状结构展示调用链路层次关系

**Timeline格式**  
  以时间线形式展示调用的时序关系

详情信息
--------

.. note::
   * 两种展示方式Tree/Timeline
   * 详情数据：Latency，tokens输入/输出/总计，模型实例名称，对话的输入/输出，Metadata等
   * 支持Pretty/JSON格式转换

每个链路详情包含：

**性能指标**
  * **Latency**：调用延迟时间
  * **Tokens**：输入/输出/总计token数量

**调用信息**
  * **模型实例名称**：使用的具体模型实例
  * **输入内容**：用户的输入prompt
  * **输出内容**：模型的响应结果

**元数据**
  * **Metadata**：调用的附加信息
  * **时间戳**：精确的调用时间
  * **用户信息**：调用者标识

数据格式
--------

支持两种数据展示格式：

* **Pretty格式**：格式化的易读显示
* **JSON格式**：原始的JSON数据结构

使用场景
========

性能优化
--------

* 通过延迟统计识别性能瓶颈
* 分析token使用效率
* 监控模型响应时间趋势

调试分析
--------

* 查看完整的输入输出内容
* 分析调用链路中的异常
* 追踪特定用户的使用模式

成本管理
--------

* 统计各模型的token消耗
* 分析成本分布和趋势
* 优化模型选择策略

故障排除
========

常见问题
--------

1. **Langfuse服务无法启动**
   
   **可能原因**：
   * Docker或Docker Compose版本过低
   * 端口被占用
   * 磁盘空间不足
   * 内存不足
   
   **解决方案**：
   
   .. code-block:: bash
   
      # 检查Docker版本
      docker --version
      docker-compose --version
      
      # 检查端口占用
      netstat -tlnp | grep -E "(3000|5432|6379|8123|9000)"
      
      # 检查磁盘空间
      df -h
      
      # 查看容器日志
      docker-compose logs langfuse-web
      docker-compose logs postgres

2. **Xinference无法连接Langfuse**
   
   **可能原因**：
   * 网络连通性问题
   * 配置参数错误
   * 防火墙阻拦
   
   **解决方案**：
   
   .. code-block:: bash
   
      # 测试网络连通性
      curl -f http://<langfuse-ip>:3000/api/public/health
      
      # 检查Xinference配置
      # 在Xinference WebUI设置中验证Langfuse连接参数

3. **链路数据不显示**
   
   **可能原因**：
   * Langfuse配置未生效
   * 模型调用异常
   * 数据库连接问题
   
   **解决方案**：
   
   .. code-block:: bash
   
      # 检查Langfuse服务状态
      docker-compose exec langfuse-web curl -f http://localhost:3000/api/public/health
      
      # 检查数据库连接
      docker-compose exec postgres pg_isready -U postgres
      
      # 重启Xinference服务以重新加载配置

4. **性能问题**
   
   **可能原因**：
   * 资源不足
   * 数据库性能瓶颈
   * 网络延迟
   
   **解决方案**：
   * 增加系统内存
   * 优化数据库配置
   * 使用本地部署减少网络延迟

维护建议
--------

**定期维护**：
* 定期清理旧的链路数据
* 监控磁盘使用情况
* 备份重要的配置和数据

**性能优化**：
* 根据使用量调整数据库配置
* 考虑使用外部高性能数据库
* 定期更新到最新版本

更多详细的故障排除方案请参考：:doc:`troubleshooting`

相关文档
========

* :doc:`index` - 镜像使用总览
* :doc:`nvidia` - Nvidia系列镜像使用
* :doc:`multi_deployment` - 多机部署配置
* :doc:`kubernetes` - K8s部署配置
* :doc:`performance` - 性能测试指南
* :doc:`troubleshooting` - 故障排除指南

.. note::
   **部署建议**：
   
   * 建议在Xinference服务稳定运行后再部署Langfuse
   * 生产环境请修改所有默认密码和密钥
   * 定期备份Langfuse数据以防数据丢失
   * 如遇问题，请优先查看容器日志进行排查
