#!/bin/bash

readonly DIR=$(cd $(dirname $0) && pwd)
readonly TG_DIR="tg"

main() {
	local chat=$1
	local limit="5000"
	local step="100"
	local i

	mkfifo tg_pipe
	cd "$TG_DIR"
	./telegram -W < $DIR/tg_pipe > $DIR/output &
	cd "$DIR"
	echo "chat_info $chat" > tg_pipe;
	sleep 2;
	echo > $DIR/output;

	for i in $(seq $limit -$step 0); do
		echo -n ".";
		cmd="history $chat $step $i";
		# echo $cmd;
		echo $cmd > tg_pipe;
		sleep 3;
	done

	echo "quit" > tg_pipe
	rm tg_pipe
}

main $1