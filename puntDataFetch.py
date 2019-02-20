import requests
import json

if __name__ == '__main__':
    plays = []  # an empty list we'll fill with punts.

    for y in range(2005, 2019):
        for w in range(1, 16):
            # Fetch the plays for this week and year

            url = "https://api.collegefootballdata.com/plays?seasonType=regular&year={}&week={}".format(y, w)
            foo = json.loads(requests.get(url).text)

            # The play-by-play, unfortunately, does not include the home and away teams. However, the "yard_line"
            # element is indexed to the home team's goal line. So we need to figure out which team is home and which
            # is away.

            url = "https://api.collegefootballdata.com/games?year={}&week={}".format(y, w)
            games = json.loads(requests.get(url).text)

            # Scan through the plays, find all of the punt, stuff them in a new list.

            for x in foo:
                if 'Punt' in x['play_type']:
                    # The play record doesn't include the week and year, so add those.

                    tmp = dict({'year': y, 'week': w}, **x)

                    # Throw away fields we don't want right now.

                    for key in ['id', 'offense_conference', 'defense_conference', 'drive_id', 'play_text']:
                        del tmp[key]

                    # Figure out which game this is and add fields for the home and away team. We need these to properly
                    # use the field position for calculations later.

                    for g in games:
                        if set([tmp['offense'], tmp['defense']]) == set([g['home_team'], g['away_team']]):
                            tmp['home_team'], tmp['away_team'] = g['home_team'], g['away_team']
                            # ESPN play-by-play indexes the yard_line field to the home team's goal line.
                            # Let's change it so that it's indexed from the offense's goal line.
                            if tmp['offense'] == tmp['away_team']:
                                tmp['yard_line'] = 100 - tmp['yard_line']

                            break
                    plays.append(tmp)

    # Now dump the cleaned plays into a file.

    with open('punts.json', 'w+') as file:
        json.dump(plays, file, indent=4, sort_keys=True)
