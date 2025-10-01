import pywikibot as pw
from pywikibot import pagegenerators
import pandas as pd

def getGameWDEntry(df: pd.DataFrame) -> pd.DataFrame:
    site = pw.Site("wikidata", "wikidata")
    repo = site.data_repository()

    def fetch_wikidata_data(appid: int) -> dict:
        try:
            game_row = df[df['appid'] == appid].iloc[0]
            search_term = game_row['name'] + " video game"
            search_results = pagegenerators.SearchPageGenerator(search_term, total=1, namespaces=[0], site=site)

            result_data = {
                'wd_game_id': None,
                'wd_developers': None,
                'wd_publishers': None,
                'wd_platforms': None,
                'wd_genres': None,
            }

            for result in search_results:
                item = pw.ItemPage(repo, result.title())
                item_dict = item.get()

                # Check for "instance of" property (P31)
                if 'P31' in item_dict['claims']:
                    for claim in item_dict['claims']['P31']:
                        if claim.getTarget().getID() == 'Q7889':  # Q7889: video game
                            result_data['wd_game_id'] = item.title()

                # Check for "developer" property (P178)
                if 'P178' in item_dict['claims']:
                    result_data['wd_developers'] = [
                        claim.getTarget().getID() for claim in item_dict['claims']['P178']
                    ]
                
                # Check for "publisher" property (P123)
                if 'P123' in item_dict['claims']:
                    result_data['wd_publishers'] = [
                        claim.getTarget().getID() for claim in item_dict['claims']['P123']
                    ]

                # Check for "platform" property (P400)
                if 'P400' in item_dict['claims']:
                    result_data['wd_platforms'] = [
                        claim.getTarget().getID() for claim in item_dict['claims']['P400']
                    ]

                # Check for "genre" property (P136)
                if 'P136' in item_dict['claims']:
                    result_data['wd_genres'] = [
                        claim.getTarget().getID() for claim in item_dict['claims']['P136']
                    ]

            return result_data
        except Exception as e:
            print(f"Error fetching Wikidata data for appid {appid}: {e}")
            return {
                'wd_game_id': None,
                'wd_instance_of': None,
                'wd_developer': None
            }

    wikidata_columns = df['appid'].apply(fetch_wikidata_data).apply(pd.Series)
    df = pd.concat([df, wikidata_columns], axis=1)
    return df
