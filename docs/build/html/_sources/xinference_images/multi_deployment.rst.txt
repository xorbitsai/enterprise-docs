.. _multi_deployment:

========================
Xinference 多机部署
========================

本文档介绍如何在多台机器上部署Xinference集群服务。

.. contents:: 目录
   :local:
   :depth: 2

前置要求
========

系统要求
--------

**每台机器都需要满足**：

* **硬件**：NVIDIA GPU（支持CUDA计算能力3.5+）
* **内存**：建议16GB以上系统内存
* **存储**：至少50GB可用磁盘空间
* **网络**：稳定的局域网连接，各节点间可互相访问

**软件要求**：

* **操作系统**：Linux (Ubuntu 20.04+, CentOS 7+)
* **Docker**：Docker 20.10+
* **NVIDIA Driver**：版本450+
* **NVIDIA Container Toolkit**：用于Docker GPU支持

网络规划
--------

**端口规划**：

* **Supervisor节点**：需要开放服务端口（如9997）和WebUI端口（8000）
* **Worker节点**：需要能够访问Supervisor的服务端口
* **防火墙**：确保相关端口在防火墙中开放

**IP地址规划示例**：

* Supervisor：192.168.1.100
* Worker-01：192.168.1.101  
* Worker-02：192.168.1.102

概述
====

在Xinf服务中，Supervisor负责调度Worker的执行，因此在集群服务中，需要1个Supervisor和1个及以上的Worker来组成多机服务。

架构说明
--------

* **Supervisor节点**：负责任务调度和管理，提供Web界面访问
* **Worker节点**：负责实际的模型推理计算
* **集群要求**：1个Supervisor + 1个或多个Worker

启动Supervisor
==============

以nvidia系列镜像为例，如要启动Supervisor，需要通过以下命令来启动容器。

拉取镜像
--------

首先登录镜像仓库并拉取所需的镜像：

.. code-block:: bash

   docker login --username=qin@qinxuye.me registry.cn-hangzhou.aliyuncs.com
   # 镜像仓库密码: cre.uwd3nyn4UDM6fzm
   docker pull registry.cn-hangzhou.aliyuncs.com/xinference-prod/xinference-prod:0.2.2-nvidia

.. note::
   **镜像仓库访问说明**：
   
   * 用户名：``qin@qinxuye.me``
   * 密码：``cre.uwd3nyn4UDM6fzm``
   * 仓库地址：``registry.cn-hangzhou.aliyuncs.com``
   
   这是访问Xinference企业版镜像仓库的凭据。登录成功后即可拉取相应的镜像。

启动Supervisor容器
------------------

.. code-block:: bash

   docker run -it \
   --name xinference-supervisor \
   --network host \
   --gpus all \
   --shm-size=128g \
   --restart unless-stopped \
   -v </your/home/path>/.xinference:/root/.xinference \
   -v </your/home/path>/.cache/huggingface:/root/.cache/huggingface \
   -v </your/home/path>/.cache/modelscope:/root/.cache/modelscope \
   -e XINFERENCE_PROCESS_START_METHOD=spawn \
   -e XINFERENCE_PROMETHEUS_SRC=/opt/projects/prometheus \
   registry.cn-hangzhou.aliyuncs.com/xinference-prod/xinference-prod:0.2.2-nvidia /bin/bash

.. important::
   **路径配置说明**：
   
   请将 ``</your/home/path>`` 替换为你的实际存储路径。可以选择：
   
   * **主目录**：``/home/username`` 或 ``/Users/username``
   * **数据盘**：``/data`` 或 ``/mnt/data`` (推荐用于大容量存储)
   * **自定义路径**：任何有足够空间的目录
   
   详细配置示例请参考 :doc:`nvidia` 文档中的"路径配置说明"部分。

启动Supervisor服务
------------------

在进入容器xinference-supervisor后，可以执行以下两种方式来启动Supervisor服务。

