==================================================
Ascend 310P: Qwen3 precision and eager execution
==================================================

.. container:: docs-metadata

   :Hardware: Ascend 310P
   :Backend: vLLM-Ascend
   :Model: Qwen3

.. container:: docs-pending

   Xinference, driver and backend versions were not supplied in the original case. This workaround belongs to the recorded hardware and model combination.

Symptom
=========

Deployment or inference can fail with default parameters on this combination.

Recorded workaround
=====================

Explicitly configure half precision and eager execution in the engine parameters.

.. code-block:: text
   :caption: Engine parameters

   dtype=float16
   enforce_eager=true

Verification
==============

Confirm the effective engine parameters in model logs, then send a fixed prompt and check that inference completes with coherent output. The record does not isolate which parameter is decisive, so preserve both when reproducing this configuration.

Related guides
================

* :doc:`ascend_310p_qwen35`
* :doc:`../xinference_images/mindie`
