# Singleton Class (has only one instance per class)
class StockInformationConfigurator:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(StockInformationConfigurator, cls).__new__(cls)
        return cls._instance

    def __init__(self, period=None, companies_day=None, companies_month=None, companies_year=None, last_update_time=None):
        if companies_day is None:
            companies_day = [("Test", 0, 0, 0)]
        if not hasattr(self, '_initialized'):
            self.period = period
            self._companies_day = companies_day
            self._companies_month = companies_month
            self._companies_year = companies_year
            self.last_update_time = last_update_time
            self._initialized = True

    @property
    def companies_day(self):
        return self._companies_day

    @companies_day.setter
    def companies_day(self, value):
        self._companies_day = value

    @property
    def companies_month(self):
        return self._companies_month

    @companies_month.setter
    def companies_month(self, value):
        self._companies_month = value

    @property
    def companies_year(self):
        return self._companies_year

    @companies_year.setter
    def companies_year(self, value):
        self._companies_year = value

    @property
    def last_update_time(self):
        return self._last_update_time

    @last_update_time.setter
    def last_update_time(self, value):
        self._last_update_time = value