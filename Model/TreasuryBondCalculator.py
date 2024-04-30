NOMINAL_VALUE_OF_OBLIGATION = 100
OTS = "OTS"
ROR = "ROR"
DOR = "DOR"
TOS = "TOS"
COI = "COI"
EDO = "EDO"
ROS = "ROS"
ROD = "ROD"

class TreasuryBondCalculator:
    def __init__(self, params):
        self.bond_type = params[0]
        self.number_of_bonds = params[1]
        self.curr_inflation = params[2]
        self.FUNCTION_MAP = {
            OTS: self.calculate(),
            ROR: self.calculate(),
            DOR: self.calculate(),
            TOS: self.calculate(),
            COI: self.calculate(),
            EDO: self.calculate(),
            ROS: self.calculate(),
            ROD: self.calculate()
        }

    def calculate(self):
        pass