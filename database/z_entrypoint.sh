#!/bin/bash

if [ ! -v LOCAL ]; then
    /bin/update-db.sh woz &
	echo STARTED UPDATE SCRIPT
fi
