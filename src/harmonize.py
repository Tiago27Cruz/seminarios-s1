import pandas as pd

def removeGames(df: pd.DataFrame) -> pd.DataFrame:
    def filter_by_owners(row):
        owners_range = row['owners'].split('-')
        if len(owners_range) > 0:
            min_owners = int(owners_range[0])
            return min_owners >= 1000000
        else:
            raise ValueError("Invalid owners range")

    df = df.drop(columns=['english'])
    df = df[df.apply(filter_by_owners, axis=1)]
    return df