方法一：机器上只启动Supervisor节点
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   ./xinf-enterprise.sh --host <supervisor-ip> --port <supervisor-port> && \
   xinference-supervisor --host <supervisor-ip> --port <supervisor-port> --log-level debug

.. important::
   **参数配置说明**：
   
   请将上述命令中的占位符替换为实际值：
   
   * ``<supervisor-ip>``：Supervisor节点的IP地址
   * ``<supervisor-port>``：Supervisor服务端口号
   
   **配置示例**：
   
   .. code-block:: bash
   
      # 局域网部署示例
      ./xinf-enterprise.sh --host 192.168.1.100 --port 9997 && \
      xinference-supervisor --host 192.168.1.100 --port 9997 --log-level debug
      
      # 使用自定义端口
      ./xinf-enterprise.sh --host 192.168.1.100 --port 8888 && \
      xinference-supervisor --host 192.168.1.100 --port 8888 --log-level debug

.. note::
   **访问说明**：
   
   * Supervisor服务启动成功后，可通过 ``http://<supervisor-ip>:8000`` 访问WebUI界面
   * 确保防火墙已开放相应端口（Supervisor端口 + 8000端口）
   * 其他Worker节点需要能够访问Supervisor的IP地址和端口

方法二：机器上同时启动Supervisor和Worker节点
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   ./xinf-enterprise.sh --host <supervisor-ip> --port <supervisor-port> && \
   xinference-local --host <supervisor-ip> --port <supervisor-port> --log-level debug

.. important::
   **参数配置说明**：
   
   此方法在单台机器上同时运行Supervisor和Worker功能，适用于单机多GPU场景。
   
   **配置示例**：
   
   .. code-block:: bash
   
      # 单机部署示例
      ./xinf-enterprise.sh --host 192.168.1.100 --port 9997 && \
      xinference-local --host 192.168.1.100 --port 9997 --log-level debug

.. note::
   **使用场景**：
   
   * 适用于单台高性能服务器，具有多个GPU
   * 既提供调度管理功能，又直接参与模型推理
   * 简化部署，减少网络通信开销

启动Worker
===========

同样以nvidia系列镜像为例，如要启动Worker，启动命令与Supervisor类似。

启动Worker容器
--------------

.. code-block:: bash

   docker run -it \
   --name xinference-worker-01 \
   --network host \
   --gpus all \
   --shm-size=128g \
   --restart unless-stopped \
   -v </your/home/path>/.xinference:/root/.xinference \
   -v </your/home/path>/.cache/huggingface:/root/.cache/huggingface \
   -v </your/home/path>/.cache/modelscope:/root/.cache/modelscope \
   -e XINFERENCE_PROCESS_START_METHOD=spawn \
   -e XINFERENCE_PROMETHEUS_SRC=/opt/projects/prometheus \
   registry.cn-hangzhou.aliyuncs.com/xinference-prod/xinference-prod:0.2.2-nvidia /bin/bash

.. important::
   **路径配置说明**：
   
   Worker节点的路径配置与Supervisor节点相同。请将 ``</your/home/path>`` 替换为你的实际存储路径。
   详细配置示例请参考 :doc:`nvidia` 文档中的"路径配置说明"部分。

启动Worker服务
--------------

在进入容器xinference-worker-01后，需要通过以下命令启动Worker服务。

.. code-block:: bash

   xinference-worker -e "http://<supervisor-ip>:<supervisor-port>" --host <worker-ip> --log-level debug

.. important::
   **参数配置说明**：
   
   请将上述命令中的占位符替换为实际值：
   
   * ``<supervisor-ip>``：Supervisor节点的IP地址
   * ``<supervisor-port>``：Supervisor服务端口号
   * ``<worker-ip>``：当前Worker节点的IP地址
   
   **配置示例**：
   
   .. code-block:: bash
   
      # Worker节点连接到Supervisor
      xinference-worker -e "http://192.168.1.100:9997" --host 192.168.1.101 --log-level debug
      
      # 多个Worker节点示例
      # Worker-01: 192.168.1.101
      xinference-worker -e "http://192.168.1.100:9997" --host 192.168.1.101 --log-level debug
      
      # Worker-02: 192.168.1.102  
      xinference-worker -e "http://192.168.1.100:9997" --host 192.168.1.102 --log-level debug

