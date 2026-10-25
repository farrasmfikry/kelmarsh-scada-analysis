"""Print the first rows of a Kelmarsh SCADA CSV file."""

import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.data_loader import load_scada_data


DEFAULT_CSV = (
    PROJECT_ROOT
    / "data"
    / "Turbine_Data_Kelmarsh_1_2020-01-01_-_2021-01-01.csv"
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Print the first rows of a Kelmarsh SCADA CSV file."
    )
    parser.add_argument(
        "csv_file",
        nargs="?",
        type=Path,
        default=DEFAULT_CSV,
        help=f"CSV file to read (default: {DEFAULT_CSV})",
    )
    parser.add_argument(
        "-n",
        "--rows",
        type=int,
        default=5,
        help="Number of rows to print (default: 5).",
    )
    args = parser.parse_args()

    if args.rows < 0:
        parser.error("--rows must be zero or greater")

    data = load_scada_data(args.csv_file)
    print(data.head(args.rows).to_string())


if __name__ == "__main__":
    main()
