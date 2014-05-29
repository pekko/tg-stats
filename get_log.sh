#!/bin/bash

DIR=$(cd $(dirname $0) && pwd)
TG_DIR="tg"
LIMIT="1000"

mkfifo tg_pipe
cd "$TG_DIR"
./telegram -W < $DIR/tg_pipe > $DIR/output &
cd "$DIR"
echo "history NappiGram $LIMIT" > tg_pipe
sleep 2
echo "quit" > tg_pipe
rm tg_pipe
