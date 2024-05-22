class Bonds:
    @staticmethod
    def get_bonds():
        return Bonds.bonds

    bonds = {
        "ROD": (7.05, 2.0, "Year", 2, 144, True, None),
        "EDO": (6.8, 1.5, "Year", 2, 120, True, None),
        "ROS": (6.75, 1.75, "Year", 0.7, 72, True, None),
        "TOS": (6.4, None, "Year", 0.7, 36, True, None),
        "COI": (6.55, 1.25, "Year", 0.7, 48, False, None),
        "OTS": (3 / 12, None, "Month", 0, 3, False, None),  # 3% roczne oprcentowanie ale na miesiac to 0,25
        "ROR": (6.05 / 12, None, "Month", 0.5, 12, False, 0), # bierzemy % NBP i dzielimy przez 12; 0 bo dodajemy 0 do NBP
        "DOR": (6.3 / 12, None, "Month", 0.7, 24, False, 0.5),  # bierzemy % NBP i dzielimy przez 12
    }

