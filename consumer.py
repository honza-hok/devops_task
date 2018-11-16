#!/bin/env python3
''' consumer.py
Reads FIFO data, keeps messages and sends to REST APIs
'''
__version__='0.1'

################################################################################
# AUTHORS         : Jan Kohout
# CREATION DATE   : 2018-11-15
#
# DESCRIPTION :
#   Reads FIFO data, keeps messages and sends to REST APIs
#
# MODIFICATION HISTORY:
#   2018-11-15  Jan Kohout      0.1      Initial version
#
################################################################################
 
from os import mkfifo, remove
import errno
from time import sleep
import configparser
import requests

from msg_class import msgEvent

import random

#    ----------------------------    init_queue    ----------------------    #
def init_files (file_name):
    '''Initialize the FIFO implemented as OS FIFO. Returns stored message list. '''

    mkfifo (file_name)
    print ('FIFO created ...')

    config = configparser.RawConfigParser()
    config.read ('api_defs.ini')

    return [config [section] for section in config.sections ()]
 
#    ----------------------------    process_data  ----------------------    #
def process_data (data, config_APIs, msg_list):
    '''Reads fifo data and creates new messages. Updates message list. '''

    # For each input line and each configurated API create message object, fill with API and add to list (if API values success)
    for data_line in data:
        for cfg_API in config_APIs:
            version, data_date, data_time = data_line.rstrip().split (' ')
            msg = msgEvent (version, data_date, data_time)
            if msg.set_APIs (cfg_API ['method'], cfg_API ['url'], cfg_API ['data_format']):
                msg_list += [ msg ]

#    ----------------------------    process_msgs  ----------------------    #
def process_msgs (msg_list):
    '''Reads fifo data and creates new messages. Updates message list. '''

    failed_list = []

    print ('Message queue length:', len (msg_list) )
    for message in msg_list:
        try:
            if message.method == 'POST':
                resp = requests.post (message.url, json=message.data_format)
            elif message.method == 'PUT':
                resp = requests.put (message.url, json=message.data_format)
            if resp.status_code != requests.codes.ok:
                failed_list += [message]

        except Exception as oe:
            print ('Failed:', message)
            print (oe)
            ## Just for testing w-out target
            if random.randrange (2):    # 2 => 0,1
                failed_list += [message]
            
            ## Main version:
            # failed_list += [message]

        del message    
    
    return failed_list

#    ----------------------------    main        ------------------------    #
def main (input_pipe):
    '''Main method for consumer. Initialize, read and process data. '''

    msg_list = []
    config_APIs = init_files (input_pipe)

    print ('Opening FIFO ...')
    while True:             # FIFO must be closed after each try not to re-read same data
        with open (input_pipe) as fifo:
            data = fifo.readlines ()
            if data:
                process_data (data, config_APIs, msg_list)
            msg_list = process_msgs (msg_list)     # Old messages may exist in list queue
        sleep (5)

#    ----------------------------    main        ------------------------    #
if __name__=='__main__':

    input_pipe = '/tmp/ci_pipe'
    # File exists => consumer already running => exit
    try:
        main (input_pipe)
    except OSError as oe: 
        if oe.errno == errno.EEXIST:
            print ('Consumer already running!')
            raise SystemExit
    except:
        remove (input_pipe)
        raise

    remove (input_pipe)
