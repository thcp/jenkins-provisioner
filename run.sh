#!/bin/bash

set -e

INSTANCES_HOME="$(pwd)/instances"
RDATA="$(pwd)/rdata"

download_war() {
    JENKINS_BIN="${RDATA}/jenkins.war"
    MASTER_HOME="${INSTANCES_HOME}/${1}"
    mkdir -p "$RDATA" "$MASTER_HOME"
    
    if [ ! -f "$JENKINS_BIN" ]
    then
        URL='http://mirrors.jenkins.io/war-stable/latest/jenkins.war'
        wget -P "$RDATA" "$URL"
    fi
}


connect_test() {
    DEFAULT_PORT="8080"
    
    while true
    do
        if [ cat < /dev/tcp/localhost/"$DEFAULT_PORT" ]; then
            DEFAULT_PORT=$((DEFAULT_PORT+1))
            echo "Port ${DEFAULT_PORT} in use, trying next one"
        else
            echo "Port ${DEFAULT_PORT} available, assigning for this server.."
            NEW_PORT=$DEFAULT_PORT
            break
        fi
    done
}

launch_instance() {
    export JENKINS_HOME="${INSTANCES_HOME}/${1}"
    LOG_DIR="${JENKINS_HOME}/logs"
    mkdir -p "$LOG_DIR"    
    connect_test
    watcher
}

watcher() {
    while :
    do
        if [ ! -f "/proc/$(cat /tmp/agent.pid)/status" ]
        then
            echo "Starting Jenkins instance: ${MASTER} "
            java -jar $JENKINS_BIN \
            --logfile="$LOG_DIR/daily.log" \
            --httpPort="$NEW_PORT" &
            echo $! > /tmp/agent.pid
            # placeholder for notification
        else
            :
        fi
        sleep 10
    done   
}

deploy_master() {
    MASTER="$1"
    
    if [ ! -d "$INSTANCE_PATH" ]
    then
        echo "Deploying  New jenkins master Server: ${MASTER}"
        download_war "$MASTER"
        launch_instance "$MASTER"
    else
        echo "Instance already exists, aborting."
        exit 1
    fi
}

case "$1" in
    deploy)
        deploy_master "$2"
        ;;
    remove)
        remove_master "$2"
        ;;
    status)
        check_status "$2"
        ;;
    *)
        echo "Option not supported, currently available options are:"
        echo "deploy <instance_name>"
        echo "remove <instance name>"
        echo "status <instance name>"
esac
