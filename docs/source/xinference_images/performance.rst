.. _performance_testing:

================
性能测试
================

本文档介绍如何使用Xinference的性能测试工具。

.. contents:: 目录
   :local:
   :depth: 2

测试工具概述
============

使用 https://github.com/xorbitsai/inference/tree/main/benchmark 提供的测试集。

测试工具包括：

* ``benchmark_serving``：测试整体服务指标。
* ``benchmark_latency``：测试延迟指标。
* ``benchmark_long``：测试长上下文的推理效果。

测试数据集
==========

对于 serving 和 latency 的测试，需要使用数据集。默认使用的数据集在 https://hf-mirror.com/datasets/anon8231489123/ShareGPT_Vicuna_unfiltered/tree/main ，下载 ``ShareGPT_V3_unfiltered_cleaned_split.json``

运行测试集
==========

基本命令
--------

.. code-block:: bash

   python benchmark_serving.py --dataset /path/to/ShareGPT_V3_unfiltered_cleaned_split.json \
                               --tokenizer /path/to/tokenizer \
                               --model-uid ${model_uid} \
                               --num-prompt 100 --concurrency 50

参数说明
--------

* ``--dataset`` 为刚刚下载的数据集路径。
* ``--tokenizer`` 指定为模型的下载路径。
* ``--model-uid`` 指定为模型的 ID，在运行的模型列表里可以找到。
* ``--num-prompt`` 为测试的 prompt 个数，默认 100。
* ``--concurrency`` 同时并发的请求，默认100。

结果说明
========

测试结果示例
------------

.. code-block:: text

   ================ Benchmark Result ================
   Successful requests:                     100       
   Benchmark duration (s):                  44.55     
   Total input tokens:                      16604     
   Total generated tokens:                  18181     
   Request throughput (req/s):              2.24      
   Input token throughput (tok/s):          372.70    
   Output token throughput (tok/s):         408.10    
   ----------------Latency Statistics----------------
   Mean latency (s):                        22.7351   
   Mean latency per token (s):              0.0909    
   Mean latency per output token (s):       0.3358    
   ==================================================

指标含义
--------

* ``Successful requests``：成功的请求数。
* ``Benchmark duration (s)``：Benchmark 时长。
* ``Total input tokens``：总输入 token 数。
* ``Total generated tokens``：总生成 token 数。
* ``Request throughput (req/s)``：请求吞吐（每秒处理的请求）。
* ``Input token throughput (tok/s)``：输入 token 吞吐（每秒处理的输入 token）。
* ``Output token throughput (tok/s)``：输出的 token 吞吐（每秒生成的 token）。
* ``Mean latency (s)``：平均延迟。
* ``Mean latency per token (s)``：平均每 token 延迟。
* ``Mean latency per output token (s)``：平均每输出 token 延迟。

相关文档
========

* :doc:`nvidia` - Nvidia系列镜像使用
* :doc:`mindie` - MindIE系列镜像使用
* :doc:`hygon` - 海光系列镜像使用
