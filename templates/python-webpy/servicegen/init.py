# Initialization code for servicegen services.
import os, sys
from ConfigParser import SafeConfigParser
import logging, logging.handlers

def getConfig(app):
    """
    Returns a ConfigParser object for the given application.
    """
    cfg = SafeConfigParser()
    filename = app + '.cfg'
    cfg.read([
        '/etc/servicegen/common.cfg', os.path.expanduser('~/.servicegen/common.cfg'),
        filename,
        '/etc/servicegen/' + filename, os.path.expanduser('~/.servicegen/' + filename)])
    
    if len(sys.argv) == 1 and cfg.has_option('server', 'port'):
        sys.argv.append(cfg.get('server', 'port'))
    
    return cfg

def getLogger(cfg, name):
    """
    Returns a logger for the given name. Use servicegen.<servicename>
    as the name.
    """
    rootLogger = logging.getLogger('')
    if len(rootLogger.handlers) == 0:
        handler = logging.handlers.RotatingFileHandler(cfg.get('logging', 'filename'),
            maxBytes=52428800, backupCount=5)   # 50 MB
        handler.setFormatter(logging.Formatter(cfg.get('logging', 'format')))
        level = getattr(logging, cfg.get('logging', 'level'))
        rootLogger.setLevel(level)
        rootLogger.addHandler(handler)
    return logging.getLogger(name)
