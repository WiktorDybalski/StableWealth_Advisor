import pandas as pd

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
            OTS: self.calculate_OTS,
            ROR: self.calculate_ROR,
            DOR: self.calculate_DOR,
            TOS: self.calculate_TOS,
            COI: self.calculate_COI,
            EDO: self.calculate_EDO,
            ROS: self.calculate_ROS,
            ROD: self.calculate_ROD
        }

    def main(self, bond_type):
        calculate_func = self.FUNCTION_MAP.get(bond_type)
        if calculate_func:
            return calculate_func()
        else:
            print("Unsupported bond type.")
            return None

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
        redemption_fee_per_bond = 2
        n = self.number_of_bonds
        redemption_fee = [0] + [redemption_fee_per_bond * n for _ in range(9)] + [0]
        year_inflation = self.curr_inflation / 100
        bond_value = 100
        start_value = n * bond_value
        interest_rates = [0.07] + [(year_inflation + 0.015) for _ in range(9)]
        last_accumulated_inflation = 0
        last_accumulated_interests = 0
        last_value = start_value

        titles = ['Value', 'Interest Rate', 'Interests', 'Accumulated Interests', 'Redemption Fee',
                  'Belka Tax', 'Net Profit', 'Year Inflation', 'Accumulated Inflation', 'Total Profit',
                  'Total Profit %']
        data = pd.DataFrame(columns=titles)

        first_row = [start_value] + [0 for _ in range(10)]
        data.loc[len(data)] = first_row

        for i in range(10):
            value = self.calculate_value(last_value, interest_rates[i])
            interest_rate = interest_rates[i]
            interests = last_value * interest_rate
            accumulated_interests = last_accumulated_interests + interests
            beam_belka_tax = BELKA_TAX * (accumulated_interests - redemption_fee[i + 1])
            net_profit = self.calculate_net_profit(accumulated_interests, redemption_fee[i + 1])
            accumulated_inflation = (1 - last_accumulated_inflation) * year_inflation + last_accumulated_inflation
            total_profit = (start_value + net_profit) * (1 - accumulated_inflation) - start_value
            total_profit_percent = total_profit / start_value

            row = [round(value, 2), round(interest_rate, 2), round(interests, 2),
                   round(accumulated_interests, 2),
                   round(redemption_fee[i + 1], 2), round(beam_belka_tax, 2), round(net_profit, 2),
                   round(year_inflation * 100, 2), round(accumulated_inflation * 100, 2),
                   round(total_profit, 2), round(total_profit_percent * 100, 2)]

            data.loc[len(data)] = row

            last_value = value
            last_accumulated_interests = accumulated_interests
            last_accumulated_inflation = accumulated_inflation

        data.index.name = "Year"
        data.to_csv("calc_results.csv")

        return data

    def calculate_ROS(self):
        pass

    def calculate_ROD(self):
        pass

    def calculate_value(self, value, interest):
        return value * (interest + 1)

    def calculate_net_profit(self, accumulated_interests, redemption_fee):
        return accumulated_interests - redemption_fee - BELKA_TAX * (accumulated_interests - redemption_fee)


if __name__ == "__main__":
    calc = TreasuryBondCalculator(["EDO", 1000, 3])
    print(calc.main("EDO"))
