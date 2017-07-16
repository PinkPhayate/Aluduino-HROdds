from oddsman import oddsman

ow = oddsman.OddsWatcher()

### TODAY MODE ###
later_race_ids = ow.get_later_race_ids()
print(later_race_ids)
odds = ow.get_nearest_odds()
print(odds)

# history mode
# race_id = '201702010412'
# odds_dict = ow.get_race_odds(race_id)
# print(odds_dict)
