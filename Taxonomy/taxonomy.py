#!/usr/bin/env python
from glob import glob
from plumbum import cli
from typing import List, Dict

"""
Script will parse all files in a glob statement and generate a summary .tsv file of taxonomic assignments
Currently only supports Alexander MAG naming scheme

From working directory:
./taxonomy.py -i "out/wdir/*/taxonomy/tax-report.txt" -o tax-summary.tsv
From summary directory:
./taxonomy.py -i "out/results/run/*/tax-report.txt" -o tax-summary.tsv

"""


tax_levels = ("kingdom", "clade", "phylum", "class", "subclass", "order", "family", "genus", "species")


def generate_summary_taxonomy_file(file_list: List[str], out_path: str):
    w = open(out_path, "w")
    w.write("".join(("ID\t", "\t".join(tax_levels), "\tregion\tdepth\tsize_fraction\n")))
    for file in file_list:
        prefix = file.split("/")[2]
        file_data = get_data_from_file(file)
        # Write header
        w.write("".join((
            prefix, "\t", "\t".join((file_data[t] for t in tax_levels)),
        )))
        # Write added info from file name metadata
        w.write("".join((
            "\t",
            "\t".join((
                "-".join(prefix.split("-")[0:2]), prefix.split("-")[2], "-".join(prefix.split("-")[3:]).split("_")[0]
            )),
            "\n"
        )))
    w.close()


def get_data_from_file(file_path: str) -> Dict[str, str]:
    r = open(file_path, "r")
    i = 0
    data = {tax: (".", 1.0) for tax in tax_levels}
    for line in r:
        line = line.rstrip("\r\n").split()
        if len(line) < 5:
            break
        if line[3] in tax_levels and line[5] not in ("environmental", "uncultured"):
            if data.get(line[3]) is None or float(line[0]) > data.get(line[3])[1]:
                data[line[3]] = (" ".join(line[5:]), float(line[0]))
        i += 1
        if (line[3] == "species" and i > 25) or i > 35:
            break
    return {t: d[0] for t, d in data.items()}


class TaxonomyApp(cli.Application):
    file_glob = cli.SwitchAttr(["-i", "--input-glob"], mandatory=True,
                               help="Glob for all tax-report.txt files to merge for results")
    output_path = cli.SwitchAttr(["-o", "--output"], mandatory=True, help="Output path of summary file")

    def main(self):
        generate_summary_taxonomy_file(glob(self.file_glob), self.output_path)


if __name__ == "__main__":
    TaxonomyApp.run()
