import pandas as pd
import matplotlib.pyplot as plt

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
    def __init__(self):
        self.period = None
        self.curr_inflation = None
        self.number_of_bonds = None
        self.bond_type = None
        self.NBP = None
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
        self.bonds = {
            "EDO": (7, 1.5, "Year", 2, 10, True, None),
            "ROS": (6.95, 1.75, "Year", 0.7, 6, True, None),
            "TOS": (6.6, None, "Year", 0.7, 3, True, None),
            "COI": (6.75, 1.25, "Year", 0.7, 4, False, None),
            "OTS": (3/12, None, "Month", 0, 3, False, None),  # 3% roczne oprcentowanie ale na miesiac to 0,25
            "ROR": (6.25/12, None, "Month", 0.5, 12, False, 0),  # bierzemy % NBP i dzielimy przez 12; 0 bo dodajemy 0 do NBP
            "DOR": (6.5 / 12, None, "Month", 0.7, 24, False, 0.5),  # bierzemy % NBP i dzielimy przez 12
        }

    def main(self, params):

        # param to np. ["EDO", 1000, 12.4, 150]

        # (Nazwa, oprocentowanie1, #2, redemtion fee per bond ,okres, ilosc cykli, Kapitalizacja, NBP)
        # [("EDO", 7, 2, "Year", 10), ("ROS", 6.95, 2.5, "Year", 12) ("ROS", 6.95, 2.5, "Year", 12, 5.25)]

        # (Nazwa, oprocentowanie1, #2, okres, ilosc cykli, Kapitalizacja, NBP)

        # bonds = {
        #     "EDO": (7, 1.5, "Year", 10, True, None),
        #     "ROS": (6.95, 1.75, "Year", 6, True, None),
        #     "TOS": (6.6, None, "Year", 3, True, None),
        #     "COI": (6.75, 1.25, "Year", 4, False, None),
        #     "OTS": (3/12, None, "Month", 3, False, None),  # 3% roczne oprcentowanie ale na miesiac to 0,25
        #     "ROR": (6.25/12, None, "Month", 12, False, 0),  # bierzemy % NBP i dzielimy przez 12; 0 bo dodajemy 0 do NBP
        #     "DOR": (6.5 / 12, None, "Month", 24, False, 0.5),  # bierzemy % NBP i dzielimy przez 12
        # }


        self.bond_type = params[0]
        self.number_of_bonds = params[1]
        self.curr_inflation = params[2]
        self.period = params[3]
        if len(params) == 5:
            self.NBP = params[4]
        start_value = params[1] * 100
        bond_period = 120

        df = pd.DataFrame()
        remaining_period = self.period

        while remaining_period > bond_period:
            current_period = min(remaining_period, bond_period)
            self.period = current_period
            #new_df = self.FUNCTION_MAP.get(self.bond_type)(start_value)
            new_df = self.calculate_bond(start_value)
            df = pd.concat([df, new_df], ignore_index=True)
            total_profit = df.iloc[-1, 6]
            start_value += total_profit
            remaining_period -= current_period

        # For the remaining period (if less than bond period)
        if remaining_period > 0:
            self.period = remaining_period
            #final_df = self.FUNCTION_MAP.get(self.bond_type)(start_value)
            final_df = self.calculate_bond(start_value)
            df = pd.concat([df, final_df.iloc[:remaining_period // 12 + 1]], ignore_index=True)

        df.index.name = "Year"

        if self.bond_type in ["OTS", "ROR", "DOR"]:
            df.index.name = "Month"
        df.to_csv("calc_results.csv")
        print(df)
        #print(type(df))

        # Sample data in a dictionary format


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


    # For refernce
    # bonds = {
            # "EDO": (7, 1.5, "Year", 2, 10, True, None),
            # "ROS": (6.95, 1.75, "Year", 0.7, 6, True, None),
            # "TOS": (6.6, None, "Year", 0.7, 3, True, None),
            # "COI": (6.75, 1.25, "Year", 0.7, 4, False, None),
            # "OTS": (3/12, None, "Month", 0, 3, False, None),  # 3% roczne oprcentowanie ale na miesiac to 0,25
            # "ROR": (6.25/12, None, "Month", 0.5, 12, False, 0),  # bierzemy % NBP i dzielimy przez 12; 0 bo dodajemy 0 do NBP
            # "DOR": (6.5 / 12, None, "Month", 0.7, 24, False, 0.5),  # bierzemy % NBP i dzielimy przez 12
    # }

    def calculate_bond(self, start_value):
        print("calculating bond")
        redemption_fee_per_bond = self.bonds[self.bond_type][3]
        n = self.number_of_bonds

        percetnage_initial = self.bonds[self.bond_type][0]
        percetnage_later = self.bonds[self.bond_type][1]
        cycle_duration = self.bonds[self.bond_type][2]
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
            interest_rates = [percetnage_initial / 100] + [((nbp+self.NBP/12) / 100) for _ in range(cycles - 1)]

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
            print(interest_rates[i])
            interests = last_value * interest_rate
            accumulated_interests = last_accumulated_interests + interests
            belka_tax = BELKA_TAX * (accumulated_interests - redemption_fee[i])

            net_profit = self.calculate_net_profit(accumulated_interests, redemption_fee[i])
            if not capitalaised:
                value = start_value
                belka_tax = BELKA_TAX * interests
                net_profit = accumulated_interests - redemption_fee[i] - belka_tax
            accumulated_inflation = (1 - last_accumulated_inflation) * year_inflation + last_accumulated_inflation
            total_profit = (start_value + net_profit) * (1 - accumulated_inflation) - start_value
            total_profit_percent = total_profit / start_value

            row = [round(value, 2), round(interest_rate, 2), round(interests, 2),
                   round(accumulated_interests, 2),
                   round(redemption_fee[i], 2), round(belka_tax, 2), round(net_profit, 2),
                   round(year_inflation * 100, 2), round(accumulated_inflation * 100, 2),
                   round(total_profit, 2), round(total_profit_percent * 100, 2)]

            data.loc[len(data)] = row

            last_value = value
            last_accumulated_interests = accumulated_interests
            last_accumulated_inflation = accumulated_inflation

        return data

    def calculate_OTS(self, start_value):
        print("calculating OTS")

        redemption_fee_per_bond = 0  # w tysiacach
        n = self.number_of_bonds
        redemption_fee = [redemption_fee_per_bond * n for _ in range(2)] + [0] + [0]
        year_inflation = (self.curr_inflation / 100) / 12
        interest_rates = [0.0025] + [0.0025 for _ in range(2)]
        last_accumulated_inflation = 0
        last_accumulated_interests = 0
        last_value = start_value

        titles = ['Value', 'Interest Rate', 'Interests', 'Accumulated Interests', 'Redemption Fee',
                  'Belka Tax', 'Net Profit', 'Cycle Inflation', 'Accumulated Inflation', 'Total Profit',
                  'Total Profit %']
        data = pd.DataFrame(columns=titles)

        first_row = [start_value] + [0 for _ in range(10)]
        data.loc[len(data)] = first_row

        for i in range(3):
            # value = self.calculate_value(last_value, interest_rates[i])
            value = start_value
            interest_rate = interest_rates[i]
            interests = last_value * interest_rate
            accumulated_interests = last_accumulated_interests + interests
            # belka_tax = BELKA_TAX * (accumulated_interests - redemption_fee[i])
            belka_tax = BELKA_TAX * interests
            net_profit = self.calculate_net_profit(accumulated_interests, redemption_fee[i])
            accumulated_inflation = (1 - last_accumulated_inflation) * year_inflation + last_accumulated_inflation
            total_profit = (start_value + net_profit) * (1 - accumulated_inflation) - start_value
            total_profit_percent = total_profit / start_value

            row = [round(value, 2), round(interest_rate, 2), round(interests, 2),
                   round(accumulated_interests, 2),
                   round(redemption_fee[i], 2), round(belka_tax, 2), round(net_profit, 2),
                   round(year_inflation * 100, 2), round(accumulated_inflation * 100, 2),
                   round(total_profit, 2), round(total_profit_percent * 100, 2)]

            data.loc[len(data)] = row

            last_value = value
            last_accumulated_interests = accumulated_interests
            last_accumulated_inflation = accumulated_inflation
        return data

    def calculate_ROR(self, start_value):
        print("calculating ROR")
        #print(self.NBP)
        redemption_fee_per_bond = 0.5  # w tysiacach
        n = self.number_of_bonds
        redemption_fee = [redemption_fee_per_bond * n for _ in range(11)] + [0] + [0]
        year_inflation = (self.curr_inflation / 100) / 12
        interest_rates = [0.00521] + [self.NBP/100 for _ in range(11)]
        last_accumulated_inflation = 0
        last_accumulated_interests = 0
        last_value = start_value

        titles = ['Value', 'Interest Rate', 'Interests', 'Accumulated Interests', 'Redemption Fee',
                  'Belka Tax', 'Net Profit', 'Cycle Inflation', 'Accumulated Inflation', 'Total Profit',
                  'Total Profit %']
        data = pd.DataFrame(columns=titles)

        first_row = [start_value] + [0 for _ in range(10)]
        data.loc[len(data)] = first_row

        for i in range(12):
            # value = self.calculate_value(last_value, interest_rates[i])
            value = start_value
            interest_rate = interest_rates[i]
            interests = last_value * interest_rate
            accumulated_interests = last_accumulated_interests + interests
            # belka_tax = BELKA_TAX * (accumulated_interests - redemption_fee[i])
            belka_tax = BELKA_TAX * interests
            # net_profit = self.calculate_net_profit(interests, redemption_fee[i])
            net_profit = accumulated_interests - redemption_fee[i] - belka_tax
            accumulated_inflation = (1 - last_accumulated_inflation) * year_inflation + last_accumulated_inflation
            total_profit = (start_value + net_profit) * (1 - accumulated_inflation) - start_value
            total_profit_percent = total_profit / start_value

            row = [round(value, 2), round(interest_rate, 2), round(interests, 2),
                   round(accumulated_interests, 2),
                   round(redemption_fee[i], 2), round(belka_tax, 2), round(net_profit, 2),
                   round(year_inflation * 100, 2), round(accumulated_inflation * 100, 2),
                   round(total_profit, 2), round(total_profit_percent * 100, 2)]

            data.loc[len(data)] = row

            last_value = value
            last_accumulated_interests = accumulated_interests
            last_accumulated_inflation = accumulated_inflation
        return data

    def calculate_DOR(self, start_value):
        print("calculating DOR")
        # print(self.NBP)
        redemption_fee_per_bond = 0.7  # w tysiacach
        n = self.number_of_bonds
        redemption_fee = [redemption_fee_per_bond * n for _ in range(23)] + [0] + [0]
        year_inflation = (self.curr_inflation / 100) / 12 # czemu nie 24?
        interest_rates = [0.00542] + [self.NBP / 100 for _ in range(23)] # pownno byc +0,5%
        last_accumulated_inflation = 0
        last_accumulated_interests = 0
        last_value = start_value

        titles = ['Value', 'Interest Rate', 'Interests', 'Accumulated Interests', 'Redemption Fee',
                  'Belka Tax', 'Net Profit', 'Cycle Inflation', 'Accumulated Inflation', 'Total Profit',
                  'Total Profit %']
        data = pd.DataFrame(columns=titles)

        first_row = [start_value] + [0 for _ in range(10)]
        data.loc[len(data)] = first_row

        for i in range(24):
            # value = self.calculate_value(last_value, interest_rates[i])
            value = start_value
            interest_rate = interest_rates[i]
            interests = last_value * interest_rate
            accumulated_interests = last_accumulated_interests + interests
            # belka_tax = BELKA_TAX * (accumulated_interests - redemption_fee[i])
            belka_tax = BELKA_TAX * interests
            net_profit = self.calculate_net_profit(accumulated_interests, redemption_fee[i])
            accumulated_inflation = (1 - last_accumulated_inflation) * year_inflation + last_accumulated_inflation
            total_profit = (start_value + net_profit) * (1 - accumulated_inflation) - start_value
            total_profit_percent = total_profit / start_value

            row = [round(value, 2), round(interest_rate, 2), round(interests, 2),
                   round(accumulated_interests, 2),
                   round(redemption_fee[i], 2), round(belka_tax, 2), round(net_profit, 2),
                   round(year_inflation * 100, 2), round(accumulated_inflation * 100, 2),
                   round(total_profit, 2), round(total_profit_percent * 100, 2)]

            data.loc[len(data)] = row

            last_value = value
            last_accumulated_interests = accumulated_interests
            last_accumulated_inflation = accumulated_inflation
        return data

    def calculate_TOS(self, start_value):
        print("calculating TOS")

        redemption_fee_per_bond = 0.7  # w tysiacach
        n = self.number_of_bonds
        redemption_fee = [redemption_fee_per_bond * n for _ in range(2)] + [0] + [0]
        year_inflation = self.curr_inflation / 100
        interest_rates = [0.06] + [0.06 for _ in range(2)]
        last_accumulated_inflation = 0
        last_accumulated_interests = 0
        last_value = start_value

        titles = ['Value', 'Interest Rate', 'Interests', 'Accumulated Interests', 'Redemption Fee',
                  'Belka Tax', 'Net Profit', 'Year Inflation', 'Accumulated Inflation', 'Total Profit',
                  'Total Profit %']
        data = pd.DataFrame(columns=titles)

        first_row = [start_value] + [0 for _ in range(10)]
        data.loc[len(data)] = first_row

        for i in range(3):
            value = self.calculate_value(last_value, interest_rates[i])
            interest_rate = interest_rates[i]
            interests = last_value * interest_rate
            accumulated_interests = last_accumulated_interests + interests
            belka_tax = BELKA_TAX * (accumulated_interests - redemption_fee[i])
            net_profit = self.calculate_net_profit(accumulated_interests, redemption_fee[i])
            accumulated_inflation = (1 - last_accumulated_inflation) * year_inflation + last_accumulated_inflation
            total_profit = (start_value + net_profit) * (1 - accumulated_inflation) - start_value
            total_profit_percent = total_profit / start_value

            row = [round(value, 2), round(interest_rate, 2), round(interests, 2),
                   round(accumulated_interests, 2),
                   round(redemption_fee[i], 2), round(belka_tax, 2), round(net_profit, 2),
                   round(year_inflation * 100, 2), round(accumulated_inflation * 100, 2),
                   round(total_profit, 2), round(total_profit_percent * 100, 2)]

            data.loc[len(data)] = row

            last_value = value
            last_accumulated_interests = accumulated_interests
            last_accumulated_inflation = accumulated_inflation
        return data

    def calculate_COI(self, start_value):
        print("calculating COI")

        redemption_fee_per_bond = 0.7  # w tysiacach
        n = self.number_of_bonds
        redemption_fee = [redemption_fee_per_bond * n for _ in range(3)] + [0] + [0]
        year_inflation = self.curr_inflation / 100
        interest_rates = [0.0675] + [(year_inflation + 0.0125) for _ in range(3)]
        last_accumulated_inflation = 0
        last_accumulated_interests = 0
        last_value = start_value

        titles = ['Value', 'Interest Rate', 'Interests', 'Accumulated Interests', 'Redemption Fee',
                  'Belka Tax', 'Net Profit', 'Year Inflation', 'Accumulated Inflation', 'Total Profit',
                  'Total Profit %']
        data = pd.DataFrame(columns=titles)

        first_row = [start_value] + [0 for _ in range(10)]
        data.loc[len(data)] = first_row

        for i in range(4):
            # value = self.calculate_value(last_value, interest_rates[i])
            value = start_value
            interest_rate = interest_rates[i]
            interests = last_value * interest_rate
            accumulated_interests = last_accumulated_interests + interests
            belka_tax = BELKA_TAX * interests
            net_profit = self.calculate_net_profit(accumulated_interests, redemption_fee[i])
            accumulated_inflation = (1 - last_accumulated_inflation) * year_inflation + last_accumulated_inflation
            total_profit = (start_value + net_profit) * (1 - accumulated_inflation) - start_value
            total_profit_percent = total_profit / start_value

            row = [round(value, 2), round(interest_rate, 2), round(interests, 2),
                   round(accumulated_interests, 2),
                   round(redemption_fee[i], 2), round(belka_tax, 2), round(net_profit, 2),
                   round(year_inflation * 100, 2), round(accumulated_inflation * 100, 2),
                   round(total_profit, 2), round(total_profit_percent * 100, 2)]

            data.loc[len(data)] = row

            last_value = value
            last_accumulated_interests = accumulated_interests
            last_accumulated_inflation = accumulated_inflation
        return data

    def calculate_EDO(self, start_value):
        redemption_fee_per_bond = 2
        n = self.number_of_bonds
        redemption_fee = [redemption_fee_per_bond * n for _ in range(9)] + [0] + [0]
        year_inflation = self.curr_inflation / 100
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
            beam_belka_tax = BELKA_TAX * (accumulated_interests - redemption_fee[i])
            net_profit = self.calculate_net_profit(accumulated_interests, redemption_fee[i])
            accumulated_inflation = (1 - last_accumulated_inflation) * year_inflation + last_accumulated_inflation
            total_profit = (start_value + net_profit) * (1 - accumulated_inflation) - start_value
            total_profit_percent = total_profit / start_value

            row = [round(value, 2), round(interest_rate, 2), round(interests, 2),
                   round(accumulated_interests, 2),
                   round(redemption_fee[i], 2), round(beam_belka_tax, 2), round(net_profit, 2),
                   round(year_inflation * 100, 2), round(accumulated_inflation * 100, 2),
                   round(total_profit, 2), round(total_profit_percent * 100, 2)]

            data.loc[len(data)] = row

            last_value = value
            last_accumulated_interests = accumulated_interests
            last_accumulated_inflation = accumulated_inflation

        return data

    def calculate_ROS(self, start_value):
        print("calculating ROS")

        redemption_fee_per_bond = 0.7 # w tysiacach
        n = self.number_of_bonds
        redemption_fee = [redemption_fee_per_bond * n for _ in range(5)] + [0] + [0]
        year_inflation = self.curr_inflation / 100
        interest_rates = [0.0695] + [(year_inflation + 0.0175) for _ in range(5)]
        last_accumulated_inflation = 0
        last_accumulated_interests = 0
        last_value = start_value

        titles = ['Value', 'Interest Rate', 'Interests', 'Accumulated Interests', 'Redemption Fee',
                  'Belka Tax', 'Net Profit', 'Year Inflation', 'Accumulated Inflation', 'Total Profit',
                  'Total Profit %']
        data = pd.DataFrame(columns=titles)

        first_row = [start_value] + [0 for _ in range(10)]
        data.loc[len(data)] = first_row

        for i in range(6):
            value = self.calculate_value(last_value, interest_rates[i])
            interest_rate = interest_rates[i]
            interests = last_value * interest_rate
            accumulated_interests = last_accumulated_interests + interests
            belka_tax = BELKA_TAX * (accumulated_interests - redemption_fee[i])
            net_profit = self.calculate_net_profit(accumulated_interests, redemption_fee[i])
            accumulated_inflation = (1 - last_accumulated_inflation) * year_inflation + last_accumulated_inflation
            total_profit = (start_value + net_profit) * (1 - accumulated_inflation) - start_value
            total_profit_percent = total_profit / start_value

            row = [round(value, 2), round(interest_rate, 2), round(interests, 2),
                   round(accumulated_interests, 2),
                   round(redemption_fee[i], 2), round(belka_tax, 2), round(net_profit, 2),
                   round(year_inflation * 100, 2), round(accumulated_inflation * 100, 2),
                   round(total_profit, 2), round(total_profit_percent * 100, 2)]

            data.loc[len(data)] = row

            last_value = value
            last_accumulated_interests = accumulated_interests
            last_accumulated_inflation = accumulated_inflation
        return data

    def calculate_ROD(self, start_value):
        print("calculating ROD")

        redemption_fee_per_bond = 2  # w tysiacach
        n = self.number_of_bonds
        redemption_fee = [redemption_fee_per_bond * n for _ in range(11)] + [0] + [0]
        year_inflation = self.curr_inflation / 100
        interest_rates = [0.0725] + [(year_inflation + 0.02) for _ in range(11)]
        last_accumulated_inflation = 0
        last_accumulated_interests = 0
        last_value = start_value

        titles = ['Value', 'Interest Rate', 'Interests', 'Accumulated Interests', 'Redemption Fee',
                  'Belka Tax', 'Net Profit', 'Year Inflation', 'Accumulated Inflation', 'Total Profit',
                  'Total Profit %']
        data = pd.DataFrame(columns=titles)

        first_row = [start_value] + [0 for _ in range(10)]
        data.loc[len(data)] = first_row

        for i in range(12):
            value = self.calculate_value(last_value, interest_rates[i])
            interest_rate = interest_rates[i]
            interests = last_value * interest_rate
            accumulated_interests = last_accumulated_interests + interests
            belka_tax = BELKA_TAX * (accumulated_interests - redemption_fee[i])
            net_profit = self.calculate_net_profit(accumulated_interests, redemption_fee[i])
            accumulated_inflation = (1 - last_accumulated_inflation) * year_inflation + last_accumulated_inflation
            total_profit = (start_value + net_profit) * (1 - accumulated_inflation) - start_value
            total_profit_percent = total_profit / start_value

            row = [round(value, 2), round(interest_rate, 2), round(interests, 2),
                   round(accumulated_interests, 2),
                   round(redemption_fee[i], 2), round(belka_tax, 2), round(net_profit, 2),
                   round(year_inflation * 100, 2), round(accumulated_inflation * 100, 2),
                   round(total_profit, 2), round(total_profit_percent * 100, 2)]

            data.loc[len(data)] = row

            last_value = value
            last_accumulated_interests = accumulated_interests
            last_accumulated_inflation = accumulated_inflation
        return data

    def calculate_value(self, value, interest):
        return value * (interest + 1)

    def calculate_net_profit(self, accumulated_interests, redemption_fee):
        return accumulated_interests - redemption_fee - BELKA_TAX * (accumulated_interests - redemption_fee)


if __name__ == "__main__":
    calc = TreasuryBondCalculator()
    #calc.main(["EDO", 1000, 12.4, 150])
    #calc.main(["ROS", 1000, 12.4, 80])
    #calc.main(["ROD", 1000, 12.4, 121]) # czemu pojawia sie az 13 lat dla >120 a dla 120 tylko 10 lat...
    #calc.main(["TOS", 1000, 12.4, 40])
    #calc.main(["COI", 1000, 12.4, 50]) # bez kapitalizacji

    # miesiecznie i wszystkie bez kapitalizcji
    #OTS
    #calc.main(["OTS", 1000, 12.4, 40]) #


    # ROR i DOR DO NAPRAWY
    #ROR
    calc.main(["ROR", 1000, 12.4, 121, 5.25])  # bez kapitalizacji, CZEMU 13 MIESIECY, net profit coś nie tak
    #DOR
    # calc.main(["DOR", 1000, 12.4, 121, 0.479])  # bez kapitalizacji, CZEMU 13 MIESIECY
    # może wszedzie dac Cycle Inflation a nie Year Inflation? - bo przy miesiecznych to sie zmienia
    # bondos = {
    #     "EDO": (7, 1.5, "Year", 2, 10, True, None),
    #     "ROS": (6.95, 1.75, "Year", 0.7, 6, True, None),
    #     "TOS": (6.6, None, "Year", 0.7, 3, True, None),
    #     "COI": (6.75, 1.25, "Year", 0.7, 4, False, None),
    #     "OTS": (3 / 12, None, "Month", 0, 3, False, None),  # 3% roczne oprcentowanie ale na miesiac to 0,25
    #     "ROR": (6.25 / 12, None, "Month", 0.5, 12, False, 0),
    #     # bierzemy % NBP i dzielimy przez 12; 0 bo dodajemy 0 do NBP
    #     "DOR": (6.5 / 12, None, "Month", 0.7, 24, False, 0.5),  # bierzemy % NBP i dzielimy przez 12
    # }
    # args = ["EDO", 1000, 12.4, 150]
    # print(bondos[args[0]][2])