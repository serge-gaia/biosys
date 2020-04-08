import logging

from django.utils import six
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.writer.write_only import WriteOnlyCell

from main.utils_data_package import GenericSchema

COLUMN_HEADER_FONT = Font(bold=True)

logger = logging.getLogger(__name__)


class DefaultExporter:
    """
    dataset: Dataset
    records: [Record]
    mapping_funcs: defines a dictionary of functions that will be applied to the value of the field
                   key=field.name value=func(record, field, value)
                   Example, round latitude and longitude to 6 decimals
                   {
                     'latitude': lambda record, field, value: round(value, 6),
                     'longitude': lambda record, field, value: round(value, 6),
                   }
    """

    def __init__(self, dataset, records=None, mapping_funcs=None):
        self.ds = dataset
        self.schema = GenericSchema(dataset.schema_data)
        self.headers = self.schema.headers
        self.warnings = []
        self.errors = []
        self.records = records if records else []
        self.mapping_funcs = mapping_funcs or {}
        if not isinstance(self.mapping_funcs, dict):
            raise ValueError("mapping_funcs must be a dictionary.")

    def row_it(self, cast=True):
        for record in self.records:
            row = []
            for field in self.schema.fields:
                value = record.data.get(field.name, '')
                mapping_func = self.mapping_funcs.get(field.name)
                # noinspection PyBroadException
                try:
                    if callable(mapping_func):
                        value = mapping_func(record, field, value)
                    else:
                        if cast:
                            # Cast to native python type
                            value = field.cast(value)
                except Exception:
                    pass
                # TODO: remove that when running in Python3
                if isinstance(value, six.string_types) and not isinstance(value, six.text_type):
                    value = six.u(value)
                row.append(value)
            yield row

    def csv_it(self):
        yield self.headers
        for row in self.row_it(cast=False):
            yield row

    def _to_worksheet(self, ws):
        ws.title = self.ds.name
        # write headers
        headers = []
        for header in self.headers:
            cell = WriteOnlyCell(ws, value=header)
            cell.font = COLUMN_HEADER_FONT
            headers.append(cell)
        ws.append(headers)
        for row in self.row_it():
            ws.append(row)
        return ws

    def to_workbook(self):
        wb = Workbook(write_only=True)
        ws = wb.create_sheet()
        self._to_worksheet(ws)
        return wb

    def to_csv(self, output):
        # TODO: remove when python3
        if six.PY2:
            import unicodecsv as csv
        else:
            import csv

        output = output or six.StringIO()
        writer = csv.writer(output, dialect='excel')
        for row in self.csv_it():
            writer.writerow(row)


class BionetExporter(DefaultExporter):
    """
    Same as default but spit two blank lines at the top when using csv
    07/04/2020: OEH Bionet also wants the record id in the External Key field (if any)
    https://youtrack.gaiaresources.com.au/youtrack/issue/BIOSYS-412
    """
    mapping_funcs = {
        'External Key': lambda record, _field, _value: record.id
    }

    def __init__(self, dataset, records=None):
        super().__init__(dataset, records, mapping_funcs=self.mapping_funcs)

    def to_csv(self, output):
        # TODO: remove when python3
        if six.PY2:
            import unicodecsv as csv
        else:
            import csv

        output = output or six.StringIO()
        writer = csv.writer(output, dialect='excel')
        writer.writerow(['Bionet Ignored Line'])
        writer.writerow(['Bionet Ignored Line'])
        for row in self.csv_it():
            writer.writerow(row)
