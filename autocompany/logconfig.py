import logging

class ColorFormatter(logging.Formatter):
    """A logging formatter to add colors to the log levels."""
    FORMAT = "{levelname} {asctime} {module} {message}"
    FORMATS = {
        logging.DEBUG: "\033[0;36m" + FORMAT + "\033[0m",  # Cyan for DEBUG
        logging.INFO: "\033[0;32m" + FORMAT + "\033[0m",  # Green for INFO
        logging.WARNING: "\033[0;33m" + FORMAT + "\033[0m",  # Yellow for WARNING
        logging.ERROR: "\033[0;31m" + FORMAT + "\033[0m",  # Red for ERROR
        logging.CRITICAL: "\033[1;41m" + FORMAT + "\033[0m",  # Red background for CRITICAL
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, style='{')
        return formatter.format(record)
