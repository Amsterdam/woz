Datapunt WOZ API
================

Structure for the jenkins scripts:
.jenkins/test   : scripts for ci testing
.jenkins/import : scripts for ci importing
.jenkins        : common scripts, used by test and import (e.g. docker-wait.sh)

This structure prevents that web/ contains CI related scripts.


NOTE:
-----

For backwards compatability reasons:
 * the directory .jenkins-import is created:
this directory is currently actually  being called by CI. In future CI should point to the .jenkins/import/import.sh.
 * web/docker-migrate.sh
 this is being called by CI. In future CI should point to .jenkins/docker-migrate.sh


NOTE 2:
-------

The import requires to have data imported from BAG, this is doen in the `prepare_db.sh` script which is packaged in the
database docker. Import docker then waits for the data to be present before proceeding.