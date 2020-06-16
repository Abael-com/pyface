# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from random import choice, randint

from traits.api import HasStrictTraits, Instance, Int, Str, List

from pyface.api import ApplicationWindow, GUI
from pyface.data_view.abstract_value_type import AbstractValueType, none_value
from pyface.data_view.data_models.column_data_model import (
    AbstractRowInfo, ColumnDataModel, HasTraitsRowInfo
)
from pyface.data_view.i_data_view_widget import IDataViewWidget
from pyface.data_view.data_view_widget import DataViewWidget
from pyface.data_view.value_types.api import IntValue, TextValue


class Address(HasStrictTraits):

    street = Str

    city = Str

    country = Str


class Person(HasStrictTraits):

    name = Str

    age = Int

    address = Instance(Address)


row_info = HasTraitsRowInfo(
    title='People',
    value='name',
    value_type=TextValue(),
    rows=[
        HasTraitsRowInfo(
            title="Age",
            value="age",
            value_type=IntValue(minimum=0),
        ),
        HasTraitsRowInfo(
            title="Address",
            value_type=none_value,
            value='address',
            rows=[
                HasTraitsRowInfo(
                    title="Street",
                    value="address.street",
                    value_type=TextValue(),
                ),
                HasTraitsRowInfo(
                    title="City",
                    value="address.city",
                    value_type=TextValue(),
                ),
                HasTraitsRowInfo(
                    title="Country",
                    value="address.country",
                    value_type=TextValue(),
                ),
            ],
        ),
    ],
)


class MainWindow(ApplicationWindow):
    """ The main application window. """

    data = List(Instance(Person))

    row_info = Instance(AbstractRowInfo)

    data_view = Instance(IDataViewWidget)

    def _create_contents(self, parent):
        """ Creates the left hand side or top depending on the style. """

        self.data_view = DataViewWidget(
            parent=parent,
            data_model=ColumnDataModel(
                data=self.data,
                row_info=self.row_info,
            ),
            #header_visible=False,
        )
        self.data_view._create()
        return self.data_view.control

    def _data_default(self):
        import numpy
        return numpy.random.uniform(size=(100000, 10))

male_names = [
    'Michael',
    'Edward',
    'Timothy',
    'James',
    'George',
    'Ralph',
    'David',
    'Martin',
    'Bryce',
    'Richard',
    'Eric',
    'Travis',
    'Robert',
    'Bryan',
    'Alan',
    'Harold',
    'John',
    'Stephen',
    'Gael',
    'Frederic',
    'Eli',
    'Scott',
    'Samuel',
    'Alexander',
    'Tobias',
    'Sven',
    'Peter',
    'Albert',
    'Thomas',
    'Horatio',
    'Julius',
    'Henry',
    'Walter',
    'Woodrow',
    'Dylan',
    'Elmer']

female_names = [
    'Leah',
    'Jaya',
    'Katrina',
    'Vibha',
    'Diane',
    'Lisa',
    'Jean',
    'Alice',
    'Rebecca',
    'Delia',
    'Christine',
    'Marie',
    'Dorothy',
    'Ellen',
    'Victoria',
    'Elizabeth',
    'Margaret',
    'Joyce',
    'Sally',
    'Ethel',
    'Esther',
    'Suzanne',
    'Monica',
    'Hortense',
    'Samantha',
    'Tabitha',
    'Judith',
    'Ariel',
    'Helen',
    'Mary',
    'Jane',
    'Janet',
    'Jennifer',
    'Rita',
    'Rena',
    'Rianna']

all_names = male_names + female_names

male_name = lambda: choice(male_names)
female_name = lambda: choice(female_names)
any_name = lambda: choice(all_names)
age = lambda: randint(15, 72)

family_name = lambda: choice(['Jones',
                              'Smith',
                              'Thompson',
                              'Hayes',
                              'Thomas',
                              'Boyle',
                              "O'Reilly",
                              'Lebowski',
                              'Lennon',
                              'Starr',
                              'McCartney',
                              'Harrison',
                              'Harrelson',
                              'Steinbeck',
                              'Rand',
                              'Hemingway',
                              'Zhivago',
                              'Clemens',
                              'Heinlien',
                              'Farmer',
                              'Niven',
                              'Van Vogt',
                              'Sturbridge',
                              'Washington',
                              'Adams',
                              'Bush',
                              'Kennedy',
                              'Ford',
                              'Lincoln',
                              'Jackson',
                              'Johnson',
                              'Eisenhower',
                              'Truman',
                              'Roosevelt',
                              'Wilson',
                              'Coolidge',
                              'Mack',
                              'Moon',
                              'Monroe',
                              'Springsteen',
                              'Rigby',
                              "O'Neil",
                              'Philips',
                              'Clinton',
                              'Clapton',
                              'Santana',
                              'Midler',
                              'Flack',
                              'Conner',
                              'Bond',
                              'Seinfeld',
                              'Costanza',
                              'Kramer',
                              'Falk',
                              'Moore',
                              'Cramdon',
                              'Baird',
                              'Baer',
                              'Spears',
                              'Simmons',
                              'Roberts',
                              'Michaels',
                              'Stuart',
                              'Montague',
                              'Miller'])

street = lambda: '%d %s %s' % (randint(11,
                                        999),
                                choice(['Spring',
                                        'Summer',
                                        'Moonlight',
                                        'Winding',
                                        'Windy',
                                        'Whispering',
                                        'Falling',
                                        'Roaring',
                                        'Hummingbird',
                                        'Mockingbird',
                                        'Bluebird',
                                        'Robin',
                                        'Babbling',
                                        'Cedar',
                                        'Pine',
                                        'Ash',
                                        'Maple',
                                        'Oak',
                                        'Birch',
                                        'Cherry',
                                        'Blossom',
                                        'Rosewood',
                                        'Apple',
                                        'Peach',
                                        'Blackberry',
                                        'Strawberry',
                                        'Starlight',
                                        'Wilderness',
                                        'Dappled',
                                        'Beaver',
                                        'Acorn',
                                        'Pecan',
                                        'Pheasant',
                                        'Owl']),
                                choice(['Way',
                                        'Lane',
                                        'Boulevard',
                                        'Street',
                                        'Drive',
                                        'Circle',
                                        'Avenue',
                                        'Trail']))

city = lambda: choice(['Boston', 'Cambridge', ])
country = lambda: choice(['USA', 'UK'])

people = [
    Person(
        name='%s %s' % (any_name(), family_name()),
        age=age(),
        address=Address(
            street=street(),
            city=city(),
            country=country(),
        ),
    )
    for i in range(100)
]


# Application entry point.
if __name__ == "__main__":
    # Create the GUI (this does NOT start the GUI event loop).
    gui = GUI()

    # Create and open the main window.
    window = MainWindow(data=people, row_info=row_info)
    window.open()

    # Start the GUI event loop!
    gui.start_event_loop()
