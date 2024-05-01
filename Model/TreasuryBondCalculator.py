import pandas

NOMINAL_VALUE_OF_OBLIGATION = 100
BELKA_TAX = 0.19

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
            OTS: self.calculate_OTS(),
            ROR: self.calculate_ROR(),
            DOR: self.calculate_DOR(),
            TOS: self.calculate_TOS(),
            COI: self.calculate_COI(),
            EDO: self.calculate_EDO(),
            ROS: self.calculate_ROS(),
            ROD: self.calculate_ROD()
        }

    def main(self, bond_type):
        result_df = self.FUNCTION_MAP.get(bond_type)

    def calculate_OTS(self):
        pass

    def calculate_ROR(self):
        pass

    def calculate_DOR(self):
        pass

    def calculate_TOS(self):
        pass

    def calculate_COI(self):
        pass

    def calculate_EDO(self):
        titles = ["Year", "Amount to buy", "Interest rate", "Accumulated interest", "Redemption fee", "Belka tax",
                  "Net profit/loss", "Annual inflation", "Accumulated inflation", "Cumulative real profit/loss"]
        redemption_fee_per_bond = 2
        n = 10
        redemption_fee = n * redemption_fee_per_bond
        year_inflation = 0.03
        bond_value = 100
        start_value = n * bond_value
        inflation = 4
        interest_rates = [6.80] + [inflation for _ in range(10)]
        amount_to_buy = [0 for _ in range(10)]
        accumulated_interests = [0 for _ in range(10)]
        accumulated_inflation = []
        first_row = [0] + [start_value] + [0 for _ in range(11)]
        last_value = start_value


        df = pandas.DataFrame(columns=titles)

        for i in range(10):
            row = [i, self.calculate_amount_to_buy(last_value, interest_rates[i - 1]), interest_rates[i],
                   last_value * interest_rates[i - 1], accumulated_interests[i - 1] + last_value * interest_rates[i - 1],
                   redemption_fee, BELKA_TAX * accumulated_interests[i], self.calculate_net_profit(accumulated_interests[i], redemption_fee),
                   year_inflation, accumulated_inflation[i],
                   self.calculate_net_profit(accumulated_interests[i], redemption_fee) - start_value + (start_value * accumulated_inflation[i])]
            amount_to_buy[i] = row[1]

    def calculate_ROS(self):
        pass

    def calculate_ROD(self):
        pass

    def calculate_amount_to_buy(self, value, interest):
        return value * (interest + 1)

    def calculate_net_profit(self, accumulated_interest, redemption_fee):
        return accumulated_interest - redemption_fee - BELKA_TAX * accumulated_interest