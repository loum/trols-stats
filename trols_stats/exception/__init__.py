__all__ = ['TrolsStatsConfigError']


class Error(Exception):
    def __init__(self, code=None, message=None):
        self.errno = code
        self.strerror = message

    def __str__(self):
        return '%d: %s' % (self.errno, self.strerror)


class TrolsStatsConfigError(Error):
    __error_msgs = {
        1000: {
            'message':
                'Config file not found',
            'help':
                'A configuration file was provided but could not be '
                'sourced on the server'
            },
        1001: {
            'message':
                'No config elements have been defined',
            'help':
                'A configuration file has not been parsed yet'
        }
    }

    def __init__(self, code=None):
        msg_code = TrolsStatsConfigError.__error_msgs.get(code)
        if msg_code is not None:
            msg = msg_code.get('message')
        super(TrolsStatsConfigError, self).__init__(code=code, message=msg)
