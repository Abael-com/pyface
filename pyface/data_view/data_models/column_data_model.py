from abc import abstractmethod

from traits.api import (
    ABCHasStrictTraits, Callable, ComparisonMode, Event, HasTraits, Instance,
    List, Str, Tuple, observe
)
from traits.trait_base import xgetattr, xsetattr

from pyface.data_view.abstract_data_model import AbstractDataModel
from pyface.data_view.abstract_value_type import AbstractValueType
from pyface.data_view.index_manager import TupleIndexManager
from pyface.data_view.value_types.api import TextValue


def id(obj):
    return obj


class AbstractRowInfo(ABCHasStrictTraits):
    """ Configuration for a data row in a ColumnDataModel.
    """

    #: The text to display in the first column.
    title = Str()

    #: The child rows of this row, if any.
    rows = List(
        Instance('AbstractRowInfo'),
        comparison_mode=ComparisonMode.identity,
    )

    #: The value type of the data stored in this row.
    title_type = Instance(
        AbstractValueType,
        factory=TextValue,
        kw={'is_editable': False},
    )

    #: The value type of the data stored in this row.
    value_type = Instance(AbstractValueType)

    #: An event fired when the row or its children update.  The payload is
    #: a tuple of whether the title or value changed (or both), and the
    #: row_index affected.
    updated = Event

    def __iter__(self):
        yield self
        for row in self.rows:
            yield from row

    @abstractmethod
    def get_value(self, obj):
        raise NotImplementedError

    @abstractmethod
    def can_set_value(self, obj):
        raise NotImplementedError

    def set_value(self, obj):
        return False

    @abstractmethod
    def get_observable(self, obj):
        raise NotImplementedError

    # trait observers

    @observe('title,title_type.updated', dispatch='ui')
    def title_updated(self, event):
        self.updated = (self, 'title', [])

    @observe('value_type.updated', dispatch='ui')
    def value_type_updated(self, event):
        self.updated = (self, 'value', [])

    @observe('rows.items', dispatch='ui')
    def rows_updated(self, event):
        self.updated = (self, 'rows', [])

    @observe('rows:items:updated', dispatch='ui')
    def row_item_updated(self, event):
        row = event.object
        row_info, part, row_index = event.new
        row_index = [self.rows.index(row)] + row_index
        self.updated = (row_info, part, row_index)


class HasTraitsRowInfo(AbstractRowInfo):
    """ RowInfo that presents a named trait value.
    """

    #: The extended trait name of the trait holding the value.
    value = Str()

    def get_value(self, obj):
        return xgetattr(obj, self.value, None)

    def can_set_value(self, obj):
        return self.value != ''

    def set_value(self, obj, value):
        if not self.value:
            return False
        xsetattr(obj, self.value, value)
        return True

    def get_observable(self):
        return self.value

    @observe('value', dispatch='ui')
    def value_type_updated(self, event):
        self.updated = (self, 'value', [])


class DictRowInfo(AbstractRowInfo):
    """ RowInfo that presents an item in a dictionary.

    The attribute ``value`` should reference a dictionary trait on a
    has traits object.
    """

    #: The extended trait name of the dictionary holding the values.
    value = Str()

    #: The key holding the value.
    key = Str()

    def get_value(self, obj):
        data = xgetattr(obj, self.value, None)
        return data.get(self.key, None)

    def can_set_value(self, obj):
        return self.value != ''

    def set_value(self, obj, value):
        data = xgetattr(obj, self.value, None)
        data[self.key] = value
        return True

    def get_observable(self):
        return self.value + '.items'

    @observe('value,key', dispatch='ui')
    def value_type_updated(self, event):
        self.updated = (self, 'value', [])


class ColumnDataModel(AbstractDataModel):
    """ A data model that presents a list of objects as columns.
    """

    #: A list of objects to display in columns.
    data = List(
        Instance(HasTraits),
        comparison_mode=ComparisonMode.identity,
    )

    #: An object which describes how to map data for each row.
    row_info = Instance(AbstractRowInfo)

    #: The index manager that helps convert toolkit indices to data view
    #: indices.
    index_manager = Instance(TupleIndexManager, args=())

    def get_column_count(self, row):
        return len(self.data)

    def can_have_children(self, row):
        if len(row) == 0:
            return True
        row_info = self._row_info_object(row)
        return len(row_info.rows) != 0

    def get_row_count(self, row):
        row_info = self._row_info_object(row)
        return len(row_info.rows)

    def get_value(self, row, column):
        row_info = self._row_info_object(row)
        if len(column) == 0:
            return row_info.title
        obj = self.data[column[0]]
        return row_info.get_value(obj)

    def set_value(self, row, column, value):
        row_info = self._row_info_object(row)
        if len(column) == 0:
            return False
        obj = self.data[column[0]]
        return row_info.set_value(obj, value)

    def get_value_type(self, row, column):
        row_info = self._row_info_object(row)
        if len(column) == 0:
            return row_info.title_type
        else:
            return row_info.value_type

    def _row_info_object(self, row):
        row_info = self.row_info
        for index in row:
            row_info = row_info.rows[index]
        return row_info
