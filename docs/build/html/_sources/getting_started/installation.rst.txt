.. _installation:

============
Installation
============

Xinference can be installed with ``docker`` on Nvidia, NPU, GCU, and DCU.To run models using Xinference, you will need to pull the image corresponding to the type of device you intend to serve.



Nvidia
-------------------

To pull the Nvidia image, run the following command:

.. code-block:: bash

    docker login --username=qin@qinxuye.me registry.cn-hangzhou.aliyuncs.com
    Password: cre.uwd3nyn4UDM6fzm
    docker pull registry.cn-hangzhou.aliyuncs.com/xinference-prod/xinference-prod:0.0.10-nvidia


Run Command Example
^^^^^^^^^^^^^^^^^^^

To run the container, use the following command:

.. code-block:: bash

    docker run -it \
    --name Xinf \
    --network host \
    --gpus all \
    --restart unless-stopped \
    -v </your/home/path>/.xinference:/root/.xinference \
    -v </your/home/path>/.cache/huggingface:/root/.cache/huggingface \
    -v </your/home/path>/.cache/modelscope:/root/.cache/modelscope \
    registry.cn-hangzhou.aliyuncs.com/xinference-prod/xinference-prod:0.0.10-nvidia /bin/bash

Start Xinference
^^^^^^^^^^^^^^^^^^^

After starting the container, navigate to the `/opt/projects` directory inside the container and run the following command:

.. code-block:: bash

    ./xinf-enterprise.sh --host 192.168.10.197 --port 9997 && \
    XINFERENCE_MODEL_SRC=modelscope xinference-local --host 192.168.10.197 --port 9997 --log-level debug

The `./xinf-enterprise.sh` script is used to start the Nginx service and write the Xinf service startup address to the configuration file.

The Xinf service startup command can be adjusted according to actual requirements. The `host` and `port` should be adjusted according to your device's configuration.

Once the Xinf service is started, you can access the Xinf WebUI interface by visiting port 8000.

MindIE Series
-------------------

Version Information
^^^^^^^^^^^^^^^^^^^
- Python Version: 3.10
- CANN Version: 8.0.rc2
- Operating System Version: ubuntu_22.04
- mindie_1.0.RC2


Dependencies
^^^^^^^^^^^^^^^^^^^
For 310I DUO:
- Driver: Ascend-hdk-310p-npu-driver_24.1.rc2_linux-aarch64.run - `Download <https://obs-whaicc-fae-public.obs.cn-central-221.ovaijisuan.com/cann/mindie/1.0.RC2/310p/Ascend-hdk-310p-npu-driver_24.1.rc2_linux-aarch64.run>`_
- Firmware: Ascend-hdk-310p-npu-firmware_7.3.0.1.231.run - `Download <https://obs-whaicc-fae-public.obs.cn-central-221.ovaijisuan.com/cann/mindie/1.0.RC2/310p/Ascend-hdk-310p-npu-firmware_7.3.0.1.231.run>`_

For 910B:
- Driver: Ascend-hdk-910b-npu-driver_24.1.rc3_linux-aarch64.run - `Download <https://ascend-repo.obs.cn-east-2.myhuaweicloud.com/Ascend%20HDK/Ascend%20HDK%2024.1.RC3/Ascend-hdk-910b-npu-driver_24.1.rc3_linux-aarch64.run?response-content-type=application/octet-stream>`_
- Firmware: Ascend-hdk-910b-npu-firmware_7.5.0.1.129.run - `Download <https://ascend-repo.obs.cn-east-2.myhuaweicloud.com/Ascend%20HDK/Ascend%20HDK%2024.1.RC3/Ascend-hdk-910b-npu-firmware_7.5.0.1.129.run?response-content-type=application/octet-stream>`_

Download the `.run` packages to the host machine, and then run the following commands to install the drivers and firmware:

.. code-block:: bash

    chmod +x Ascend-hdk-910b-npu-driver_24.1.rc3_linux-aarch64.run
    ./Ascend-hdk-910b-npu-firmware_7.5.0.1.129.run --full

Once the installation is complete, the output should indicate "successfully," confirming the installation. The firmware installation method is the same.

When Mindie does not start properly, verify that the driver and firmware versions match. Both the driver and firmware must be installed on the host machine and loaded into the Docker container via mounting.

For version upgrades, install the firmware first, then the driver.

Pull the Image
^^^^^^^^^^^^^^^^^^^
For 310I DUO:

.. code-block:: bash

    docker login --username=qin@qinxuye.me registry.cn-hangzhou.aliyuncs.com
    Password: cre.uwd3nyn4UDM6fzm
    docker pull registry.cn-hangzhou.aliyuncs.com/xinference-prod/xinference-prod:0.0.10-310p

For 910B:

.. code-block:: bash

    docker login --username=qin@qinxuye.me registry.cn-hangzhou.aliyuncs.com
    Password: cre.uwd3nyn4UDM6fzm
    docker pull registry.cn-hangzhou.aliyuncs.com/xinference-prod/xinference-prod:0.0.10-910b

Run Command Example
^^^^^^^^^^^^^^^^^^^
To run the container, use the following command:

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
    registry.cn-hangzhou.aliyuncs.com/xinference-prod/xinference-prod:0.0.10-910b

Start Xinference
^^^^^^^^^^^^^^^^^^^
After starting the container, navigate to the `/opt/projects` directory inside the container and run the following command:

.. code-block:: bash

    ./xinf-enterprise.sh --host 192.168.10.197 --port 9997 && \
    XINFERENCE_MODEL_SRC=modelscope xinference-local --host 192.168.10.197 --port 9997 --log-level debug

The `./xinf-enterprise.sh` script starts the Nginx service and writes the Xinf service startup address to the configuration file.

The Xinf service startup command can be adjusted according to your needs. Adjust the `host` and `port` according to your device's configuration.

Once the Xinf service is started, you can access the Xinf WebUI by visiting port 8000.

Supported Models
^^^^^^^^^^^^^^^^^^^

When selecting a model execution engine, we recommend using the Mindie model for faster inference speed. Other engines may have slower inference speeds and are not recommended for use.

Currently, Mindie supports the following large language models:

- baichuan-chat
- baichuan-2-chat
- chatglm3
- deepseek-chat
- deepseek-coder-instruct
- llama-3-instruct
- mistral-instruct-v0.3
- telechat
- Yi-chat
- Yi-1.5-chat
- qwen-chat
- qwen1.5-chat
- codeqwen1.5-chat
- qwen2-instruct
- csg-wukong-chat-v0.1
- qwen2.5 series (qwen2.5-instruct, qwen2.5-coder-instruct, etc.)

Embedding Models:
- bge-large-zh-v1.5

Rerank Models:
- bge-reranker-large
