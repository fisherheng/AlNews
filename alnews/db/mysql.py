# coding: utf-8
#!/usr/bin/env python

from sqlalchemy import *
from sqlalchemy.orm import *

import logging.config

# Init log
logging.config.fileConfig('log.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

# Settings to connect to mysql database
database_setting = {'database_type': 'mysql',
                    'connector': 'mysqlconnector',
                    'user_name': 'root',
                    'password': 'zhang@heng0617M',
                    'host_name': 'localhost',
                    'database_name': 'platform',
                    'charset': 'charset=utf8'
                    }
