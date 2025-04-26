import logging
import os

log_dir = os.path.join(os.path.dirname(__file__), '../log')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'client.log')

logger = logging.getLogger('client')
logger.setLevel(logging.INFO)

formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')

# 控制台
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# 文件
file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def info(msg):
    logger.info(msg)

def warning(msg):
    logger.warning(msg)

def error(msg):
    logger.error(msg) 