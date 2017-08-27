import logging
import logging.config

#init log in main
logging.config.fileConfig('log.conf', disable_existing_loggers=False)

logger = logging.getLogger(__name__)

logger.debug('test main logger')
logger.info('start import module \'mod\'...')

