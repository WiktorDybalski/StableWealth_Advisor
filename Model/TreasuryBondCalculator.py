import pandas as pd
import matplotlib.pyplot as plt

NOMINAL_VALUE_OF_OBLIGATION = 100
BELKA_TAX = 0.19

class TreasuryBondCalculator:
    def __init__(self):
        self.period = None
        self.curr_inflation = None
        self.number_of_bonds = None
        self.bond_type = None
        self.NBP = None
        self.last_row_list = []
        self.start_value = 0
        self.bonds = {
            "ROD": (7.25, 2.0, "Year", 2, 144, True, None),
            "EDO": (7, 1.5, "Year", 2, 120, True, None),
            "ROS": (6.95, 1.75, "Year", 0.7, 72, True, None),
            "TOS": (6.6, None, "Year", 0.7, 36, True, None),
            "COI": (6.75, 1.25, "Year", 0.7, 48, False, None),
            "OTS": (3/12, None, "Month", 0, 3, False, None),  # 3% roczne oprcentowanie ale na miesiac to 0,25
            "ROR": (6.25/12, None, "Month", 0.5, 12, False, 0),  # bierzemy % NBP i dzielimy przez 12; 0 bo dodajemy 0 do NBP
            "DOR": (6.5 / 12, None, "Month", 0.7, 24, False, 0.5),  # bierzemy % NBP i dzielimy przez 12
        }

    def main(self, params):
        self.bond_type = params[0]
        self.number_of_bonds = params[1]
        self.curr_inflation = params[2]
        self.period = params[3]
        self.NBP = params[4]
        start_value = params[1] * 100
        self.start_value = start_value
        last_value = start_value
        bond_stats = self.bonds.get(self.bond_type)
        df = pd.DataFrame()
        remaining_period = self.period
        first_cycle = 1
        if remaining_period < bond_stats[4] // 12:
            print("It is stupid request")
            return
        while remaining_period >= bond_stats[4]:
            current_period = min(remaining_period, bond_stats[4])
            self.period = current_period
            new_df = self.calculate_bond(last_value)
            if first_cycle:
                df = pd.concat([df, new_df], ignore_index=True)
                first_cycle = 0
            else:
                df = pd.concat([df, new_df[1:]], ignore_index=True)
            self.last_row_list = df.iloc[-1].values.tolist()
            total_profit = df.iloc[-1, 6]
            last_value = last_value + total_profit
            remaining_period -= current_period

        # For the remaining period (if less than bond period)
        if remaining_period > 0:
            self.period = remaining_period
            final_df = self.calculate_bond(last_value)
            if bond_stats[2] == "Month":
                df = pd.concat([df, final_df.iloc[1:remaining_period + 1]], ignore_index=True)
            else:
                df = pd.concat([df, final_df.iloc[1:remaining_period // 12 + 1]], ignore_index=True)

        df.index.name = bond_stats[2]
        df.to_csv("calc_results.csv")
        print(df)

        # Plot the data
        plt.figure(figsize=(10, 6))

        # Mozna [1:] usunac by bylo od roku 0
        # Plot Net Profit
        plt.plot(df.index[1:], df['Net Profit'][1:], marker='o', color='green', label='Net Profit')

        # Plot Total Profit
        plt.plot(df.index[1:], df['Total Profit'][1:], marker='o', color='red', label='Total Profit')

        # Plot the profit limit
        plt.axhline(y=0, color='orange', linestyle='--', label='Profit limit')

        # Adjust x-axis limits to start from Year 1
        plt.xlim(left=0)

        # Adding titles and labels
        plt.title('Net Profit and Total Profit over Years')
        plt.xlabel('After "x" years')
        if self.bond_type in ["OTS", "ROR", "DOR"]:
            plt.title('Net Profit and Total Profit over Months')
            plt.xlabel('After "x" months')
        plt.ylabel('Profit in PLN')
        plt.legend()

        # Show the plot
        plt.grid(True)
        plt.show()

    def calculate_bond(self, start_value):
        print("calculating bond")
        redemption_fee_per_bond = self.bonds[self.bond_type][3]
        n = self.number_of_bonds

        percetnage_initial = self.bonds[self.bond_type][0]
        percetnage_later = self.bonds[self.bond_type][1]
        cycle_duration = self.bonds[self.bond_type][2]
        if cycle_duration == "Year":
            cycles = self.bonds[self.bond_type][4] // 12
        else:
            cycles = self.bonds[self.bond_type][4]
        nbp = self.bonds[self.bond_type][6]

        redemption_fee = [redemption_fee_per_bond * n for _ in range(cycles - 1)] + [0] + [0]

        capitalaised = self.bonds[self.bond_type][5]

        affected_by_inflation = True
        if percetnage_later is None:
            percetnage_later = percetnage_initial
            affected_by_inflation = False

        year_inflation = (self.curr_inflation / 100)
        if cycle_duration == "Month":
            year_inflation = (self.curr_inflation / 100) / 12
        interest_rates = [percetnage_initial/100] + [(percetnage_later/100+year_inflation) for _ in range(cycles-1)]
        if not affected_by_inflation:
            interest_rates = [percetnage_initial/100] + [percetnage_later/100 for _ in range(cycles-1)]
        if nbp is not None:
            interest_rates = [percetnage_initial / 100] + [(((nbp+self.NBP)/12) / 100) for _ in range(cycles - 1)]

        if self.last_row_list:
            print(self.last_row_list[8])
            last_accumulated_inflation = self.last_row_list[8] / 100
        else:
            last_accumulated_inflation = 0
        last_accumulated_interests = 0
        last_value = start_value

        titles = ['Value', 'Interest Rate', 'Interests', 'Accumulated Interests', 'Redemption Fee',
                  'Belka Tax', 'Net Profit', 'Year Inflation', 'Accumulated Inflation', 'Total Profit',
                  'Total Profit %']
        data = pd.DataFrame(columns=titles)

        first_row = [start_value] + [0 for _ in range(10)]
        data.loc[len(data)] = first_row

        for i in range(cycles):
            value = self.calculate_value(last_value, interest_rates[i])
            interest_rate = interest_rates[i]
            interests = last_value * interest_rate
            accumulated_interests = last_accumulated_interests + interests
            belka_tax = BELKA_TAX * (accumulated_interests - redemption_fee[i])
            net_profit = self.calculate_net_profit(accumulated_interests, redemption_fee[i])
            if not capitalaised and nbp is not None:
                value = start_value
                belka_tax = BELKA_TAX * interests
                net_profit = accumulated_interests - redemption_fee[i] - belka_tax
            elif not capitalaised:
                value = start_value
                belka_tax = BELKA_TAX * accumulated_interests
            accumulated_inflation = (1 - last_accumulated_inflation) * year_inflation + last_accumulated_inflation
            total_profit = (start_value + net_profit) * (1 - accumulated_inflation) - self.start_value
            total_profit_percent = total_profit / self.start_value

            row = [round(value, 2), round(interest_rate, 2), round(interests, 2),
                   round(accumulated_interests, 2),
                   round(redemption_fee[i], 2), round(belka_tax, 2), round(net_profit, 2),
                   round(year_inflation * 100, 2), round(accumulated_inflation * 100, 2),
                   round(total_profit, 2), round(total_profit_percent * 100, 2)]

            data.loc[len(data)] = row

            last_value = value
            last_accumulated_interests = accumulated_interests
            if nbp is not None:
                last_accumulated_interests = accumulated_interests - belka_tax
            last_accumulated_inflation = accumulated_inflation

        return data


    def calculate_value(self, value, interest):
        return value * (interest + 1)

    def calculate_net_profit(self, accumulated_interests, redemption_fee):
        return accumulated_interests - redemption_fee - BELKA_TAX * (accumulated_interests - redemption_fee)

if __name__ == "__main__":
    calc = TreasuryBondCalculator()

    # calc.main(["TOS", 1000, 12.4, 36, None])
    calc.main(["ROR", 1000, 12.4, 24, 5.25])