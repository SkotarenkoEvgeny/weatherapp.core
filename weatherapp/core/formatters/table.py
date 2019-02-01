import prettytable
import csv

from weatherapp.core.abstract import Formatter


class TableFormatter(Formatter):
    """
    Table formatter for app output.
    """

    def __init__(self):
        self.pt = prettytable.PrettyTable()
        self.pt.field_names = ["site_name", "temperature", "place", "cond"]

    def emit(self, data):
        """
        Format and print data from the iterable source.
        :param column_names: names of the columns
        :type column_names: list
        :param data: iterable data source, one tuple per object
        with values in order of column names
        :type data: list or tuple
        """
        for i in data:
            self.pt.add_row(i)

        self.pt.align = 'l'
        self.padding_width = 1
        # pt.hrules = 2
        # pt.vrules = 0
        return self.pt.get_string()

class CSV_Formatter(Formatter):
    """
    CSV formatter for app output.
    """
    def emit(self, data):

        with open("output.csv", "w", newline='', encoding='utf-8') as csv_file:
            for unit in data:
                writer = csv.writer(csv_file, delimiter=',')
                writer.writerow(unit)
        return 'csv file is written'
