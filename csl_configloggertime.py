import logging
import os
import time
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

from config_names import FILENAME_MAIN


class ConfigLogerTiming:
    """Class for configuring the timer, logging, etc."""

    def __init__(self):
        self.folder_for_logs = "logs"
        self.start_time = time.time()
        self.iteration_index = 0
        self.last_iteration_period = 0
        self.list_iteration_periods = []
        self.total_iterations = 0
        self.saving_period = 10
        self.loop_beginning_time = None
        self.loop_end_time = None
        self.logger = self.setup_logger()

    def iter_number(self, index_of_iteration):
        """Calculate number of iteration.
        :param index_of_iteration: Index of iteration
        :return: Number of iteration"""
        self.iteration_index = index_of_iteration
        return index_of_iteration

    def calculate_average_iteration_time(self):
        """Calculate average time for an iteration.
        :return: Average time for an iteration"""

        if len(self.list_iteration_periods) == 0:
            return 45
        else:
            return sum(self.list_iteration_periods) / len(self.list_iteration_periods)

    def time_elapsed(self):
        """Calculate time elapsed since the script started.
        :return: str Time elapsed"""

        elapsed_time = time.time() - self.start_time
        d_h_m_s = str(datetime.timedelta(seconds=elapsed_time)).split(':')
        return datetime.timedelta(seconds=elapsed_time), d_h_m_s

    def time_left(self):
        """Calculate time left for the script to run.
        :return: str Time left"""

        elapsed_time = time.time() - self.start_time
        time_per_iteration = elapsed_time / (self.iteration_index + 1)
        time_left = (self.total_iterations - self.iteration_index) * time_per_iteration
        return str(datetime.timedelta(seconds=time_left))

    def work_elapsed(self):
        """Calculate work elapsed since the script started.
        :return: str % elapsed"""

        return f"{round(self.iteration_index / self.total_iterations * 100, 2)}%"

    def work_left(self):
        """Calculate work left for the script to run.
        :return: str % left"""

        return f"{round((self.total_iterations - self.iteration_index) / self.total_iterations * 100, 2)}%"

    def exp_time_end(self):
        """Calculate time when the script will end.
        :return: str Time when the script will end"""

        time_end = self.start_time + (
                self.total_iterations - self.iteration_index) * self.calculate_average_iteration_time()
        return datetime.datetime.fromtimestamp(time_end).strftime('%Y-%m-%d %H:%M:%S')

    def setup_logger(self):
        """Set up logger."""
        logger = logging.getLogger('my_logger')
        logger.setLevel(logging.DEBUG)

        os.makedirs(self.folder_for_logs, exist_ok=True)  # Create the 'logs' folder if it doesn't exist

        log_file = os.path.join(self.folder_for_logs, 'mylog.log')
        timed_rotating_handler = TimedRotatingFileHandler(log_file, when='m', interval=self.saving_period,
                                                          encoding='utf-8')
        timed_rotating_handler.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()  # StreamHandler is displaying logs on the console
        console_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        timed_rotating_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)  # Set the formatter for the console handler

        logger.addHandler(timed_rotating_handler)
        logger.addHandler(console_handler)  # Add the console handler to the logger

        return logger

    def pre_scrape(self, total_iterations):
        """Print info before the scraping.
        What we are going to do:
        - set up logger
        Show some analytics:
        - time elapsed
        - time left
        - work elapsed
        - work left
        - average time per iteration
        - time end"""

        self.total_iterations = total_iterations
        self.logger.info(f"Total links to scrape: {self.total_iterations}")
        self.logger.info(f"We are going to scrape data for all links")
        self.logger.info(f"Logs will be saved to new file every {self.saving_period} minutes.")
        self.logger.info(f"We are going to recalculate average time per iteration every iteration.")
        self.logger.info(f"Time start:"
                         f" {datetime.datetime.fromtimestamp(self.start_time).strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info(f"Expected average time per iteration: {self.calculate_average_iteration_time()}")
        self.logger.info(f"Expected time end: {self.exp_time_end()}")

    def post_scrape(self):
        """Print info after the scraping.
        What we have done:
        - time elapsed
        - average time per iteration
        - time end.
        Where we saved the data:
        - logs
        - data"""

        self.logger.info(f"Time end: {datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info(f"Time elapsed: {self.time_elapsed()[0]}")
        self.logger.info(f"Average time per iteration: {self.calculate_average_iteration_time()}")
        self.logger.info(f"Expected time end: {self.exp_time_end()}")
        self.logger.info(f"All data was scraped successfully!")
        self.logger.info(f"Logs were saved to '{self.folder_for_logs}' folder.")
        self.logger.info(f"Data was saved as '{FILENAME_MAIN}' file.")

    def iteration_start(self, iter_index, lnk):
        """Print info before the iteration.
        What we are going to do:
        - time left
        - work left
        - average time per iteration
        - time end"""
        self.logger.info("\n")
        self.logger.info('-' * 120)
        self.iter_number(iter_index)
        self.logger.info(f"Starting iteration {iter_index} of {self.total_iterations}...")
        self.logger.info(f"Website: {lnk}")
        if iter_index != 0:
            self.logger.info(f"Work have done: {self.work_elapsed()}")
            self.logger.info(f"Average time per iteration: {self.calculate_average_iteration_time()}")
        self.loop_beginning_time = time.time()

    def iteration_end(self, iter_index):
        """Print info after the iteration.
        What we have done:
        - time elapsed
        - time left
        - work elapsed
        - work left
        - average time per iteration
        - time end"""

        if iter_index != 0:
            self.logger.info(f"Time elapsed: {self.last_iteration_period}")
            self.logger.info(f"Time left: {self.time_left()}")
            self.logger.info(f"Work elapsed: {self.work_elapsed()}")
            self.logger.info(f"Work left: {self.work_left()}")
            self.logger.info(f"Average time per iteration: {self.calculate_average_iteration_time()}")
        self.logger.info(f"Expected time end: {self.exp_time_end()}")
        self.logger.info(f"Iteration {iter_index + 1} of {self.total_iterations} was successfully!")
        self.logger.info(f"Data was saved to '{FILENAME_MAIN}' file.")
        self.loop_end_time = time.time()
        self.last_iteration_period = self.loop_end_time - self.loop_beginning_time
        self.list_iteration_periods += [self.last_iteration_period]
        self.logger.info(f"Last iteration took {self.last_iteration_period}")
        self.logger.info('-' * 120 + '\n')
