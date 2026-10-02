=====================================
Ascend 310P: Qwen3.5 context length
=====================================

.. container:: docs-metadata

   :Hardware: Ascend 310P
   :Backend: vLLM-Ascend
   :Model: Qwen3.5

Symptom and recorded configuration
====================================

The deployment notes require an explicit context-length setting in addition to the Qwen3 precision and eager parameters. The exact failure log and backend version were not recorded.

.. code-block:: text
   :caption: Recorded engine parameters

   dtype=float16
   enforce_eager=true
   max-model-len=16384

.. container:: docs-evidence

   :Observed: The supplied notes record this parameter combination for Qwen3.5 on 310P.
   :Hypothesis: The attention operator may require a large uncompressed mask. This explanation is unconfirmed; it is not evidence of a universal model or hardware limit.

Verification and reference
============================

Check the effective context limit after startup and verify inference within that limit. Record the exact backend and image versions when reproducing the case.

The original notes reference `vLLM-Ascend issue 7394 <https://github.com/vllm-project/vllm-ascend/issues/7394>`_.

* :doc:`ascend_310p_qwen3`
