.. _hygon_series:

============
海光系列
============

本文档介绍如何使用Xinference的海光系列镜像，适用于海光DCU环境。

.. contents:: 目录
   :local:
   :depth: 2

使用说明
========

拉取镜像
--------

.. code-block:: bash

   docker login --username=qin@qinxuye.me registry.cn-hangzhou.aliyuncs.com
   # 镜像仓库密码: cre.uwd3nyn4UDM6fzm
   docker pull registry.cn-hangzhou.aliyuncs.com/xinference-prod/xinference-prod:0.0.12-dcu

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
   --name Xinf \
   --network host \
   --shm-size 500g \
   --privileged \
   --device=/dev/kfd \
   --device=/dev/dri \
   --group-add video \
   --cap-add=SYS_PTRACE \
   --security-opt seccomp=unconfined \
   --restart unless-stopped \
   -v /opt/hyhal:/opt/hyhal:ro \
   -v </your/home/path>/.xinference:/root/.xinference \
   -v </your/home/path>/.cache/huggingface:/root/.cache/huggingface \
   -v </your/home/path>/.cache/modelscope:/root/.cache/modelscope \
   registry.cn-hangzhou.aliyuncs.com/xinference-prod/xinference-prod:0.0.12-dcu /bin/bash

.. important::
   **路径配置说明**：
   
   请将 ``</your/home/path>`` 替换为你的实际存储路径。可以选择：
   
   * **主目录**：``/home/username`` (默认)
   * **数据盘**：``/data`` (推荐用于大容量存储)
   * **自定义路径**：任何有足够空间的目录
   
   参考Nvidia系列文档中的详细配置示例。

启动Xinference
--------------

启动容器后，进入容器/opt/projects目录下，执行以下命令：

.. code-block:: bash

   ./xinf-enterprise.sh --host <your-machine-ip> --port <your-port> && \
   XINFERENCE_MODEL_SRC=modelscope xinference-local --host <your-machine-ip> --port <your-port> --log-level debug

.. important::
   **IP地址和端口配置**：
   
   请将 ``<your-machine-ip>`` 和 ``<your-port>`` 替换为你的实际机器IP地址和端口号。
   详细配置示例请参考 :doc:`nvidia` 文档中的"IP地址和端口配置"部分。

.. note::
   * ``./xinf-enterprise.sh`` 脚本用于启动nginx服务，以及将Xinf服务启动地址写入配置文件
   * 脚本详细参数说明请参考 :doc:`nvidia` 文档中的"xinf-enterprise.sh 脚本参数说明"部分
   * Xinf服务启动命令可以根据实际需求进行调整
   * host和port请根据自己设备情况自行调整

Xinf服务启动完成后，即可通过访问8000端口进入Xinf WebUI界面。

相关文档
========

* :doc:`license` - 证书更新说明
* :doc:`performance` - 性能测试指南
* :doc:`multi_deployment` - 多机部署配置
* :doc:`langfuse` - 企业版链路日志使用
* :doc:`kubernetes` - K8s部署配置
