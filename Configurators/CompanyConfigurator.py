# Singleton Class (has only one instance per class)
class CompanyConfigurator:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CompanyConfigurator, cls).__new__(cls)
        return cls._instance

    def __init__(self, company_name=None, growth=None, percentage_growth=None):
        if not hasattr(self, '_initialized'):
            self._company_name = company_name
            self._growth = growth
            self._percentage_growth = percentage_growth
            self._initialized = True

    @property
    def company_name(self):
        return self._company_name

    @company_name.setter
    def company_name(self, value):
        self._company_name = value

    @property
    def growth(self):
        return self._growth

    @growth.setter
    def growth(self, value):
        self._growth = value

    @property
    def percentage_growth(self):
        return self._percentage_growth

    @percentage_growth.setter
    def percentage_growth(self, value):
        self._percentage_growth = value