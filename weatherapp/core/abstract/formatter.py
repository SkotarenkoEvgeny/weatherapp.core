import abc


class Formatter(abc.ABC):

    """ Base abstract class for formatters.
    """


    @abc.abstractmethod
    def emit(self, data):
        """ Format and print data from the iterable source.
        :param column_names: names of the columns
        :type data: list or tuple
        :param stdout: output stream where data should be written
        :type stdout: sys.stdout or file like object
        """

