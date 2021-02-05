#!/usr/bin/env python3
import os
from glob import glob
from plumbum import cli
from typing import List, Dict
from collections import defaultdict

"""
Script will parse all files in a glob statement and generate a summary .tsv file
Currently only supports Alexander MAG naming scheme

From working directory:
./repeats.py -i "out/wdir/*/repeats_final/mask.final.tbl" -o repeats-summary.tsv

"""


def generate_summary_file(file_list: List[str], out_path: str):
    header = set()
    all_data: Dict[str, Dict[str, str]] = {}
    # Gather keys
    for _file in file_list:
        data = get_data_from_file(_file)
        for key in data.keys():
            header.add(key)
        all_data[_file.split("/")[2]] = data
    # Sort and begin writing data
    sorted_header: List[str] = sorted(list(header))
    w = open(out_path, "w")
    # Write header
    w.write("".join(("ID\t", "\t".join(sorted_header), "\n")))
    for record, record_dict in all_data.items():
        w.write("".join((
            record, "\t", "\t".join((
                record_dict[key] if key in record_dict.keys() else "0.0" for key in sorted_header
            )), "\n"
        )))
    w.close()


def get_data_from_file(file_path: str) -> Dict[str, str]:
    if os.path.getsize(file_path) == 0:
        return {}
    r = open(file_path, "r")
    _line: str = next(r)
    out = defaultdict(str)
    # Skip to beginning of summary
    while not _line.startswith("-"):
        _line = next(r)
    # Begin parsing
    line: List[str]
    for _line in r:
        if _line.startswith("="):
            break
        line = _line.rstrip("\r\n").split()
        if len(line) > 5:
            out[line[0]] = line[-4]
    return dict(out)


class RepeatsApp(cli.Application):
    file_glob = cli.SwitchAttr(["-i", "--input-glob"], mandatory=True,
                               help="Glob for all mask.final.tbl files to merge for results")
    output_path = cli.SwitchAttr(["-o", "--output"], mandatory=True, help="Output path of summary file")

    def main(self):
        generate_summary_file(glob(self.file_glob), self.output_path)


if __name__ == "__main__":
    RepeatsApp.run()
