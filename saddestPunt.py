import json


def surrender_index(punt: dict) -> float:
    # Some helper functions to tidy up the calculations.
    def field_position(pos: int) -> float:
        if pos <= 40:
            return 1.0
        elif 40 < pos <= 50:
            return 1.1 ** (pos - 40)
        else:
            return 2.59 * 1.2 ** (pos - 50)

    def first_down_distance(dist: int) -> float:
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

    def score_of_game(diff: int) -> float:
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

    d = punt['offense_score'] - punt['defense_score']    # score differential

    res = field_position(punt['yard_line']) * first_down_distance(punt['distance']) * score_of_game(d)

    if punt['period'] > 2 and d < 0:
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


if __name__ == '__main__':
    with open('punts.json', 'r') as file:
        punts = json.load(file)

    for p in punts:
        p['surrender_index'] = surrender_index(p)

    punts.sort(key=lambda x: x['surrender_index'], reverse=True)

    for p in punts[0:10]:
        print(p)

    with open('amended_punts.json', 'w+') as file:
        json.dump(punts, file, sort_keys=True, indent=4)
