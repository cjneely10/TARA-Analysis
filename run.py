#!/usr/bin/env python
import os
from pathlib import Path
from plumbum import BG
from plumbum import cli
from plumbum import local


class StreamlitApp(cli.Application):
    base_directory = Path(os.path.dirname(__file__)).resolve()
    npm_start = None

    def main(self):
        local.cwd.chdir(os.path.join(self.base_directory, "TARAVisualize", "components", "component-template",
                                     "template", "my_component", "frontend"))
        try:
            self.npm_start = local["npm"]["run", "start"] & BG
            local.cwd.chdir(self.base_directory)
            local["streamlit"]["run", os.path.join(self.base_directory, "TARAVisualize", "main.py")]()

        except KeyboardInterrupt:
            del self.npm_start


if __name__ == "__main__":
    StreamlitApp.run()
