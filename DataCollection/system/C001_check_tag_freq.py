import pandas as pd
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent
def json_parse(x):
    try:
        return json.loads(x)
    except:
        return None

def run():
    df = pd.read_csv(f'{HERE}/var/local.csv')
    tag_freq = {}
    for tags in df['TAGS'].apply(json_parse):
        if tags is None:
            continue
        for tag in tags:
            if tag_freq.get(tag) is None:
                tag_freq[tag] = 0
            tag_freq[tag] += 1

    dfR = pd.DataFrame([{'TAG':tag, 'FREQ':freq} for tag, freq in tag_freq.items()])
    dfR = dfR.sort_values(by=['FREQ'])
    dfR.to_csv(f'{HERE}/var/tag_freq.csv', index=None)

if __name__ == '__main__':
    run()
