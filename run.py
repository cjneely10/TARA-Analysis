#!/usr/bin/env python
import os
from plumbum import cli
from plumbum import local


class RunStreamlit(cli.Application):
    def main(self):
        print("Launching streamlit...")
        try:
            local["streamlit"]["run",
                               os.path.join(os.path.dirname(__file__), "TARAVisualize", "main.py")]()
        except KeyboardInterrupt:
            print("\nEnding streamlit...")


if __name__ == "__main__":
    RunStreamlit.run()
