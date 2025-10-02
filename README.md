# Seminarios - Module: Research Data Management (RDM) - Project

Dataset from https://www.kaggle.com/datasets/nikdavis/steam-store-games

## How to Run

1. Download dataset from https://www.kaggle.com/datasets/nikdavis/steam-store-games -- You can choose any name to set it as, but we recommend to leave it as steam.csv under root/resources/
2. Create the new linked data dataset: 
    - from root/src/ 
    
            python main.py -c

    - If you wish to specify input and output paths, you can.
    
            python main.py -c --input "path\to\input" --output "path\to\output"
3. Run using linked data dataset:
    - from root/src/ 
    
            python main.py

## 1. Choose Dataset

We chose this dataset because it had pertinant information, was in a 2-star data format (csv) and lacked interoperability and linked data

## 2. Clean/Harmonize the Data and Link to External Data Sources

### Clean/Harmonize

- Removed column "English", as it was a boolean on if the game was in english or not, which wasn't pertinent information for our case and we felt it was unnecessary
- Dropped games with less than 1000000 (a million) owners. There were >20k games in our dataset and the process of linking data was too slow to allow for such a enormous dataset. We decided to filter by the most popular games using the column "owners", which revealed a range of owners.
- 

## Developers

Work done for Seminarios class in M.EIC @ FEUP by

- Nuno Jesus
- Tiago Cruz