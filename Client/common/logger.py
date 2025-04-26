import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

class Logger:
    def __init__(self):
        self.log_dir = os.path.join(os.path.dirname(__file__), '../log')
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_file = os.path.join(self.log_dir, f'client_{datetime.now().strftime("%Y%m%d")}.log')
        self.logger = logging.getLogger('client')
        self.logger.setLevel(logging.INFO)
        self.formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
        self.setup_handlers()
        self.setup_custom_levels()

    def setup_handlers(self):
        # 控制台
        self.console_handler = logging.StreamHandler()
        self.console_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.console_handler)

        # 文件
        self.file_handler = RotatingFileHandler(self.log_file, maxBytes=1024*1024, backupCount=5, encoding='utf-8')
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)

    def setup_custom_levels(self):
        # 添加自定义日志级别
        self.PRINT_ONLY = 25
        self.NO_PRINT = 35
        logging.addLevelName(self.PRINT_ONLY, 'PRINT_ONLY')
        logging.addLevelName(self.NO_PRINT, 'NO_PRINT')

        # 设置处理逻辑
        def handle_print_only(record):
            if record.levelno == self.PRINT_ONLY:
                print(record.msg)
                return False
            return True

        def handle_no_print(record):
            if record.levelno == self.NO_PRINT:
                return False
            return True

        # 添加过滤器
        self.console_handler.addFilter(handle_print_only)
        self.file_handler.addFilter(handle_no_print)

    def print_only(self, msg):
        self.logger.log(self.PRINT_ONLY, msg)

    def no_print(self, msg):
        self.logger.log(self.NO_PRINT, msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

# 创建全局实例
logger = Logger()

# 导出模块级别的函数
info = logger.info
error = logger.error
print_only = logger.print_only
no_print = logger.no_print 