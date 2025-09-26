.. _kubernetes_deployment:

================
在 K8s 上部署
================

本文档介绍如何在Kubernetes环境中部署Xinference企业版。

.. contents:: 目录
   :local:
   :depth: 2

前置准备
========

创建用于私有镜像拉取的 Docker Registry Secret
----------------------------------------------

.. code-block:: bash

   kubectl create secret docker-registry xinference-regcred \
     --docker-server=registry.cn-hangzhou.aliyuncs.com \
     --docker-username=qin@qinxuye.me \
     --docker-password=cre.uwd3nyn4UDM6fzm \
     --docker-email=qin@qinxuye.me \
     --namespace=xinference

配置文件
========

准备 values-xinf-enterprise.yaml 文件
--------------------------------------

.. code-block:: yaml

   ###############################################################################################
   #
   # Xinference Enterprise deployment configuration
   # Two workers, each using one GPU
   #
   ###############################################################################################

   # Common configurations
   config:
     xinference_image: "registry.cn-hangzhou.aliyuncs.com/xinference-prod/xinference-prod:0.0.11-nvidia"
     curl_image: curlimages/curl:8.8.0
     image_pull_policy: "IfNotPresent"
     imagePullSecrets:
       - name: xinference-regcred
     worker_num: 2  # 根据实际情况调整 worker 的个数
     model_src: "modelscope"
     persistence:
       enabled: true
       mountPath: "/data"
     extra_envs: {}

   # Storage configuration
   storageClass:
     name: local-storage
     spec:
       provisioner: kubernetes.io/no-provisioner
       volumeBindingMode: WaitForFirstConsumer

   pv:
     accessModes:
       - ReadWriteMany
     capacity:
       storage: 500Gi
     hostPath:
       path: /mnt/xinference
     persistentVolumeReclaimPolicy: Retain
     storageClassName: "local-storage"

   pvc:
     accessModes:
       - ReadWriteMany
     sharedVolumeClaim:
       storageRequest: 500Gi
     storageClassName: "local-storage"
     volumeMode: "Filesystem"

   # Service configurations
   serviceWeb:
     ports:
     - name: frontend-port
       nodePort: 30003
       port: 8000
       protocol: TCP
       targetPort: 8000
     - name: api-port
       nodePort: 30004                                                                                                                                                                                                                               
       port: 9997                                                                                                                                                                                                                                      
       protocol: TCP                                                                                                                                                                                                                                   
       targetPort: 9997
     type: NodePort

   serviceSupervisor:
     ports:
     - name: service-supervisor-oscar
       port: 9999
       protocol: TCP
       targetPort: 9999
     - name: service-supervisor-web
       port: 9997
       protocol: TCP
       targetPort: 9997
     type: ClusterIP

   serviceWorker:
     ports:
     - port: 30001
       protocol: TCP
       targetPort: 30001
     type: ClusterIP

   xinferenceSupervisor:
     supervisor:
       command:
         - /bin/sh
         - -c
         - "/opt/projects/xinf-enterprise.sh --host $(POD_IP) --port 30004 && xinference-supervisor --host $(POD_IP) --port 9997 --log-level debug"
       ports:
         - containerPort: 9997
           name: web
         - containerPort: 9999
           name: oscar
       resources:
         requests:
           cpu: "1"
           memory: 4Gi

   xinferenceWorker:
     strategy:
       type: Recreate
     worker:
       initContainers:
         command: [ 'sh', '-c', "until curl -v http://service-supervisor:9997/v1/address; do echo waiting for supervisor; sleep 1; done" ]
       args:
       - -e
       - http://service-supervisor:9997
       - --host
       - $(POD_IP)
       - --worker-port
       - "30001"
       - --log-level
       - debug
       ports:
         - containerPort: 30001
       resources:  # 根据实际情况调整资源
         requests:
           cpu: "2"
           memory: 8Gi
         limits:
           nvidia.com/gpu: "1"

配置注意点
----------

* Worker 个数在 config 里配置；worker 使用的资源在 xinferenceWorker.worker.resources 里定义。包括 CPU、GPU 以及内存大小。
* ``/opt/projects/xinf-enterprise.sh --host $(POD_IP) --port 30004`` 是 Xinference 企业版前端（内部端口 8000，对外映射为 30003）需要连接的后端地址，当 Xinference API（端口9997，默认映射到对外地址是 30004）暴露后，需要将这里的 host 和 port 指定成对外地址。

部署步骤
========

创建 Xinference helm charts 服务
---------------------------------

.. code-block:: bash

   # add repo
   helm repo add xinference https://xorbitsai.github.io/xinference-helm-charts

   # update indexes and query xinference versions
   helm repo update
   helm search repo xinference/xinference --devel --versions

   # install xinference
   helm install xinference xinference/xinference -n xinference \
     --version 0.0.2-v1.3.1.post1 \
     -f values-xinf-enterprise.yaml

验证部署
========

使用如下命令看 Xinference supervisor 和 worker 的启动情况：

.. code-block:: bash

   kubectl get pods -n xinference

访问服务
========

根据 values-xinf-enterprise.yaml，默认 XInference 前端对外配置在 supervisor_ip:30003，API 地址在 supervisor_ip:30004。访问 http://supervisor_ip:30003 即可打开 Xinference 企业版服务地址。（supervisor_ip 替换成真实 IP）

相关文档
========

* :doc:`multi_deployment` - 多机部署配置
* :doc:`langfuse` - 企业版链路日志使用
* :doc:`nvidia` - Nvidia系列镜像使用
* :doc:`mindie` - MindIE系列镜像使用
* :doc:`hygon` - 海光系列镜像使用
