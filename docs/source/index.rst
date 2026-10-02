.. _index:

==========================================
Deploy and operate Xinference Enterprise
==========================================

.. container:: docs-home

   Guides for installing on your hardware, running models across nodes and diagnosing issues, with cases from recorded deployments.

Common tasks
==============

.. container:: docs-task-list

   * :doc:`getting_started/installation`

     Choose a deployment option and prepare the runtime environment.

   * :doc:`hardware/index`

     Set up NVIDIA, Ascend, Hygon or MetaX accelerators.

   * :doc:`xinference_images/license`

     Activate and manage an Enterprise license.

   * :doc:`xinference_images/multi_deployment`

     Connect supervisors and workers across hosts.

   * :doc:`cluster/high_availability`

     Deploy primary and secondary supervisors and verify failover.

   * :doc:`troubleshooting/index`

     Start from a symptom and compare recorded cases.

.. grid:: 1 1 2 2
   :gutter: 4
   :class-container: docs-home-columns

   .. grid-item::

      .. rubric:: New guides

      * :doc:`hardware/metax`
      * :doc:`deployment/pd_disaggregation`
      * :doc:`cluster/high_availability`

   .. grid-item::

      .. rubric:: Recorded troubleshooting cases

      * :doc:`troubleshooting/ascend_310p_qwen3`
      * :doc:`troubleshooting/ascend_310p_qwen35`
      * :doc:`troubleshooting/ascend_910b_operators`
      * :doc:`troubleshooting/nvidia_slow_response`
      * :doc:`troubleshooting/gb10_multinode`

All guides
============

.. container:: docs-guide-index

   Getting started
      :doc:`getting_started/installation` · :doc:`getting_started/environments` · :doc:`xinference_images/license`

   Hardware & installation
      :doc:`xinference_images/nvidia` · :doc:`xinference_images/mindie` · :doc:`xinference_images/hygon` · :doc:`hardware/metax`

   Models & performance
      :doc:`deployment/pd_disaggregation` · :doc:`xinference_images/performance`

   Clusters & availability
      :doc:`xinference_images/multi_deployment` · :doc:`cluster/high_availability` · :doc:`xinference_images/kubernetes`

   Observability
      :doc:`xinference_images/langfuse`

   Troubleshooting
      :doc:`xinference_images/troubleshooting` · :doc:`troubleshooting/index`

.. toctree::
   :maxdepth: 2
   :hidden:

   getting_started/index
   hardware/index
   deployment/index
   cluster/index
   observability/index
   troubleshooting/index
