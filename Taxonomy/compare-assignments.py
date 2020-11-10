#!/usr/bin/env python3
import os
import numpy as np
from arg_parse import ArgParse
from collections import namedtuple
from typing import Dict, List, Tuple

"""
Script will take file in format:
TARA_ARC_108_MAG_00273			Chromista	Ciliophora	Oligotrichea	Choreotrichida	Rhabdonellidae	Schmidingerella

And compare it to file in format:
TARA_ARC_108_MAG_00273
kingdom Viridiplantae
phylum Chromerida
class Spirotrichea
order Tintinnida
family Rhabdonellidae
genus Schmidingerella

To generate and output a matrix where rows are MAG id, columns are the taxonomic levels, and the data values are
1 or 0 if the data comparison values are the same

"""

FIELDS = ("kingdom", "phylum", "cclass", "order", "family", "genus")
Taxonomy = namedtuple("Taxonomy", FIELDS)
Taxonomy.__new__.__defaults__ = ("",) * len(FIELDS)


def load_delmont(file_path: str) -> Dict[str, Taxonomy]:
    r = open(file_path, "r")
    out = {}
    for line in r:
        line = line.rstrip("\r\n").split("\t")
        out[line[0]] = Taxonomy(*line[1:7])
    return out


def load_eukms(file_path: str) -> Dict[str, Taxonomy]:
    r = open(file_path, "r")
    out = {}
    # Get and store name of MAG
    line = next(r).rstrip("\r\n").split()
    while r:
        data = {"_id": line[0]}
        # Get next line which start the taxonomy assignment information
        try:
            line = next(r)
        except StopIteration:
            break
        line = line.rstrip("\r\n").split()
        # While not at next end of line or at next mag
        while len(line) != 1:
            if line[0] == "class":
                line[0] = "cclass"
            data[line[0]] = line[1]
            try:
                line = next(r)
            except StopIteration:
                break
            line = line.rstrip("\r\n").split()
        # Store taxonomy object
        _id = data["_id"]
        del data["_id"]
        out[_id] = Taxonomy(**data)

    assert len(list(out.keys())) == 682, print(len(list(out.keys())))  # Adjusted to remove Metagenome_centric_SAG
    return out


def generate_comparison_matrix(delmont: Dict[str, Taxonomy], eukms: Dict[str, Taxonomy]) -> Tuple[List[str], np.ndarray, int]:
    keys = sorted(list(eukms.keys()))
    out = np.zeros((len(keys), len(FIELDS) - 1), dtype="int8")
    z = 0
    for i, key in enumerate(keys):
        if key in delmont.keys():
            z += 1
            for k in range(0, len(FIELDS)):
                for l in range(len(FIELDS)):
                    if eukms[key][l] != "" and eukms[key][l].lower() in delmont[key][k].lower():
                        out[i, l - 1] = 1
    return keys, out, z


def write_to_file(file_path: str, output_data: Tuple[List[str], List[List[int]], int]):
    w = open(file_path, "w")
    for name, data in zip(output_data[0], output_data[1]):
        w.write("".join((name, "\t", "\t".join(map(str, data)), "\n")))
    w.close()
    non_zero = 0
    for row in output_data[1]:
        if np.sum(row) != 0:
            non_zero += 1
    print(non_zero, output_data[2])


if __name__ == "__main__":
    ap = ArgParse(
        (
            (("-d", "--delmont"),
             {"help": "Path to Delmont file", "required": True}),
            (("-e", "--eukms"),
             {"help": "Path to EukMS file", "required": True}),
            (("-o", "--output"),
             {"help": "Output data matrix path, default stdout", "default": "/dev/stdout"}),
        ),
        description="Compare EukMS annotation to delmont-derived data"
    )
    if not os.path.exists(ap.args.delmont):
        print("Provide valid Delmont path")
        exit(1)
    if not os.path.exists(ap.args.eukms):
        print("Provide valid EukMS path")
        exit(1)

    write_to_file(
        ap.args.output,
        generate_comparison_matrix(load_delmont(ap.args.delmont), load_delmont(ap.args.eukms))
    )
