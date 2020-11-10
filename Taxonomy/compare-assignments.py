#!/usr/bin/env python3
import os
from typing import Dict, List
from arg_parse import ArgParse
from collections import namedtuple

"""
Script will take file in format:
TARA_ARC_108_MAG_00273	Chromista	Ciliophora	Oligotrichea    Choreotrichida	Rhabdonellidae	Schmidingerella Eukarya	Chromista   Unique	Schmidingerella

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


Taxonomy = namedtuple("Taxonomy", ("kingdom", "phylum", "class", "order", "family", "genus"))


def load_delmont(file_path: str) -> Dict[str, Taxonomy]:
    pass


def load_eukms(file_path: str) -> Dict[str, Taxonomy]:
    pass


def generate_comparison_matrix(delmont: Dict[str, Taxonomy], eukms: Dict[str, Taxonomy]) -> List[List[int]]:
    pass


def write_to_file(file_path: str, output_data: List[List[int]]):
    pass


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
        generate_comparison_matrix(load_delmont(ap.args.delmont), load_eukms(ap.args.eukms))
    )
