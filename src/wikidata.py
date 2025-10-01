import pywikibot as pw
from pywikibot import pagegenerators
import pandas as pd

def getGameWDEntry(df: pd.DataFrame) -> pd.DataFrame:
    site = pw.Site("wikidata", "wikidata")
    repo = site.data_repository()

    def fetch_wikidata_id(appid: int) -> str | None:
        try:
            game_row = df[df['appid'] == appid].iloc[0]
            search_term = game_row['name'] + " video game"
            search_results = pagegenerators.SearchPageGenerator(search_term, total=1, namespaces=[0], site=site)

            for result in search_results:
                item = pw.ItemPage(repo, result.title())
                item_dict = item.get()
                if 'P31' in item_dict['claims']: # (instance of) property
                    for claim in item_dict['claims']['P31']:
                        if claim.getTarget().getID() in ['Q7889']: # Q7889: video game
                            print(f"Found Wikidata ID for game {game_row['name'] }: {item.title()}")
                            return item.title().replace("Q", "")
            return None
        except Exception as e:
            print(f"Error fetching Wikidata ID for appid {appid}: {e}")
            return None

    def fetch_wikidata_dev_id(dev_name: str) -> str | None:
        try:
            dev_name = dev_name + " dev"
            search_results = pagegenerators.SearchPageGenerator(dev_name, total=1, namespaces=[0], site=site)

            for result in search_results:
                item = pw.ItemPage(repo, result.title())
                item_dict = item.get()
                if 'P452' in item_dict['claims']: # (industry) property
                    for claim in item_dict['claims']['P452']:
                        if claim.getTarget().getID() in ['Q941594']: # Q941594: video game industry
                            print(f"Found Wikidata ID for developer {dev_name }: {item.title()}")
                            return item.title().replace("Q", "")
            return None
        except Exception as e:
            print(f"Error fetching Wikidata ID for developer {dev_name}: {e}")
            return None

    df['wikidata_id'] = df['appid'].apply(fetch_wikidata_id)
    return df
