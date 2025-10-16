# Seminarios - Module: Research Data Management (RDM) - Project

Dataset from https://www.kaggle.com/datasets/nikdavis/steam-store-games

## 0. How to Run

1. Download dataset from https://www.kaggle.com/datasets/nikdavis/steam-store-games 
    - You can choose any name to set it as, but we recommend to leave it as steam.csv under root/resources/
2. Create the new linked data dataset: 
    - from root/src/ 
    
            python main.py -c

    - If you wish to specify input and output paths, you can.
    
            python main.py -c --input "path\to\input" --output "path\to\output"
3. Run using linked data dataset:
    - from root/src/ 
        python main.py

4. To convert to jsonld use
    - from root/src/
        python convert.py

## Developers

Work done for Seminarios class in M.EIC @ FEUP by

- Nuno Jesus
- Tiago Cruz