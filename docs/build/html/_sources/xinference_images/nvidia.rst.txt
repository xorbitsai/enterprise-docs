.. _nvidia_series:

============
Nvidia系列
============

本文档介绍如何使用Xinference的Nvidia系列镜像，适用于CUDA环境。

.. contents:: 目录
   :local:
   :depth: 2

系统要求
========

硬件要求
--------

* **GPU**：NVIDIA GPU（支持CUDA计算能力3.5+）
* **内存**：建议16GB以上系统内存
* **存储**：至少50GB可用磁盘空间（用于模型存储）
* **网络**：稳定的网络连接（用于模型下载）

软件要求
--------

* **操作系统**：Linux (Ubuntu 20.04+, CentOS 7+) 或 macOS
* **Docker**：Docker 20.10+ 
* **NVIDIA Driver**：版本450+
* **NVIDIA Container Toolkit**：用于Docker GPU支持

.. code-block:: bash

   # 验证GPU和Docker支持
   nvidia-smi
   docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi

使用说明
========

拉取镜像
--------

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

启动指令示例
------------

.. code-block:: bash

   docker run -it \
   --name xinference-nvidia \
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
   
   请将 ``</your/home/path>`` 替换为你的实际存储路径。可以选择以下位置：
   
   * **主目录**：``/home/username`` 或 ``/Users/username``
   * **数据盘**：``/data`` 或 ``/mnt/data`` (推荐用于大容量存储)
   * **自定义路径**：任何有足够空间的目录
   
   **配置示例**：
   
   .. code-block:: bash
   
      # 使用主目录 (Linux)
      -v /home/arthur/.xinference:/root/.xinference \
      -v /home/arthur/.cache/huggingface:/root/.cache/huggingface \
      -v /home/arthur/.cache/modelscope:/root/.cache/modelscope \
      
      # 使用主目录 (macOS)
      -v /Users/arthur/.xinference:/root/.xinference \
      -v /Users/arthur/.cache/huggingface:/root/.cache/huggingface \
      -v /Users/arthur/.cache/modelscope:/root/.cache/modelscope \
      
      # 使用数据盘 (推荐用于大模型)
      -v /data/xinference:/root/.xinference \
      -v /data/cache/huggingface:/root/.cache/huggingface \
      -v /data/cache/modelscope:/root/.cache/modelscope \
   
   .. tip::
      **存储建议**：
      
      * 模型文件通常较大(几GB到几十GB)，建议使用容量充足的磁盘
      * 如果有专门的数据盘(如 ``/data``)，优先使用数据盘存储
      * 确保选择的目录有足够的读写权限

启动Xinference
--------------

启动容器后，进入容器/opt/projects目录下，执行以下命令：

.. code-block:: bash

   ./xinf-enterprise.sh --host <your-machine-ip> --port <your-port> && \
   XINFERENCE_MODEL_SRC=modelscope xinference-local --host <your-machine-ip> --port <your-port> --log-level debug

.. important::
   **IP地址和端口配置**：
   
   请将上述命令中的占位符替换为实际值：
   
   * ``<your-machine-ip>``：替换为你的机器IP地址
   * ``<your-port>``：替换为你要使用的端口号
   
   **配置示例**：
   
   .. code-block:: bash
   
      # 使用本机IP和默认端口
      ./xinf-enterprise.sh --host 192.168.1.100 --port 9997 && \
      XINFERENCE_MODEL_SRC=modelscope xinference-local --host 192.168.1.100 --port 9997 --log-level debug
      
      # 使用自定义端口
      ./xinf-enterprise.sh --host 192.168.1.100 --port 8888 && \
      XINFERENCE_MODEL_SRC=modelscope xinference-local --host 192.168.1.100 --port 8888 --log-level debug
      
      # 本地开发环境
      ./xinf-enterprise.sh --host 127.0.0.1 --port 9997 && \
      XINFERENCE_MODEL_SRC=modelscope xinference-local --host 127.0.0.1 --port 9997 --log-level debug

xinf-enterprise.sh 脚本参数说明
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``xinf-enterprise.sh`` 脚本用于启动nginx服务并配置Xinf服务地址。使用方法：

.. code-block:: bash

   # 完整参数格式
   ./xinf-enterprise.sh --host <host> --port <port> [--listen-port <nginx_listen_port>]
   
   # 简写格式
   ./xinf-enterprise.sh -H <host> -P <port> [-L <nginx_listen_port>]
   
   # 查看帮助信息
   ./xinf-enterprise.sh --help

**参数说明**：

* ``--host`` / ``-H``：指定Xinference服务的主机地址
* ``--port`` / ``-P``：指定Xinference服务的端口号
* ``--listen-port`` / ``-L``：指定nginx监听端口（可选，默认8000）

**配置示例**：

.. code-block:: bash

   # 基本配置
   ./xinf-enterprise.sh --host 192.168.1.100 --port 9997
   
   # 指定nginx端口
   ./xinf-enterprise.sh --host 192.168.1.100 --port 9997 --listen-port 8080
   
   # 使用简写格式
   ./xinf-enterprise.sh -H 192.168.1.100 -P 9997 -L 8080

.. note::
   * ``./xinf-enterprise.sh`` 脚本用于启动nginx服务，以及将Xinf服务启动地址写入配置文件
   * Xinf服务启动命令可以根据实际需求进行调整
   * host和port请根据自己设备的实际IP地址和端口配置
   * nginx默认监听8000端口，可通过 ``--listen-port`` 参数自定义

Xinf服务启动完成后，即可通过访问nginx监听端口(默认8000)进入Xinf WebUI界面。

验证部署
========

服务状态检查
------------

.. code-block:: bash

   # 检查容器状态
   docker ps | grep xinference-nvidia
   
   # 查看服务日志
   docker logs xinference-nvidia
   
   # 检查服务端口
   netstat -tlnp | grep 8000

访问WebUI界面
-------------

1. **打开浏览器**，访问：``http://<your-machine-ip>:8000``
2. **验证功能**：
   
   * 查看模型列表
   * 尝试加载一个小模型进行测试
   * 检查节点状态和资源使用情况

3. **API测试**：

   .. code-block:: bash
   
      # 测试API连通性
      curl http://<your-machine-ip>:9997/v1/models
      
      # 测试模型推理（需要先加载模型）
      curl -X POST http://<your-machine-ip>:9997/v1/chat/completions \
        -H "Content-Type: application/json" \
        -d '{"model": "model-name", "messages": [{"role": "user", "content": "Hello"}]}'

常见问题
--------

如果遇到问题，请参考：

* :doc:`troubleshooting` - 详细的故障排除指南
* 检查GPU驱动和Docker配置
* 确认网络端口配置正确

相关文档
========

* :doc:`license` - 证书更新说明
* :doc:`performance` - 性能测试指南
* :doc:`multi_deployment` - 多机部署配置
* :doc:`langfuse` - 企业版链路日志使用
* :doc:`kubernetes` - K8s部署配置
* :doc:`troubleshooting` - 故障排除指南
