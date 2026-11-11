import argparse
from .config import RAW, PROCESSED, STATCAN_TABLES
from .data_pipeline import download_statcan_table, build_analysis_extract

def main():
    parser = argparse.ArgumentParser(description="SE Bridge Statistics Canada pipeline")
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--build", action="store_true")
    args = parser.parse_args()
    if args.download:
        for key in STATCAN_TABLES:
            print("Downloaded:", download_statcan_table(key))
    if args.build:
        PROCESSED.mkdir(parents=True, exist_ok=True)
        for key, spec in STATCAN_TABLES.items():
            source = RAW / f"{spec['table_id']}.csv"
            if not source.exists():
                raise FileNotFoundError(f"{source} missing; run --download first")
            target = PROCESSED / f"{key}.csv"
            build_analysis_extract(source, target, key)
            print("Built:", target)
    if not args.download and not args.build:
        parser.print_help()

if __name__ == "__main__":
    main()
