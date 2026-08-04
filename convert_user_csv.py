#!/usr/bin/env python3

"""
Convert user CSV data into the target CSV format.

Autor: Christian Wichmann <wichmann@bbs-brinkstrasse.de>
Created with Github Copilot (GPT-5.4-Codex).
"""

from __future__ import annotations

import argparse
import csv
import secrets
import string
from pathlib import Path

OUTPUT_HEADER = ["lastname", "firstname", "cohort1", "username", "email", "password", "profile_field_source", "auth"]
PASSWORD_ALPHABET = string.ascii_letters + string.digits


def generate_password(length: int = 24) -> str:
    return "".join(secrets.choice(PASSWORD_ALPHABET) for _ in range(length))


def convert_csv(input_path: Path, output_path: Path, domain: str, password_length: int) -> None:
    with input_path.open("r", encoding="utf-8-sig", newline="") as src_file, output_path.open(
        "w", encoding="utf-8", newline=""
    ) as dst_file:
        reader = csv.DictReader(src_file)
        writer = csv.DictWriter(dst_file, fieldnames=OUTPUT_HEADER, delimiter=";")
        writer.writeheader()

        for row in reader:
            username = (row.get("Account") or "").strip()
            password = (row.get("Passwort") or "").strip() or generate_password(password_length)
            writer.writerow(
                {
                    "lastname": (row.get("Nachname") or "").strip(),
                    "firstname": (row.get("Vorname") or "").strip(),
                    "cohort1": (row.get("Klasse/Information") or "").strip(),
                    "username": username,
                    "email": f"{username}@{domain}" if username else "",
                    "password": password,
                    # mark all students as imported from iServ!
                    "profile_field_source": "iServ",
                    # mark all accounts as using OAuth2 authentication
                    "auth": "oauth2"
                }
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert a user CSV file from German source format to target format."
    )
    parser.add_argument("input_csv", type=Path, help="Path to the input CSV file")
    parser.add_argument(
        "--domain",
        default="bbs-brinkstrasse.net",
        help="Domain part for the generated email address (default: bbs-brinkstrasse.net)",
    )
    parser.add_argument(
        "--password-length",
        type=int,
        default=24,
        help="Length of generated passwords for rows without password (default: 24)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = args.input_csv
    output_path = input_path.with_name(f"{input_path.stem}.converted{input_path.suffix}")
    convert_csv(input_path, output_path, args.domain, args.password_length)


if __name__ == "__main__":
    main()
