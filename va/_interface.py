import abc


class IValidator(abc.ABC):
    """Abstract base class for validators.
    """

    @abc.abstractmethod
    def __init__(self):
        """
        Args:
            request - Request object
            **kwargs - all kwargs of Django Forms.
        """
        pass

    @abc.abstractmethod
    def is_valid(self) -> bool:
        """Validate and clean data.

        1. Set `cleaned_data` and return True if data is valid
        2. Set `errors` and return False otherwise.

        Returns:
            True: data is valid
            False: data is invalid
        """
        pass

    @property
    @abc.abstractmethod
    def errors(self):
        """Errors dict. Set by `is_valid` method.

        key: name of invalid field or `__all__`.
        value: list of errors strings.
        """
        pass

    @property
    @abc.abstractmethod
    def cleaned_data(self):
        """Cleaned data dict (or other type). Set by `is_valid` method.
        """
        pass
