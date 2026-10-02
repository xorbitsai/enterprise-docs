===========================================
GB10: multi-node communication dependency
===========================================

.. container:: docs-metadata

   :Hardware: Two NVIDIA GB10 hosts
   :Architecture: aarch64
   :Xinference: 1.0.4

Symptom and evidence
======================

A single-node deployment chats normally, but one replica spread across two workers waits without output and eventually encounters an engine error. GPU activity fluctuates during the distributed request. The deployment logs in the supplied record pointed to an outdated CuPy version.

Recorded dependency change
============================

The case used these versions. Apply them consistently to the affected worker environments and check their compatibility with the rest of the image rather than adopting them as requirements for other releases.

.. code-block:: bash

   python -m pip install "cupy-cuda12x==13.6.0" "numpy==1.26.4"
   python -m pip show cupy-cuda12x numpy
   python -m pip check

.. note::

   The original installation upgraded NumPy to 2.2.6 when CuPy was installed separately. The recorded environment needed NumPy 1.26.4, so the command pins both dependencies together.

Verification
==============

Restart the affected model processes after updating the environment. Confirm the versions on both workers, launch the distributed replica and verify coherent chat output. Retain the image tag and engine logs with the case.

* :doc:`../xinference_images/multi_deployment`