.. note::
   **网络要求**：
   
   * Worker节点必须能够访问Supervisor节点的IP和端口
   * 确保网络连通性和防火墙配置正确
   * 建议在同一局域网内部署，减少网络延迟

部署验证
========

完成上述操作以后，就实现了Xinf的多机部署。以下步骤帮助您验证部署是否成功。

服务状态检查
------------

**检查容器状态**：

.. code-block:: bash

   # 在Supervisor节点上
   docker ps | grep xinference-supervisor
   docker logs xinference-supervisor
   
   # 在Worker节点上  
   docker ps | grep xinference-worker
   docker logs xinference-worker-01

**检查网络连通性**：

.. code-block:: bash

   # 从Worker节点测试到Supervisor的连通性
   curl http://<supervisor-ip>:<supervisor-port>/v1/cluster/workers
   
   # 检查端口是否正常监听
   netstat -tlnp | grep 9997  # Supervisor端口
   netstat -tlnp | grep 8000  # WebUI端口

访问Web界面
-----------

1. **打开浏览器**，访问：``http://<supervisor-ip>:8000``
2. **登录界面**：如果配置了认证，请使用相应凭据登录
3. **验证功能**：确认可以正常访问各个功能模块

检查集群状态
------------

在Web界面中验证以下内容：

**节点管理页面**：
* Supervisor节点状态显示为"在线"
* 所有Worker节点都显示在节点列表中
* 各节点的资源使用情况正常显示
* 节点连接状态为"已连接"

**模型管理**：
* 可以查看可用模型列表
* 尝试在不同Worker节点上加载模型
* 验证模型负载均衡功能

**API测试**：

.. code-block:: bash

   # 测试集群API
   curl http://<supervisor-ip>:9997/v1/cluster/workers
   
   # 测试模型推理
   curl -X POST http://<supervisor-ip>:9997/v1/chat/completions \
     -H "Content-Type: application/json" \
     -d '{"model": "model-name", "messages": [{"role": "user", "content": "Hello"}]}'

部署架构示例
============

典型的多机部署架构如下：

.. code-block:: text

   ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
   │   Supervisor    │    │    Worker-01    │    │    Worker-02    │
   │  192.168.1.100  │    │  192.168.1.101  │    │  192.168.1.102  │
   │   Port: 9997    │◄──►│                 │    │                 │
   │   Web: 8000     │    │                 │    │                 │
   └─────────────────┘    └─────────────────┘    └─────────────────┘

部署流程总结
============

完整的多机部署流程如下：

**准备阶段**：
1. 确认所有节点满足系统要求
2. 规划IP地址和端口分配
3. 配置防火墙和网络连通性

**部署阶段**：
1. 在所有节点上拉取镜像
2. 启动Supervisor容器和服务
3. 启动Worker容器和服务
4. 验证节点连接状态

**验证阶段**：
1. 检查容器和服务状态
2. 访问WebUI界面
3. 验证集群功能
4. 进行API测试

**运维建议**：
* 定期检查节点状态和资源使用情况
* 监控网络连接质量
* 及时处理异常节点
* 参考故障排除文档解决问题

相关文档
========

* :doc:`index` - 镜像使用总览
* :doc:`nvidia` - Nvidia系列镜像使用
* :doc:`kubernetes` - K8s部署配置
* :doc:`troubleshooting` - 故障排除指南

.. note::
   * 如需单机部署，请参考文档：:doc:`index`
   * 如遇到部署问题，请参考：:doc:`troubleshooting`
