#!/bin/bash

################################################################################
# AUTHORS         : Jan Kohout
# CREATION DATE   : 2018-11-15
#
# DESCRIPTION :
#   Save parameters into FIFO
#
# MODIFICATION HISTORY:
#   2018-11-15  Jan Kohout      0.1      Initial version
################################################################################

# Help
if [[ $1 == "-h" || $1 == "--help" ]]; then
	echo "producer.extension.sh <build_name> YYYY-MM-DD HH:MM:SS"
	exit 1
fi

# Pipe
pipe=/tmp/ci_pipe

# Errors tests
[[ ! -p $pipe ]] && { echo "Reader not running"; exit 2; }
[[ $# -eq 3 ]] || { echo "Number of parameters is not correct"; exit 3; }
[[ $2 =~ ^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1]) ]] || { echo "Date format is not correct"; exit 4; }
[[ $3 =~ ^([0-1][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9]) ]] || { echo "Time format is not correct"; exit 4; }

# Command :-)
echo "$*" > $pipe
