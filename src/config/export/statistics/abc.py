import abc


class BaseStatisticsQueryHelper(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_survey_qs(self):
        pass

    @abc.abstractmethod
    def get_magnification_factor_map(self):
        pass

    @abc.abstractmethod
    def get_survey_map(self):
        pass

    @abc.abstractmethod
    def get_lack_farmer_ids(self):
        pass

    @classmethod
    @abc.abstractmethod
    def get_region(cls, survey):
        pass

    def __init__(self):
        self.survey_qs = self.get_survey_qs()
        self.magnification_factor_map = self.get_magnification_factor_map()
        self.survey_map = self.get_survey_map()
        self.lack_farmer_ids = self.get_lack_farmer_ids()
