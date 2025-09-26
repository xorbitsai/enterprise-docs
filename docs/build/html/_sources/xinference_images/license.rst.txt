.. _license_management:

================
Xinf证书更新
================

本文档介绍如何更新Xinference企业版的证书。

.. contents:: 目录
   :local:
   :depth: 2

前置要求
========

在开始证书更新之前，请确保：

* Xinference服务已正常启动
* 可以访问WebUI界面（即使显示证书过期提示）
* 具有管理员权限
* 网络连接正常，可以访问API接口

概述
====

Xinference企业版需要有效的证书才能正常使用。首次部署或证书过期时，会出现以下情况：

* 访问WebUI界面时显示"License is expired."提示
* 部分功能受限或无法使用
* 需要获取设备信息并申请新证书

证书更新流程：

1. **获取设备信息**：通过API或WebUI获取MAC地址
2. **申请证书**：将设备信息发送给技术支持
3. **更新证书**：通过WebUI或API更新证书
4. **验证生效**：确认证书更新成功

获取设备信息
============

方法一：通过WebUI界面
--------------------

1. **访问WebUI**：打开浏览器访问 ``http://<your-ip>:8000``
2. **查看提示**：证书过期时会自动弹出对话框显示设备信息
3. **复制信息**：从对话框中复制MAC地址等设备信息

方法二：通过API接口
------------------

使用以下命令获取设备的MAC地址信息：

.. code-block:: bash

   curl --request GET 'http://<your-ip>:<your-port>/v1/license'

.. important::
   **参数说明**：
   
   * ``<your-ip>``：替换为Xinference服务的IP地址
   * ``<your-port>``：替换为Xinference服务端口（通常为9997）
   
   **示例**：
   
   .. code-block:: bash
   
      curl --request GET 'http://192.168.1.100:9997/v1/license'

**响应示例**：

.. code-block:: json

   {
       "message": "Request Successful.",
       "data": {
           "mac_address": "98:0E:27:AF:09:2D"
       }
   }

申请证书
========

获取设备信息后，需要向技术支持申请证书：

申请流程
--------

1. **收集信息**：
   
   * 设备MAC地址
   * 公司名称和联系信息
   * 使用用途说明
   * 预期使用期限

2. **提交申请**：
   
   * 发送邮件给技术支持团队
   * 或通过客服渠道提交申请
   * 包含完整的设备信息和申请说明

3. **获取证书**：
   
   * 技术支持会生成对应的证书文件
   * 通过邮件或其他安全方式发送证书
   * 证书通常为Base64编码的字符串

更新证书
========

获得证书后，可以通过以下两种方式更新：

方法一：通过WebUI界面
--------------------

1. **访问WebUI**：打开浏览器访问 ``http://<your-ip>:8000``
2. **打开证书对话框**：如果证书已过期，会自动弹出；否则可在设置中找到
3. **输入证书**：将获得的证书字符串粘贴到输入框中
4. **提交更新**：点击确认按钮完成更新
5. **验证结果**：页面会显示更新结果

方法二：通过API接口
------------------

使用以下命令通过API更新证书：

.. code-block:: bash

   curl --request POST 'http://<your-ip>:<your-port>/v1/license' \
   --header 'Content-Type: application/json' \
   --data-raw '{
       "license_key": "<your-license-key>"
   }'

.. important::
   **参数说明**：
   
   * ``<your-ip>``：替换为Xinference服务的IP地址
   * ``<your-port>``：替换为Xinference服务端口（通常为9997）
   * ``<your-license-key>``：替换为获得的实际证书字符串
   
   **示例**：
   
   .. code-block:: bash
   
      curl --request POST 'http://192.168.1.100:9997/v1/license' \
      --header 'Content-Type: application/json' \
      --data-raw '{
          "license_key": "a0df6K-hhOdeVM5tht2yuL-ddOhScqVJ8UeMy1aOGgL7WvGg93J7GgatSWaOMujL8NGE8oPJq6tDmMBYDuQ_xA=="
      }'

**响应示例**：

.. code-block:: json

   {
       "message": "Request Successful."
   }

.. note::
   出现"Request Successful"即表示更新成功，可以正常访问Xinf服务了。

验证证书生效
============

更新证书后，建议进行以下验证：

功能验证
--------

1. **刷新WebUI**：重新加载浏览器页面
2. **检查状态**：确认不再显示证书过期提示
3. **测试功能**：尝试访问各个功能模块
4. **模型加载**：测试模型加载和推理功能

API验证
-------

.. code-block:: bash

   # 检查证书状态
   curl --request GET 'http://<your-ip>:<your-port>/v1/license'
   
   # 测试模型列表API
   curl --request GET 'http://<your-ip>:<your-port>/v1/models'

默认凭据
========

WebUI访问凭据
-------------

* **用户名**：``administrator``
* **密码**：``administrator``

.. warning::
   **安全建议**：
   
   * 首次登录后请立即修改默认密码
   * 使用强密码，包含字母、数字和特殊字符
   * 定期更换密码以确保安全

常见问题
========

证书更新失败
------------

如果证书更新失败，请检查：

* 证书字符串是否完整且正确
* 网络连接是否正常
* 服务是否正常运行
* 是否有足够的权限

证书仍然显示过期
----------------

如果更新后仍显示过期：

* 清除浏览器缓存并重新访问
* 重启Xinference服务
* 检查系统时间是否正确
* 联系技术支持确认证书有效性

更多问题解决方案请参考：:doc:`troubleshooting`

相关文档
========

* :doc:`nvidia` - Nvidia系列镜像使用
* :doc:`mindie` - MindIE系列镜像使用
* :doc:`hygon` - 海光系列镜像使用
* :doc:`multi_deployment` - 多机部署配置
* :doc:`troubleshooting` - 故障排除指南

.. note::
   * 证书更新是使用Xinference企业版的必要步骤
   * 建议在部署完成后立即进行证书更新
   * 如遇到问题，请及时联系技术支持
