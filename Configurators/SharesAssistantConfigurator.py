# Singleton Class (has only one instance per class)
class SharesAssistantConfigurator:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SharesAssistantConfigurator, cls).__new__(cls)
        return cls._instance

    def __init__(self, desired_risk=None, desired_return=None, companies=None, weights=None, results=None):
        if not hasattr(self, '_initialized'):
            self._desired_risk = desired_risk
            self._desired_return = desired_return
            self._companies = companies
            self._type_of_simulation = "standard"
            self._weights = weights
            self._results = results
            self._initialized = True

    @property
    def desired_risk(self):
        return self._desired_risk

    @desired_risk.setter
    def desired_risk(self, value):
        self._desired_risk = value

    @property
    def desired_return(self):
        return self._desired_return

    @desired_return.setter
    def desired_return(self, value):
        self._desired_return = value

    @property
    def companies(self):
        return self._companies

    @companies.setter
    def companies(self, value):
        self._companies = value

    @property
    def type_of_simulation(self):
        return self._type_of_simulation

    @type_of_simulation.setter
    def type_of_simulation(self, value):
        self._type_of_simulation = value

    @property
    def weights(self):
        return self._weights

    @weights.setter
    def weights(self, value):
        self._weights = value

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, value):
        self._results = value
