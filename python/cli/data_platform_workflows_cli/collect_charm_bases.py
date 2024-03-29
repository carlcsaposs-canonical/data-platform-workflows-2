# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.
"""Collect charm bases to build from charmcraft.yaml"""

import argparse
import json
import logging
import os
import pathlib
import sys

import yaml


def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    parser = argparse.ArgumentParser()
    parser.add_argument("--charm-directory", required=True)
    parser.add_argument("--cache", required=True)
    args = parser.parse_args()
    yaml_data = yaml.safe_load(
        pathlib.Path(args.charm_directory, "charmcraft.yaml").read_text()
    )
    bases = [index for index, _ in enumerate(yaml_data["bases"])]
    logging.info(f"Collected {bases=}")
    default_prefix = (
        f'packed-charm-cache-{args.cache}-{args.charm_directory.replace("/", "-")}'
    )
    logging.info(f"{default_prefix=}")
    with open(os.environ["GITHUB_OUTPUT"], "a") as file:
        file.write(f"bases={json.dumps(bases)}\ndefault_prefix={default_prefix}")
