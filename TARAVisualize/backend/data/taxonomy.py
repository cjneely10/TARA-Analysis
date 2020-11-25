#!/usr/bin/env python
from typing import List, Dict
from plumbum import cli
from glob import glob


tax_levels = ("kingdom", "clade", "phylum", "class", "subclass", "order", "family", "genus", "species")


def generate_summary_taxonomy_file(file_list: List[str], out_path: str):
    w = open(out_path, "w")
    w.write("".join(("\t".join(tax_levels), "\n")))
    for file in file_list:
        file_data = get_data_from_file(file)
        w.write("".join(("\t".join((file_data[t] for t in tax_levels)), "\n")))
    w.close()


def get_data_from_file(file_path: str) -> Dict[str, str]:
    r = open(file_path, "r")
    i = 0
    data = {tax: "." for tax in tax_levels}
    for line in r:
        line = line.rstrip("\r\n").split()
        if line[3] in tax_levels:
            data[line[3]] = line[5]
        i += 1
        if line[3] == "species" or i > 30:
            break
    return data


class TaxonomyApp(cli.Application):
    file_glob = cli.SwitchAttr(["-i", "--input-glob"], mandatory=True,
                               help="Glob for all tax-report.txt files to merge for results")
    output_path = cli.SwitchAttr(["-o", "--output"], mandatory=True, help="Output path of summary file")

    def main(self):
        generate_summary_taxonomy_file(glob(self.file_glob), self.output_path)


if __name__ == "__main__":
    TaxonomyApp.run()
