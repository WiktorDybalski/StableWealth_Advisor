# Singleton Class (has only one instance per class)
class SharesAssistantConfigurator:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SharesAssistantConfigurator, cls).__new__(cls)
        return cls._instance

    def __init__(self, desired_risk_min=None, desired_risk_max=None, desired_return_min=None, desired_return_max=None,
                 companies=None, weights=None, results=None):
        if not hasattr(self, '_initialized'):
            self._desired_risk_min = desired_risk_min
            self._desired_risk_max = desired_risk_max
            self._desired_return_min = desired_return_min
            self._desired_return_max = desired_return_max
            self._companies = companies
            self._type_of_simulation = "standard"
            self._weights = weights
            self._results = results
            self._initialized = True

    @property
    def desired_risk_min(self):
        return self._desired_risk_min

    @desired_risk_min.setter
    def desired_risk_min(self, value):
        self._desired_risk_min = value

    @property
    def desired_risk_max(self):
        return self._desired_risk_max

    @desired_risk_max.setter
    def desired_risk_max(self, value):
        self._desired_risk_max = value

    @property
    def desired_return_min(self):
        return self._desired_return_min

    @desired_return_min.setter
    def desired_return_min(self, value):
        self._desired_return_min = value

    @property
    def desired_return_max(self):
        return self._desired_return_max

    @desired_return_max.setter
    def desired_return_max(self, value):
        self._desired_return_max = value

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
