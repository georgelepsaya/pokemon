import pandas as pd


def rank_by_strength(df: pd.DataFrame, type_chart: dict) -> pd.DataFrame:
    def calculate_strength(pok1):
        strength = 0
        for _, pok2 in df.iterrows():
            type1_pok1 = pok1['TYPE1'].lower()
            type1_pok2 = pok2['TYPE1'].lower()
            type2_pok1 = None if pd.isna(pok1['TYPE2']) else pok1['TYPE2'].lower()
            type2_pok2 = None if pd.isna(pok2['TYPE2']) else pok2['TYPE2'].lower()

            mult11 = type_chart[type1_pok1][type1_pok2]
            mult12 = 1 if type2_pok2 is None else type_chart[type1_pok1][type2_pok2]
            tm1 = mult11 * mult12

            if type2_pok1:
                mult21 = type_chart[type2_pok1][type1_pok2]
                mult22 = 1 if type2_pok2 is None else type_chart[type2_pok1][type2_pok2]
                tm2 = mult21 * mult22
                strength += max(tm1, tm2)
            else:
                strength += tm1

        return strength

    df['strength'] = df.apply(calculate_strength, axis=1)
    df_sorted = df.sort_values(by='strength', ascending=False)

    return df_sorted
