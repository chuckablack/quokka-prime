from datetime import datetime, timedelta
import time
from db_apis import trim_tables, create_summaries


class DbHourlyTask:

    def __init__(self):
        self.terminate = False
        self.current_hour = str(datetime.now())[:13]
        print("---> starting background db hourly task")

    def set_terminate(self):
        if not self.terminate:
            self.terminate = True
            print("\n\n...gracefully exiting db_hourly_task_thread")

    def start(self):

        while True and not self.terminate:

            this_hour = str(datetime.now())[:13]
            if this_hour == self.current_hour:
                time.sleep(15)
                continue

            # trim old data from status and diagnostic tables
            status_expire_after = datetime.now() - timedelta(hours=24)
            diagnostics_expire_after = datetime.now() - timedelta(hours=2)
            trim_tables(status_expire_after, diagnostics_expire_after)

            # create hourly summaries from status tables
            create_summaries(self.current_hour)

            self.current_hour = this_hour

        print("db_hourly_task_thread exit complete")
