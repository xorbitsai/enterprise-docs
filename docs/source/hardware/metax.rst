======================
MetaX GPU deployment
======================

Run the Enterprise image on a host with MetaX drivers and device files available.

.. container:: docs-metadata

   :Hardware: MetaX GPU
   :Runtime: Docker
   :Devices: ``/dev/dri``, ``/dev/mem``, ``/dev/mxcd``

.. container:: docs-pending

   The original deployment record does not specify driver, image or backend versions. Confirm a compatible combination for your environment before using this configuration.

Prerequisites
===============

Install the MetaX driver and Docker on the host. Check that all three device paths listed above exist and choose the appropriate Enterprise image.

Start the container
=====================

Replace the image placeholder with your MetaX Enterprise image. The shared-memory allocation below is the value from the deployment record; size it for the host and workload.

.. code-block:: bash
   :caption: Container startup

   docker run -it -d \
     --name xinf-mx \
     --network host \
     --device=/dev/dri \
     --device=/dev/mem \
     --device=/dev/mxcd \
     --group-add video \
     --shm-size=128g \
     --security-opt seccomp=unconfined \
     --security-opt apparmor=unconfined \
     --ulimit memlock=-1 \
     --restart unless-stopped \
     <metax-enterprise-image>

.. list-table:: Container parameters
   :header-rows: 1
   :widths: 40 60

   * - Parameter
     - Purpose
   * - ``--network host``
     - Use host ports directly without port mapping.
   * - ``--device``
     - Expose the DRI, physical-memory and MetaX compute devices.
   * - ``--group-add video``
     - Grant access through the video group.
   * - ``--shm-size=128g``
     - Configure the container's shared-memory limit.
   * - ``--security-opt``
     - Use the seccomp and AppArmor settings from the recorded configuration.
   * - ``--ulimit memlock=-1``
     - Remove the locked-memory limit.
   * - ``--restart unless-stopped``
     - Restart after an unexpected stop, except when manually stopped.

Persistent model storage
==========================

Add these options to the container command to keep downloaded models on the host. Replace the host path with an existing directory.

.. code-block:: bash

   -v /path/to/models/.xinference:/root/.xinference \
   -e XINFERENCE_HOME=/root/.xinference

Start and verify the service
==============================

Enter the container, replace the host placeholder with the machine's reachable address, and start the web entry and inference service.

.. code-block:: bash

   ./xinf-enterprise.sh --host <host-ip> --port 9997 --listen-port 8091 && \
     XINFERENCE_MODEL_SRC=modelscope xinference-local --host <host-ip> --port 9997

Check the container logs, access the web interface on port 8091 and launch a model. Validate actual inference output as well as API availability.

Related guides
================

* :doc:`../getting_started/environments`
* :doc:`../xinference_images/troubleshooting`
