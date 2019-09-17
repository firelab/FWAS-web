import abc


class Fetcher(object, metaclass=abc.ABCMeta):
    """
    Interface for any of the fetcher classes. Implements
    a simple state machine:
        - (1) download: retrieves the desired data
        - (2) transform: processes the downloaded data
        - (3) save: stores the results into the database
    """

    @abc.abstractmethod
    def download(self):
        """Download the data file to local disk."""

    @abc.abstractmethod
    def transform(self):
        """Transform the downloaded file to a suitable representation."""

    @abc.abstractmethod
    def save(self):
        """Save the results to the database."""

    @abc.abstractmethod
    def cleanup(self):
        """Cleanup any temporary files, state, etc. Will always be called"""

    def run(self):
        try:
            self.download()
            self.transform()
            self.save()
        finally:
            self.cleanup()
