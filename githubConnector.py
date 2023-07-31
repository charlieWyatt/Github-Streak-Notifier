import json
import datetime
from dateutil.relativedelta import relativedelta
from api_keys import GITHUB_API_KEY
import requests

def get_contributions(start_date, end_date):
    '''Returns the contributions of a github user in a given time period.'''
    url = 'https://api.github.com/graphql'
    json_input = { 'query' : '{ viewer { contributionsCollection( from: "'+start_date+'" to: "'+end_date+'") { contributionCalendar { totalContributions weeks { contributionDays { weekday date contributionCount color } } months { name year firstDay totalWeeks } }}} }' }
    api_token = GITHUB_API_KEY
    headers = {'Authorization': 'token %s' % api_token}

    r = requests.post(url=url, json=json_input, headers=headers)
    return r.json()

def get_streak(start_date = (datetime.datetime.now() - relativedelta(years=1)).isoformat(), end_date = (datetime.datetime.now() - relativedelta(days=1)).isoformat()):
    '''Returns the current streak of days with contributions from a github user. Only includes up to yesterday, because it is still possible for a user to continue the streak if they contribute today'''
    returned_json = get_contributions(start_date, end_date) # gets the past year of data

    weeks = returned_json['data']['viewer']['contributionsCollection']['contributionCalendar']['weeks']

    # sort weeks by date
    weeks.sort(key=lambda x: datetime.datetime.strptime(x['contributionDays'][0]['date'], '%Y-%m-%d'), reverse=True)

    # keeping taking the most recent days until there is not a contribution
    streak = 0
    for week in weeks:
        week['contributionDays'].sort(key=lambda x: datetime.datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True)
        for day in week['contributionDays']:
            if day['contributionCount'] > 0:
                streak += 1
            else:
                return streak
    return '365+' # only grabbing the past year worth of data
            
def has_contributed_today():
    returned_json = get_contributions(datetime.datetime.now().isoformat(), datetime.datetime.now().isoformat()) # gets just todays data
    return returned_json['data']['viewer']['contributionsCollection']['contributionCalendar']['totalContributions'] > 0