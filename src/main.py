import pandas as pd
import wikidata as wd

STEAMDB = "../resources/steam.csv"
STEAMLINKED = "../resources/steam_wikidata.csv"

def readCsvData(filePath: str) -> pd.DataFrame:
    df = pd.read_csv(filePath)
    return df

def removeGames(df: pd.DataFrame):
    def filter_by_owners(row):
        owners_range = row['owners'].split('-')
        if len(owners_range) > 0:
            min_owners = int(owners_range[0])
            return min_owners >= 1000000
        else:
            raise ValueError("Invalid owners range")

    df = df[df.apply(filter_by_owners, axis=1)]
    return df

def saveCsvData(df: pd.DataFrame, filePath: str):
    df.to_csv(filePath, index=False)
    print(f"Data saved to {filePath}")

def main():
    df = readCsvData(STEAMDB)
    df = removeGames(df)
    df = wd.getGameWDEntry(df)
    df.head()
    saveCsvData(df, "../resources/steam_wikidata.csv")

if __name__ == "__main__":
    main()