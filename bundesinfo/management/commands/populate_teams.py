from django.core.management.base import BaseCommand
import requests
from bundesinfo.models import TeamName


class Command(BaseCommand):
    help = 'Populates teams info for 2019'

    def handle(self, *args, **options):
        teams_url = 'https://www.openligadb.de/api/getavailableteams/bl1/2019'
        get_teams = requests.get(teams_url).json()

        for item in get_teams:
            team, created = TeamName.objects.get_or_create(teamID=int(item['TeamId']))
            team.team_name = item['ShortName']
            team.team_logo = item['TeamIconUrl']
            team.save()
        print('Done populating teams info for year 2019!')
