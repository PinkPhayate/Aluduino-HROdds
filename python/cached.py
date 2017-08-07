import redis

r = redis.Redis(host='localhost', port=6379, db=0)
def set_race_odds_list(list):
    r.set('odds-list', list)
    r.expire('odds-list', 30)

def get_race_odds_list():
    list = r.get('odds-list')
    return list

def set_race_schedule(dict):
    r.set('race-schedule', dict)
    r.expire('race-schedule', 3*60*60)

def get_race_schedule():
    dict = r.get('schedule')
    return dict
