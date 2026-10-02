==============================
High availability deployment
==============================

Deploy primary and secondary supervisors, workers, a shared database and a unified Nginx entry. This guide assumes containers with Xinference and the Enterprise HA script already installed.

.. container:: docs-metadata

   :Control plane: Primary and secondary supervisors
   :Database: Shared MySQL or PostgreSQL
   :Entry: Nginx / OpenResty

.. note::

   All addresses below are example private-network addresses from the supplied guide. Replace them with reachable addresses in your deployment. The original guide does not specify an image version; confirm that your image provides the HA options and script shown here.

Topology and ports
====================

.. code-block:: text
   :caption: Control-plane topology

   Client -> Nginx -> Primary / Secondary Supervisor -> Workers
                         |          |
                         +----------+ -> Shared database

.. list-table:: Example node and port allocation
   :header-rows: 1
   :widths: 30 30 40

   * - Component
     - Example address
     - Ports
   * - Nginx entry
     - ``10.1.0.10``
     - 8008 (external entry)
   * - Primary supervisor
     - ``10.1.0.11``
     - 9991 (API), 9911 (actor), 9551 (binlog), 9651 (checkpoint)
   * - Secondary supervisor
     - ``10.1.0.12``
     - 9992 (API), 9912 (actor), 9552 (binlog), 9652 (checkpoint)
   * - Worker
     - ``10.1.0.13``
     - 9921 (actor)
   * - Shared database
     - ``10.1.0.20``
     - 3306 (MySQL) or 5432 (PostgreSQL)

Allow both supervisors to reach the database and each other's actor, binlog and checkpoint ports. Nginx must reach both supervisor APIs. Workers must reach the primary API, and both supervisors must reach worker actor ports. Do not use loopback addresses for communication between hosts.

Prepare the database and nodes
================================

Both supervisors must use the same shared database, not separate local SQLite databases. The database stores API, permission, task and instance records; binlog and checkpoint synchronize supervisor runtime metadata. These mechanisms have different responsibilities.

Configure one database URL on both supervisors. Using the same configuration on workers keeps the environment consistent. The image must include the corresponding database driver.

.. tab-set::

   .. tab-item:: MySQL

      .. code-block:: bash

         export XINFERENCE_SQLALCHEMY_DATABASE_URL="mysql+pymysql://xinference:<password>@10.1.0.20:3306/xinference"

   .. tab-item:: PostgreSQL

      .. code-block:: bash

         export XINFERENCE_SQLALCHEMY_DATABASE_URL="postgresql+psycopg2://xinference:<password>@10.1.0.20:5432/xinference"

Confirm the supervisor and worker commands exist, inspect the supervisor's supported options, and choose the working directory used by the image.

.. code-block:: bash

   which xinference-supervisor
   which xinference-worker
   xinference-supervisor --help
   cd /opt/projects

Before starting processes, check the ports allocated to that node. For the secondary use ports 9992, 9912, 9552 and 9652; for the worker use port 9921.

.. code-block:: python
   :caption: Primary-node port check

   import socket

   for port in [9991, 9911, 9551, 9651]:
       sock = socket.socket()
       try:
           sock.bind(("0.0.0.0", port))
       except OSError:
           print(f"{port}: in use")
       else:
           print(f"{port}: available")
       finally:
           sock.close()

Start the cluster
===================

Run each command on its designated node, after exporting the shared database URL. Logs are written to the working directory.

.. tab-set::

   .. tab-item:: Primary

      .. code-block:: bash

         nohup xinference-supervisor \
           --log-level DEBUG \
           --host 10.1.0.11 \
           --port 9991 \
           --supervisor-port 9911 \
           --remote-supervisor 10.1.0.12:9912 \
           --local-binlog-port 9551 \
           --local-checkpoint-port 9651 \
           --data-path . \
           > ./primary-supervisor.log 2>&1 &

   .. tab-item:: Secondary

      .. code-block:: bash

         nohup xinference-supervisor \
           --log-level DEBUG \
           --host 10.1.0.12 \
           --port 9992 \
           --supervisor-port 9912 \
           --secondary \
           --remote-supervisor 10.1.0.11:9911 \
           --local-binlog-port 9552 \
           --local-checkpoint-port 9652 \
           --data-path . \
           > ./secondary-supervisor.log 2>&1 &

   .. tab-item:: Worker

      .. code-block:: bash

         XINFERENCE_HA=1 nohup xinference-worker \
           --log-level DEBUG \
           --endpoint http://10.1.0.11:9991 \
           --host 10.1.0.13 \
           --worker-port 9921 \
           > ./worker.log 2>&1 &

