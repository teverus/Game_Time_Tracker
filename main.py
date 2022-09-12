import os
from datetime import datetime as dt
from datetime import timedelta
from time import sleep

import psutil
import yaml
from pandas import DataFrame

from Code.BaseTable import BaseTable
from Code.constants import (
    Column,
    GAME_TIME,
    FILES,
    TIME_FORMAT,
    PROCESS_IS_ACTIVE,
    START,
    FINISH, NAME, PROCESS,
)
from Code.functions.db import append_to_table, update_a_table, read_table


class Application:
    def __init__(self):
        os.system("cls")

        self.polling_timeout = 1
        self.stats = {}
        self.applications = self.get_applications()

        self.show_application_stats()
        self.start_tracking_applications()

    def show_application_stats(self):
        df = read_table(GAME_TIME, FILES)
        BigDict = {}
        for application in self.applications:
            app_name = application[NAME]
            time_spent_stats = df.loc[df.Name == app_name].Spent
            time_spent = sum([self.get_time_in_seconds(t) for t in time_spent_stats])
            hours = int(time_spent / 3600)
            minutes = int((time_spent - (hours * 3600)) / 60)
            seconds = time_spent - (hours * 3600) - (minutes * 60)
            BigDict[app_name] = f"{hours:02}:{minutes:02}:{seconds:02}"

        # TODO Добавить заголовки колонок
        # TODO Можно не указывать table_width

        table = BaseTable(
            table_title="Hello world",
            rows=[["Hello", "100", "Yes"], ["world", "222", " "]],
            table_width=101
        ).print_table()
        a = 1

    def start_tracking_applications(self):
        for app in self.applications:
            print(f'''Tracking "{app[NAME]}" with process "{app[PROCESS]}"''')

        while True:

            for application in self.applications:
                app_name = application[NAME]
                app_process = application[PROCESS]

                if app_name not in self.stats:
                    self.stats[app_name] = {PROCESS_IS_ACTIVE: False}

                if self.check_if_process_exists(app_process):
                    if not self.stats[app_name][PROCESS_IS_ACTIVE]:
                        self.stats[app_name][START] = self.get_time()
                        self.record_app_name_and_start_time(app_name)

                        self.stats[app_name][PROCESS_IS_ACTIVE] = True

                        print(f"[{app_name}] Start @ {self.stats[app_name][START]}")

                else:
                    if self.stats[app_name][PROCESS_IS_ACTIVE]:
                        self.stats[app_name][FINISH] = self.get_time()
                        self.record_finish_time(app_name)
                        self.record_time_spent(app_name)

                        self.stats[app_name][PROCESS_IS_ACTIVE] = False

                        print(f"[{app_name}] Close @ {self.stats[app_name][FINISH]}")

                sleep(self.polling_timeout)

    @staticmethod
    def check_if_process_exists(process_name):
        for p in psutil.process_iter():
            if p.name() == process_name:
                return True

    @staticmethod
    def get_time(time_format=TIME_FORMAT):
        return dt.now().strftime(time_format)

    def record_app_name_and_start_time(self, app_name):
        df = DataFrame([], columns=Column.ALL)
        df.loc[0, Column.NAME] = app_name
        df.loc[0, Column.START] = self.stats[app_name][START]
        append_to_table(df, GAME_TIME, FILES)

    def record_finish_time(self, app_name):
        update_a_table(
            x_column=Column.START,
            x_value=self.stats[app_name][START],
            y_column=Column.FINISH,
            new_value=self.stats[app_name][FINISH],
            table_name=GAME_TIME,
            folder=FILES,
        )

    def record_time_spent(self, app_name):
        time_start = dt.strptime(self.stats[app_name][START], TIME_FORMAT)
        time_finish = dt.strptime(self.stats[app_name][FINISH], TIME_FORMAT)
        time_spend = str(time_finish - time_start)

        update_a_table(
            x_column=Column.START,
            x_value=self.stats[app_name][START],
            y_column=Column.SPENT,
            new_value=time_spend,
            table_name=GAME_TIME,
            folder=FILES,
        )

    @staticmethod
    def get_applications():
        with open("config.yml", "r") as stream:
            return yaml.safe_load(stream)["applications"]

    @staticmethod
    def get_time_in_seconds(time_as_string):
        time = dt.strptime(time_as_string, "%H:%M:%S")
        delta = timedelta(hours=time.hour, minutes=time.minute, seconds=time.second)

        return int(delta.total_seconds())


if __name__ == "__main__":
    Application()
