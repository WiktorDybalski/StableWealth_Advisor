# Singleton Class (has only one instance per class)
class CalculatorConfigurator:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CalculatorConfigurator, cls).__new__(cls)
        return cls._instance

    def __init__(self, period=None, curr_inflation=None, number_of_bonds=None, bond_type=None, NBP=None):
        if not hasattr(self, '_initialized'):
            self._period = period
            self._curr_inflation = curr_inflation
            self._number_of_bonds = number_of_bonds
            self._bond_type = bond_type
            self._NBP = NBP
            self._initialized = True

    @property
    def period(self):
        return self._period

    @period.setter
    def period(self, value):
        self._period = value

    @property
    def curr_inflation(self):
        return self._curr_inflation

    @curr_inflation.setter
    def curr_inflation(self, value):
        self._curr_inflation = value

    @property
    def number_of_bonds(self):
        return self._number_of_bonds

    @number_of_bonds.setter
    def number_of_bonds(self, value):
        self._number_of_bonds = value

    @property
    def bond_type(self):
        return self._bond_type

    @bond_type.setter
    def bond_type(self, value):
        self._bond_type = value

    @property
    def NBP(self):
        return self._NBP

    @NBP.setter
    def NBP(self, value):
        self._NBP = value
