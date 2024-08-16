# logger.py
import logging
import logging.handlers
# PAPERTRAIL_HOST ='logs2.papertrailapp.com'
# PAPERTRAIL_PORT = 17807

# handler = logging.handlers.SysLogHandler(address=(PAPERTRAIL_HOST, PAPERTRAIL_PORT))
# formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    # handlers=[handler]
    
# Terminallog
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="basic.log" 

)

def get_logger(name):
    logger = logging.getLogger(name)
    return logger

logging.debug("this is a debug message")
logging.info("this is a info message")
logging.warning("this is a warning message")
logging.error("this is a error message")
logging.critical("this is a critical message")
