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