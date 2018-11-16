#!/bin/env python3
'''msg_class.py
Classes for messages
'''
__version__='0.1'

################################################################################
# AUTHORS         : Jan Kohout
# CREATION DATE   : 2018-11-15
#
# DESCRIPTION :
#   Classes for messages
#
# MODIFICATION HISTORY:
#   2018-11-15  Jan Kohout      0.1      Initial version
#
################################################################################

from time import mktime
from datetime import datetime

#   ------------------------    msgEvent      ---------------------    #
class msgEvent (object):
    '''Class for keeping the longest match. '''

    def __init__ (self, version, data_date, data_time, performance=0):
        '''Initialization '''

        self.version = version
        self.date_time = data_date + ' ' + data_time
        self.timestamp = 0
        self.performance = performance

        self.method = ''
        self.url = ''
        self.data_format = ''

    def set_APIs (self, method, url, data_format):
        '''Here the real values for each API is defined. '''
        
        try:
            self.timestamp = int (mktime (datetime.strptime (self.date_time, '%Y-%m-%d %H:%M:%S').timetuple()))
        except ValueError: return False
        except: raise

        if method in ('PUT', 'POST'): 
            self.method = method 
        else: return False

        self.url = url
        self.data_format = data_format.format (**self.__dict__)

        return True

    def __str__ (self):
        return str ( (self.version, self.date_time, self.timestamp, self.performance, self.method, self.url, self.data_format) )

