.. _troubleshooting:

============
故障排除
============

本文档提供Xinference企业版常见问题的解决方案和故障排除指南。

.. contents:: 目录
   :local:
   :depth: 2

多机部署问题
============

Worker无法连接到Supervisor
--------------------------

**问题描述**：Worker节点无法成功连接到Supervisor节点

**可能原因及解决方案**：

1. **网络连通性问题**
   
   .. code-block:: bash
   
      # 测试网络连通性
      ping <supervisor-ip>
      
      # 测试端口连通性
      telnet <supervisor-ip> <supervisor-port>
      nc -zv <supervisor-ip> <supervisor-port>

2. **防火墙配置问题**
   
   .. code-block:: bash
   
      # CentOS/RHEL 防火墙配置
      sudo firewall-cmd --permanent --add-port=9997/tcp
      sudo firewall-cmd --permanent --add-port=8000/tcp
      sudo firewall-cmd --reload
      
      # Ubuntu 防火墙配置
      sudo ufw allow 9997/tcp
      sudo ufw allow 8000/tcp

3. **IP地址和端口配置错误**
   
   * 确认Supervisor启动时使用的IP地址和端口
   * 检查Worker连接命令中的Supervisor地址
   * 验证IP地址是否为实际的网络接口地址

4. **Supervisor服务未正常启动**
   
   .. code-block:: bash
   
      # 检查Supervisor进程
      ps aux | grep xinference-supervisor
      
      # 查看Supervisor日志
      docker logs <supervisor-container-name>

Web界面无法访问
---------------

**问题描述**：无法通过浏览器访问Xinference WebUI界面

**可能原因及解决方案**：

1. **nginx服务未启动**
   
   .. code-block:: bash
   
      # 检查nginx进程
      ps aux | grep nginx
      
      # 手动启动nginx（在容器内）
      ./xinf-enterprise.sh --host <supervisor-ip> --port <supervisor-port>

2. **端口冲突或被占用**
   
   .. code-block:: bash
   
      # 检查8000端口占用情况
      netstat -tlnp | grep 8000
      lsof -i :8000
      
      # 使用自定义nginx端口
      ./xinf-enterprise.sh --host <supervisor-ip> --port <supervisor-port> --listen-port 8080

3. **IP地址配置问题**
   
   * 确认访问的IP地址是否正确
   * 检查是否使用了内网IP但从外网访问
   * 验证容器的网络模式配置

单机部署问题
============

容器启动失败
------------

**问题描述**：Docker容器无法正常启动

**可能原因及解决方案**：

1. **GPU资源问题**
   
   .. code-block:: bash
   
      # 检查GPU状态
      nvidia-smi
      
      # 检查Docker GPU支持
      docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi

2. **内存不足**
   
   .. code-block:: bash
   
      # 检查系统内存
      free -h
      
      # 调整共享内存大小
      --shm-size=64g  # 根据实际情况调整

3. **存储空间不足**
   
   .. code-block:: bash
   
      # 检查磁盘空间
      df -h
      
      # 清理Docker缓存
      docker system prune -a

模型加载问题
------------

**问题描述**：模型下载或加载失败

**可能原因及解决方案**：

1. **网络连接问题**
   
   .. code-block:: bash
   
      # 配置代理（如需要）
      export http_proxy=http://proxy-server:port
      export https_proxy=http://proxy-server:port
      
      # 在Docker启动时添加代理
      -e http_proxy=$http_proxy \
      -e https_proxy=$https_proxy

2. **存储空间不足**
   
   * 确保模型存储目录有足够空间
   * 大模型通常需要几十GB空间
   * 检查挂载路径的磁盘使用情况

3. **权限问题**
   
   .. code-block:: bash
   
      # 检查目录权限
      ls -la /path/to/model/directory
      
      # 修复权限问题
      sudo chown -R 1000:1000 /path/to/model/directory

性能问题
========

推理速度慢
----------

**问题描述**：模型推理响应时间过长

**可能原因及解决方案**：

1. **GPU资源不足**
   
   .. code-block:: bash
   
      # 监控GPU使用情况
      nvidia-smi -l 1
      
      # 检查GPU内存使用
      nvidia-smi --query-gpu=memory.used,memory.total --format=csv

2. **模型配置问题**
   
   * 选择合适的模型大小
   * 调整批处理大小
   * 使用量化模型减少内存占用

3. **网络延迟**
   
   * 确保客户端与服务器网络连通良好
   * 考虑使用本地部署减少网络开销

内存使用过高
------------

**问题描述**：系统内存或GPU内存使用过高

**解决方案**：

1. **调整模型参数**
   
   * 使用较小的模型
   * 启用模型量化
   * 减少并发请求数量

2. **优化容器配置**
   
   .. code-block:: bash
   
      # 限制容器内存使用
      --memory=32g --memory-swap=32g

日志和调试
==========

查看详细日志
------------

.. code-block:: bash

   # 查看容器日志
   docker logs -f <container-name>
   
   # 查看Xinference服务日志
   # 在容器内启动服务时添加详细日志级别
   xinference-local --log-level debug
   xinference-supervisor --log-level debug
   xinference-worker --log-level debug

常用调试命令
------------

.. code-block:: bash

   # 检查服务状态
   curl http://<supervisor-ip>:<supervisor-port>/v1/models
   
   # 检查集群节点状态
   curl http://<supervisor-ip>:<supervisor-port>/v1/cluster/workers
   
   # 测试模型推理
   curl -X POST http://<supervisor-ip>:<supervisor-port>/v1/chat/completions \
     -H "Content-Type: application/json" \
     -d '{"model": "model-name", "messages": [{"role": "user", "content": "Hello"}]}'

获取帮助
========

如果以上解决方案无法解决您的问题，请：

1. **收集信息**：
   
   * 系统环境信息（OS、Docker版本、GPU型号等）
   * 错误日志和详细错误信息
   * 使用的镜像版本和配置参数

2. **联系支持**：
   
   * 查看官方文档获取最新信息
   * 联系技术支持团队
   * 提供详细的问题描述和环境信息

相关文档
========

* :doc:`multi_deployment` - 多机部署配置
* :doc:`nvidia` - Nvidia系列镜像使用
* :doc:`performance` - 性能测试指南
* :doc:`kubernetes` - K8s部署配置
