from typing import List, Dict
from TARAVisualize.backend.data import os

tax_levels = ("kingdom", "clade", "phylum", "class", "order", "family", "genus")


def generate_summary_taxonomy_file(file_list: List[str], out_path: str):
    w = open(out_path, "w")
    w.write("".join(("\t".join(tax_levels), "\n")))
    for file in file_list:
        file_data = get_data_from_file(file)
        w.write("".join(("\t".join((file_data[t] for t in tax_levels)), "\n")))
    w.close()


def get_data_from_file(file_path: str) -> Dict[str, str]:
    if not os.path.exists(file_path):
        exit()
    r = open(file_path, "r")
    i = 0
    data = {tax: "" for tax in tax_levels}
    for line in r:
        line = line.rstrip("\r\n").split()
        if line[3] in tax_levels and data[line[3]] == "":
            data[line[3]] = line[5]
        i += 1
        if i > 15:
            break
    return data
