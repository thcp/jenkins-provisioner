#!/usr/bin/env bash

set -e

start_jenkins() {
    echo "Starting Jenkins instance: ${NAME} on port ${PORT}"
    java -jar "$JENKINS_WAR_FILE" \
        --enable-future-java \
        --logfile="$LOGFILE" \
        --httpPort="$PORT" &
    echo $! > "$PIDFILE"
}

start_jenkins

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
