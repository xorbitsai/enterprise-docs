===============================================
NVIDIA: GPU at 100% with long response delays
===============================================

.. container:: docs-metadata

   :Hardware: NVIDIA GPU
   :Model: Qwen3-32B
   :Log context: Xinference 1.0.3

Symptom
=========

Qwen3-32B on one GPU keeps its memory allocated and utilization near 100%, while Qwen2.5-VL on another GPU responds normally. Even a short probe waits; one recorded greeting returned about 40 minutes later as GPU utilization fell.

.. container:: docs-evidence

   :Observed: Another model on the same machine remained responsive. High GPU utilization shows active computation but does not distinguish many requests from one long-running request.
   :Hypothesis: Long prompts, large token budgets, thinking output or a queue may occupy this model instance. The root cause was not confirmed in the record.

Logs and request correlation
==============================

In the recorded Xinference 1.0.3 context, chat entry and exit messages use DEBUG logging. Model subprocess logs may differ from the worker's main log; absent chat messages in that file do not prove the request never reached the model.

Mitigation and diagnostics
============================

The notes recommend streaming, a bounded token budget, a unique request identifier and disabling thinking where the engine supports it. The following is the recorded client request configuration; keep client-specific fields in the format expected by your SDK.

.. code-block:: json

   {
     "stream": true,
     "max_tokens": 512,
     "request_id": "unique-business-request-id",
     "extra_body": {
       "enable_thinking": false
     }
   }

Use a small ``request_limits`` value, such as 1 or 2, when reproducing the case. Add concurrency, timeout and queue limits at the entry layer so short requests do not wait indefinitely behind long ones.

Verification
==============

Compare the same prompt on an idle instance and under load. Correlate request identifiers with model logs and record first-token latency, total latency and whether output completes. Treat these measures as diagnostic evidence, not confirmation of the proposed cause.

* :doc:`../xinference_images/performance`
* :doc:`../xinference_images/langfuse`
