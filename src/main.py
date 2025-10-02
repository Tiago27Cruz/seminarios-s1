import pandas as pd
import wikidata as wd
import harmonize as hm
import argparse

STEAMDB = "../resources/steam.csv"
STEAMLINKED = "../resources/steam_wikidata.csv"

def readCsvData(filePath: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(filePath)
        return df
    except Exception as e:
        print(f"Error reading {filePath}: {e}")
        return pd.DataFrame()

def saveCsvData(df: pd.DataFrame, filePath: str) -> None:
    df.to_csv(filePath, index=False)
    print(f"Data saved to {filePath}")

def createParser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Process Steam data.")
    parser.add_argument('-c', '--create', action='store_true', help='Create a new CSV file with linked data')
    parser.add_argument('--input', type=str, default=STEAMDB, help='Input CSV file path')
    parser.add_argument('--output', type=str, default=STEAMLINKED, help='Output CSV file path (with linked data and data processing)')
    return parser

def main():
    parser = createParser()
    args = parser.parse_args()
    
    if args.create:
        print("Creating new CSV with linked data @ " + args.output)
        df = readCsvData(args.input)
        df = hm.removeGames(df)
        df = hm.aggregateRatings(df)
        df = wd.getGameWDEntry(df)
        saveCsvData(df, args.output)
    else:
        if not args.input or args.input == STEAMDB:
            args.input = STEAMLINKED
        print("Reading existing CSV with linked data @ " + args.input)
        df = readCsvData(args.input)
        saveCsvData(df, args.output)

    print(df.head())
    

if __name__ == "__main__":
    main()