# ilugc-archivetics
This project aims to have a live query searchable interface for the ILUGC email archives.

Prototype is to have a Python beautifulsoap cron which would monitor the archives and push the updates to queue.

A service reads the updates on the queue and indexes them on Elastic Search cluster.

Queries and analytics are possible there after by running a Kibana instance connecting with ES cluster.
