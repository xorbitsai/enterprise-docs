.. _mindie_series:

============
MindIE系列
============

本文档介绍如何使用Xinference的MindIE系列镜像，适用于华为昇腾NPU环境。

.. contents:: 目录
   :local:
   :depth: 2

版本信息
========

* Python版本：3.10
* CANN版本：8.0.rc2
* 操作系统版本：ubuntu_22.04
* mindie_1.0.RC2

使用说明
========

依赖
----

310I DUO
~~~~~~~~

* 驱动：Ascend-hdk-310p-npu-driver_24.1.rc2_linux-aarch64.run
* 固件：Ascend-hdk-310p-npu-firmware_7.3.0.1.231.run

910B
~~~~

* 驱动：Ascend-hdk-910b-npu-driver_24.1.rc2_linux-aarch64.run
* 固件：Ascend-hdk-910b-npu-firmware_7.3.0.1.231.run

将run包下载到宿主机上，运行如下命令安装驱动和固件：

.. code-block:: bash

   chmod +x Ascend-hdk-910b-npu-driver_24.1.rc2_linux-aarch64.run  
   ./Ascend-hdk-910b-npu-driver_24.1.rc2_linux-aarch64.run --full

完成安装后输出successfully即安装完成，固件安装方式相同。

.. warning::
   * 当Mindie无法正常启动时，请检查驱动和固件版本是否一致。
   * 驱动和固件请安装在宿主机，通过挂载的方式载入docker容器。
   * 升级版本时，请先安装firmware固件再安装driver驱动。

拉取镜像
--------

310I DUO
~~~~~~~~

.. code-block:: bash

   docker login --username=qin@qinxuye.me registry.cn-hangzhou.aliyuncs.com
   # 镜像仓库密码: cre.uwd3nyn4UDM6fzm
   docker pull registry.cn-hangzhou.aliyuncs.com/xinference-prod/xinference-prod:0.0.13.post1-310p

910B
~~~~

.. code-block:: bash

   docker login --username=qin@qinxuye.me registry.cn-hangzhou.aliyuncs.com
   # 镜像仓库密码: cre.uwd3nyn4UDM6fzm
   docker pull registry.cn-hangzhou.aliyuncs.com/xinference-prod/xinference-prod:0.0.13-910b

.. note::
   **镜像仓库访问说明**：
   
   * 用户名：``qin@qinxuye.me``
   * 密码：``cre.uwd3nyn4UDM6fzm``
   * 仓库地址：``registry.cn-hangzhou.aliyuncs.com``
   
   这是访问Xinference企业版镜像仓库的凭据。登录成功后即可拉取相应的镜像。

启动指令示例
------------

.. code-block:: bash

   docker run --name MindIE-Xinf -it \
   -d \
   --net=host \
   --shm-size=500g \
   --privileged=true \
   -w /opt/projects \
   --device=/dev/davinci_manager \
   --device=/dev/hisi_hdc \
   --device=/dev/devmm_svm \
   --entrypoint=bash \
   -v /usr/local/Ascend/driver:/usr/local/Ascend/driver \
   -v /usr/local/dcmi:/usr/local/dcmi \
   -v /usr/local/bin/npu-smi:/usr/local/bin/npu-smi \
   -v /usr/local/sbin:/usr/local/sbin \
   -v /home:/home \
   -v /root:/root/model \
   -v /tmp:/tmp \
   -v </your/home/path>/.xinference:/root/.xinference \
   -v </your/home/path>/.cache/huggingface:/root/.cache/huggingface \
   -v </your/home/path>/.cache/modelscope:/root/.cache/modelscope \
   -e http_proxy=$http_proxy \
   -e https_proxy=$https_proxy \
   registry.cn-hangzhou.aliyuncs.com/xinference-prod/xinference-prod:0.0.13-910b

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

支持模型
========

在选择模型运行引擎时，推荐使用Mindie模型，推理速度更快，其他引擎推理速度较慢，不推荐使用。

大语言模型
----------

目前Mindie大语言模型支持：

* baichuan-chat
* baichuan-2-chat
* chatglm3
* deepseek-chat
* deepseek-coder-instruct
* llama-3-instruct
* mistral-instruct-v0.3
* telechat
* Yi-chat
* Yi-1.5-chat
* qwen-chat
* qwen1.5-chat
* codeqwen1.5-chat
* qwen2-instruct
* csg-wukong-chat-v0.1
* qwen2.5 系列（qwen2.5-instruct, qwen2.5-coder-instruct 等）

Embedding 模型
--------------

* bge-large-zh-v1.5

Rerank 模型
-----------

* bge-reranker-large

相关文档
========

* :doc:`license` - 证书更新说明
* :doc:`performance` - 性能测试指南
* :doc:`multi_deployment` - 多机部署配置
* :doc:`langfuse` - 企业版链路日志使用
* :doc:`kubernetes` - K8s部署配置
