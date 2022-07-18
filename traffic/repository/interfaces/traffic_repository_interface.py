from abc import ABC, abstractmethod


class TrafficRepositoryInterface(ABC):
    @abstractmethod
    def query_jams_by_date(self, start_date, finish_date, commune, length, delay):
        pass

    @abstractmethod
    def query_jams_by_date_no_commune(self, start_date, finish_date, length, delay):
        pass

    @abstractmethod
    def query_jams_by_date_and_range_time(
        self, start_date, finish_date, commune, length, delay, init_time, finish_time
    ):
        pass

    @abstractmethod
    def query_jams_by_date_and_range_time_no_commune(
        self, start_date, finish_date, length, delay, init_time, finish_time
    ):
        pass
