import pandas as pd
import requests
import json


def fetchPunts(year):
    punts = []  # an empty list we'll fill with punts.

    for w in range(1, 16):
        # Fetch the plays for this week and year
        # Scan through the plays, find all of the punt, stuff them in a new list.

        url = "https://api.collegefootballdata.com/plays?year={}&week={}".format(year, w)

        for x in json.loads(requests.get(url).text):
            if 'Punt' in x['play_type']:
                # ESPN pbp indexes field position to the home team goal line
                x['yard_line'] = x['yard_line'] if x['offense'] == x['home'] else 100 - x['yard_line']

                punts.append(
                    {y: x[y] for y in
                     ['down', 'offense', 'defense', 'clock', 'offense_score', 'defense_score', 'yard_line', 'home', 'distance',
                      'period']})

    return punts


def surrender_index(punt: dict) -> float:
    # Some helper functions to tidy up the calculations.
    def field_position(p: dict) -> float:
        pos = p['yard_line']
        if pos <= 40:
            return 1.0
        elif 40 < pos <= 50:
            return 1.1 ** (pos - 40)
        else:
            return 2.59 * 1.2 ** (pos - 50)

    def first_down_distance(p: dict) -> float:
        dist = p['distance']

        if dist <= 1:
            return 1.0
        elif 2 <= dist <= 3:
            return 0.8
        elif 4 <= dist <= 6:
            return 0.6
        elif 7 <= dist <= 9:
            return 0.4
        else:
            return 0.2

    def score_of_game(p: dict) -> float:
        diff = p['offense_score'] - p['defense_score']  # score differential

        if diff > 0:
            return 1
        elif diff == 0:
            return 2
        elif -8 <= diff < 0:
            return 4
        else:
            return 3

    def clock(time: int) -> float:
        return ((time * 0.001) ** 3) + 1

    res = field_position(punt) * first_down_distance(punt) * score_of_game(punt)

    if punt['period'] > 2 and punt['offense_score'] - punt['defense_score'] < 0:
        try:
            m = punt['clock']['minutes']
        except KeyError:
            m = 0
        try:
            s = punt['clock']['seconds']
        except KeyError:
            s = 0
        return res * clock(m * 60 + s + 900 * (punt['period'] - 3))
    else:
        return res


def main(year):
    punts = fetchPunts(year)

    for p in punts:
        p['surrender_index'] = surrender_index(p)

    punts.sort(key=lambda x: x['surrender_index'], reverse=True)
    pd.DataFrame.from_dict(punts).to_csv('Saddest Punts of {}.csv'.format(year))


if __name__ == '__main__':
    main(2019)
