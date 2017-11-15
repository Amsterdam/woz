#!/bin/bash

if [ ! -v LOCAL ]; then
    /bin/update-db.sh woz root &
	echo STARTED UPDATE SCRIPT
fi
