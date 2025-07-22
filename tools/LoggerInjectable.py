from abc import ABC, abstractmethod
from loguru import logger as loguru_logger

__all__ = ["LoggerInjectable", "loguru_logger"]

class LoggerInjectable(ABC):
    """
    Abstract base class for logger injection.

    Provides a logger instance to subclasses, following the Dependency Inversion Principle.
    """

    def __init__(self, logger=None):
        """
        Initialize the logger, using dependency injection if provided.

        Args:
            logger: Optional custom logger instance.
        """
        self.logger = logger or self._create_logger()

    @classmethod
    def _create_logger(cls):
        """
        Create and configure a logger instance for the subclass.

        Returns:
            loguru_logger: Configured logger instance.
        """
        logger = loguru_logger.bind(classname=cls.__name__)
        logger.add(
            f"logs/{cls.__name__}.log",
            rotation="1 day",
            retention="7 days",
            level="INFO",
            filter=lambda record: record["extra"].get("classname") == cls.__name__
        )
        logger.info(f"{cls.__name__} logger initialized.")
        return logger

    @abstractmethod
    def perform_action(self):
        """
        Abstract method to be implemented by subclasses, using the injected logger.
        """
        pass

class DataProcessor(LoggerInjectable):
    """
    Example subclass that processes data and logs the action.
    """
    def perform_action(self):
        self.logger.info("Processing data in DataProcessor.")

class NotificationSender(LoggerInjectable):
    """
    Example subclass that sends notifications and logs the action.
    """
    def perform_action(self):
        self.logger.info("Sending notification in NotificationSender.")

def __init__():
    """
    LoggerInjectable module initializer.
    """
    pass
