#!/usr/bin/env python
import os
from plumbum import cli
from plumbum import local


class RunStreamlit(cli.Application):
    threads: int = 3

    @cli.switch(["-t", "--threads"], int)
    def get_threads(self, threads):
        """
        Set number of threads to use to load data
        """
        if threads < 1:
            raise ValueError("Threads must be positive!")
        self.threads = threads

    def main(self):
        print("Launching streamlit...")
        try:
            local["streamlit"]["run",
                               os.path.join(os.path.dirname(__file__), "TARAVisualize", "main.py"),
                               "--", self.threads]()
        except KeyboardInterrupt:
            print("\nEnding streamlit...")


if __name__ == "__main__":
    RunStreamlit.run()
