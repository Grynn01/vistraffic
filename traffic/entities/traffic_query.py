from dataclasses import dataclass
from datetime import datetime
import utils
from dateutil import parser


@dataclass
class TrafficQuery:
    start_date: datetime
    finish_date: datetime
    top_jams: int
    commune: str
    length: int
    delay: int
    start_time: int = None
    finish_time: int = None
    server_delay: int = 4

    def format(self):
        self.start_date = utils.adjust_to_server_datetime(
            parser.isoparse(self.start_date)
        )
        self.finish_date = utils.adjust_to_server_datetime(
            parser.isoparse(self.finish_date)
        )
        self.finish_date = utils.add_one_day(self.finish_date)
        self.top_jams = int(self.top_jams)
        self.length = int(self.length)
        self.delay = int(self.delay)
        if self.start_time:
            self.start_time = int(self.start_time.split(":")[0]) + self.server_delay
        if self.finish_time:
            self.finish_time = int(self.finish_time.split(":")[0]) + self.server_delay
