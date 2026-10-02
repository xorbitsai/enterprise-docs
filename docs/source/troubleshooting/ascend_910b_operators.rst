==================================================
Ascend 910B: custom operator environment missing
==================================================

.. container:: docs-metadata

   :Hardware: Ascend 910B
   :Backend: vLLM-Ascend
   :Model: Qwen3.6-35B-A3B

Symptom
=========

Native vLLM starts and chats successfully, but the same model launched through Xinference fails with a recurrent-state dtype error.

.. code-block:: text

   torch_npu.npu_recurrent_gated_delta_rule
   Tensor params.state not implemented for DT_FLOAT, should be in dtype support list [DT_BFLOAT16]

Evidence and diagnosis
========================

.. container:: docs-evidence

   :Observed: The recorded Xinference-launched process did not inherit the custom operator paths that were present in the working native vLLM environment.
   :Diagnosis: The missing custom GDN/Mamba operator environment caused a fallback to the built-in CANN operator, which rejected the model's float32 state in this case.

Check both ``ASCEND_CUSTOM_OPP_PATH`` and the custom ``op_api/lib`` entry in ``LD_LIBRARY_PATH`` before changing model precision.

Load the operator environment
===============================

Source the vLLM-Ascend custom environment in the same shell that starts Xinference. Adjust the installation path for your image.

.. code-block:: bash

   source /vllm-workspace/vllm-ascend/vllm_ascend/_cann_ops_custom/vendors/vllm-ascend/bin/set_env.bash
   export VLLM_DISABLE_SHARED_EXPERTS_STREAM=1
   xinference-local --host 0.0.0.0 --port 8011 --log-level debug

Align model parameters with the working native launch. These are the values from the original test, not defaults for every deployment.

.. code-block:: text
   :caption: Parameters from the recorded deployment

   dtype=bfloat16
   tensor_parallel_size=2
   data_parallel_size=1
   enable_expert_parallel=True
   max_model_len=163840
   max_num_batched_tokens=16384
   max_num_seqs=128
   gpu_memory_utilization=0.94

Verification
==============

Launch through Xinference again, inspect the inherited operator environment and confirm that the dtype error is gone and chat output is coherent. Record CANN, torch-npu, vLLM and vLLM-Ascend versions alongside the image tag.

* :doc:`../getting_started/environments`
* :doc:`../xinference_images/mindie`
