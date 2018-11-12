#!/usr/bin/env bash

set -e

start_jenkins() {
    echo "Starting Jenkins instance: ${NAME} on port ${PORT}"
    java -jar bin/jenkins.war \
        --enable-future-java \
        --logfile="$LOGFILE" \
        --httpPort="$PORT" &
    echo $! > "$PIDFILE"
}

while :
do
    if [[ ! -f "/proc/$(cat $PIDFILE)/status" ]]
    then
        start_jenkins
    else
        :
    fi
    sleep "${DELAY}"
done
