import pandas as pd
import numpy as np
from scripts.extract_data import extract_data


def rank_by_scores(df: pd.DataFrame) -> pd.DataFrame:
    def calculate_scores(pok1):
        scores = []
        for _, pok2 in df.iterrows():
            score = (pok1['ATK'] - pok2['DEF']) * 0.8 + (pok1['SP_ATK'] - pok2['SP_DEF']) * 0.2
            scores.append(score)
        return sum(scores), max(scores), np.mean(scores)

    results = df.apply(calculate_scores, axis=1, result_type='expand')
    df['Total Score'] = results[0]
    df['Max Score'] = results[1]
    df['Mean Score'] = results[2]
    df_sorted = df.sort_values(by='Total Score', ascending=False)
    df_sorted['Rank'] = df_sorted['Total Score'].rank(ascending=False, method='dense').astype(int)
    df_sorted = df_sorted.sort_values('Rank')
    cols = ['Rank', 'Total Score', 'Max Score', 'Mean Score'] + [col for col in df_sorted.columns if col not in ['Rank', 'Total Score', 'Max Score', 'Mean Score']]
    df_sorted = df_sorted[cols]
    return df_sorted


URL = "https://gist.githubusercontent.com/simsketch/1a029a8d7fca1e4c142cbfd043a68f19/raw/bd584ee6c307cc9fab5ba38916e98a85de9c2ba7/pokemon.csv"
pokemon = extract_data(URL)
ranked_df = rank_by_scores(pokemon)

ranked_df.to_csv("/Users/georgelepsaya/PycharmProjects/pokemon/data/ranked_by_scores.csv")