Configure the unified entry
=============================

Run the HA script on the Nginx node. It renders the OpenResty configuration and starts or reloads Nginx. The supplied script supports two supervisor backends; additional backends need a separate load-balancer configuration.

.. code-block:: bash

   /opt/projects/xinf-enterprise-ha.sh \
     --primary-host 10.1.0.11 \
     --primary-port 9991 \
     --secondary-host 10.1.0.12 \
     --secondary-port 9992 \
     --listen-port 8008

The entry checks both supervisors' status endpoints and routes requests to the available primary. Use the unified entry for model deployment and client requests.

.. code-block:: text

   Health checks:
   http://10.1.0.11:9991/v1/get_supervisor_status
   http://10.1.0.12:9992/v1/get_supervisor_status

   Client entry:
   http://10.1.0.10:8008

Acceptance checks
===================

Check both supervisors directly and then check the unified entry.

.. code-block:: bash

   curl http://10.1.0.11:9991/v1/cluster/version
   curl http://10.1.0.11:9991/status
   curl http://10.1.0.12:9992/v1/cluster/version
   curl http://10.1.0.12:9992/status
   curl http://10.1.0.10:8008/v1/cluster/version
   curl http://10.1.0.10:8008/v1/supervisor_transfer_status
   curl http://10.1.0.10:8008/status

Expect version information from the primary, ``it is a secondary supervisor`` from the secondary version endpoint, and the worker in both status responses. Initially the unified entry reports ``has_transfered=false`` and ``active_node=primary``.

Deploy a model through the unified entry and test actual inference. Inspect both supervisor logs for synchronized replica routing metadata before testing failover.

.. code-block:: bash

   grep -nE "ModelActor|loaded|META_REPLICA_MAP_INFO" ./primary-supervisor.log
   grep -nE "META_REPLICA_MAP_INFO|replay" ./secondary-supervisor.log

Successful secondary replay of ``META_REPLICA_MAP_INFO`` indicates that replica-to-worker routes were synchronized.

Optional failover drill and recovery
======================================

.. dropdown:: Test a primary failure in a test environment

   This drill intentionally stops the primary supervisor. Run it separately from routine installation and only in the environment chosen for failure testing.

   On the example primary node:

   .. code-block:: bash

      pkill -TERM -f "xinference-supervisor.*--port 9991"
      sleep 3
      pkill -KILL -f "xinference-supervisor.*--port 9991" || true

   Poll the secondary version endpoint. Once it returns version information instead of the secondary-role message, inspect promotion and worker-reconnection logs.

   .. code-block:: bash

      curl http://10.1.0.12:9992/v1/cluster/version
      grep -nE "set primary successfully|transfer to the Primary" ./secondary-supervisor.log
      grep -nE "change_supervisor_ref|supervisor=10.1.0.12:9912" ./worker.log

   .. code-block:: text
      :caption: Expected log indicators

      set primary successfully
      the Secondary Supervisor transfer to the Primary Supervisor success
      change_supervisor_ref: _supervisor_address: 10.1.0.12:9912

   Check the unified entry again. The recorded configuration checks approximately every two seconds and switches after five failures; this is a configuration-specific timing, not a guaranteed recovery time.

   .. code-block:: bash

      curl http://10.1.0.10:8008/v1/cluster/version
      curl http://10.1.0.10:8008/v1/supervisor_transfer_status
      curl http://10.1.0.10:8008/status

   Expect ``has_transfered=true`` and ``active_node=backup``, with the old primary down and the backup up. Send a real chat request to the already deployed model through the same entry.

   If inference cannot find the model, inspect the new primary's routing logs and the earlier replica-map replay. A successful role change alone does not establish that the model is still reachable.

   .. code-block:: bash

      grep -nE "describe_model|get_model|Model not found|qwen" ./secondary-supervisor.log

After recovering the former primary, rejoin it as a secondary with the current primary's addresses and the same shared database. Avoid automatically reclaiming the primary role. Verify metadata synchronization, node status and inference again.

Related guides
================

* :doc:`../xinference_images/multi_deployment`
* :doc:`../xinference_images/troubleshooting`
