# coding: utf-8
#!/usr/bin/env python
import logging.config
import os

logging.config.fileConfig(os.path.join(os.path.dirname(__file__), "../../conf/log.conf"), disable_existing_loggers=False)
logger = logging.getLogger(__name__)
