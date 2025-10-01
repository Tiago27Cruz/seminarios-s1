import pandas as pd

STEAMDB = "../resources/steam.csv"

def readCsvData(filePath: str) -> pd.DataFrame:
    df = pd.read_csv(filePath)
    return df

def main():
    data = readCsvData(STEAMDB)
    print(data.head())

if __name__ == "__main__":
    main()