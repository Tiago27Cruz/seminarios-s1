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

def aggregateRatings(df: pd.DataFrame) -> pd.DataFrame:
    def compute_aggregated_rating(row):
        total_reviews = row['positive_ratings'] + row['negative_ratings']
        if total_reviews > 0:
            return (row['positive_ratings'] / total_reviews) * 100
        else:
            return 0.0

    df['rating_value'] = df.apply(compute_aggregated_rating, axis=1)
    df['rating_count'] = df['positive_ratings'] + df['negative_ratings']
    df = df.drop(columns=['positive_ratings', 'negative_ratings'])
    return df

def dropWithoutWikidata(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(subset=['wd_game_id', 'wd_developers', 'wd_publishers', 'wd_platforms', 'wd_genres'])
    return df

def addWikidataPrefix(row: pd.Series) -> pd.Series:
    if pd.notna(row['wd_game_id']):
        row['wd_game_id'] = 'https://www.wikidata.org/wiki/' + row['wd_game_id']
    if pd.notna(row['wd_developers']):
        row['wd_developers'] = ['https://www.wikidata.org/wiki/' + dev for dev in row['wd_developers']]
    if pd.notna(row['wd_publishers']):
        row['wd_publishers'] = ['https://www.wikidata.org/wiki/' + pub for pub in row['wd_publishers']]
    if pd.notna(row['wd_platforms']):
        row['wd_platforms'] = ['https://www.wikidata.org/wiki/' + plat for plat in row['wd_platforms']]
    if pd.notna(row['wd_genres']):
        row['wd_genres'] = ['https://www.wikidata.org/wiki/' + genre for genre in row['wd_genres']]
    return row

def joinWikidataColumns(df: pd.DataFrame) -> pd.DataFrame:
    #df = df.apply(addWikidataPrefix, axis=1)
    df = df.drop(columns=['name', 'developer', 'publisher', 'platforms', 'genres'])
    df = df.rename(columns={
        'wd_game_id': 'name',
        'wd_developers': 'developers',
        'wd_publishers': 'publishers',
        'wd_platforms': 'platforms',
        'wd_genres': 'genres'
    })
    return df