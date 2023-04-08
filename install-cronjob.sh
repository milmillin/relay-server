#!/bin/bash
export -p > .env

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
USER_=$(whoami)

echo "#!/bin/bash" > start_relay_server.sh
echo "source $SCRIPTPATH/.env" >> start_relay_server.sh
echo "python $SCRIPTPATH/relay_server.py -p $1 >> /tmp/relay-server-$USER_.log" >> $SCRIPTPATH/start_relay_server.sh
chmod +x $SCRIPTPATH/start_relay_server.sh

(crontab -l 2>/dev/null; echo "* * * * * /usr/bin/flock -n /tmp/miluai-relay-server-$USER_.lockfile $SCRIPTPATH/start_relay_server.sh") | crontab -
