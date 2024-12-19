import inspect
import logging
from datetime import datetime
from django.conf import settings


class Logger:
    """This is a custom class extended the default logging functionality"""
    __project_logger = logging.getLogger("custom")
    __log_levels = dict(
        DEBUG='debug',
        INFO='info',
        WARNING='warning',
        WARN='warn',
        ERROR='error',
        CRITICAL='critical',
    )

    @staticmethod
    def __get_stack_details():
        """This method will return the stack details"""
        stack_info = inspect.stack()
        actual_stack = stack_info[3]
        return actual_stack.filename, actual_stack.function, actual_stack.lineno

    def __log_the_message(self, level, index, message):
        """Actual method which logs the given message with additional information
            i.e., filename, function, line number and datetime"""
        try:
            filename, func, lineno = self.__get_stack_details()
            filename = filename.replace(str(settings.BASE_DIR), ".")
            message = f"[{level:^8}] | {index:^8} | {filename} | {func} @ {lineno} : {message}"
            if settings.LOG_DATETIME:
                message = "[%s]" % datetime.now().strftime(settings.LOG_DATETIME_FORMAT) + " " + message
            self.__project_logger.__getattribute__(self.__log_levels.get(level))(message)
        except Exception as log_err:
            message = "Exception occurred! Failed to log the message, Exception: %s" % log_err
            self.__project_logger.error(message)

    def debug(self, index, message):
        self.__log_the_message("DEBUG", index=index, message=message)

    def info(self, index, message):
        self.__log_the_message("INFO", index=index, message=message)

    def warning(self, index, message):
        self.__log_the_message("WARNING", index=index, message=message)

    def warn(self, index, message):
        """This is """
        self.warning(index=index, message=message)

    def error(self, index, message):
        self.__log_the_message("ERROR", index=index, message=message)

    def critical(self, index, message):
        self.__log_the_message("CRITICAL", index=index, message=message)


logger = Logger()
