#!/usr/bin/env bash

set -e


while :
do
    if [[ ! -f "/proc/$(cat $PIDFILE)/status" ]]
    then
        echo "Starting Jenkins instance: ${NAME} "
        java -jar bin/jenkins.war \
            --enable-future-java \
            --logfile="$LOGFILE" \
            --httpPort="$PORT" &
        echo $! > "$PIDFILE"
    else
        :
    fi
    sleep 10
done
