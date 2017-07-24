from oddsman import oddsman
ow = oddsman.OddsWatcher()


def get_race_odds(mode= None):
    if mode == 'test':
        race_id = '201209030811'
        odds_list = ow.get_race_odds(race_id)
    else:
        odds_list = ow.get_nearest_odds()
    return odds_list

def retrieve_odds(odds_list, num):
    """
    @param num: integer
    """
    try:
        num = int(num)
    except:
        print('[ERROR] unexpected variable type. var must he integer')
        return None
    if num < len(odds_list):
        return odds_list[num]
    return None
