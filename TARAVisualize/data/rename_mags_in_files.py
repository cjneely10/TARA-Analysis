#!/usr/bin/env python
import re
import sys
from pathlib import Path
from typing import Dict

from plumbum import cli


class MAGRenamer(cli.Application):
    rename_dict: Dict[str, str]
    output_path: Path = Path("/dev/stdout")

    @cli.switch(["-i", "--ids_file"], str, mandatory=True)
    def load_ids(self, ids_file):
        self.rename_dict = {}
        with open(ids_file, "r") as ids_ptr:
            # Skip header
            next(ids_ptr)
            # Read rest of file into dict
            for line in ids_ptr:
                line = line.rstrip("\r\n").split()
                self.rename_dict[line[0]] = line[1]

    @cli.switch(["-o", "--output"], str)
    def set_output_path(self, output_path):
        self.output_path = Path(output_path).resolve()

    def main(self):
        self._fix_file()

    def _fix_file(self):
        out_ptr = open(self.output_path, "w")
        for line in sys.stdin:
            for old_id, new_id in self.rename_dict.items():
                line = re.sub(old_id, new_id, line, count=0)
            out_ptr.write(line)
        out_ptr.close()


if __name__ == "__main__":
    MAGRenamer.run()
