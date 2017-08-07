from oddsman import oddsman
import oddsman_wrapper as wrapper
import cached as chd
import sys

ow = oddsman.OddsWatcher()

### TODAY MODE ###
# later_race_ids = ow.get_later_race_ids()
# print(later_race_ids)
# odds = ow.get_nearest_odds()
# print(odds)

# history mode
# race_id = '201702010412'
# odds_dict = ow.get_race_odds(race_id)
# print(odds_dict)

### TODAY MODE AND CAHED
args = sys.argv
mode = None
if 1 < len(args):
    mode = 'test' if args[1]=='test' else None

odds_list = chd.get_race_odds_list()
if odds_list is None:
    odds_list = wrapper.get_race_odds(mode)
    chd.set_race_odds_list(odds_list)
else:
    odds_list = odds_list.decode('utf-8')
print(odds_list)
