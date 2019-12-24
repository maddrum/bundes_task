from django.core.management.base import BaseCommand
import requests
from bundesinfo.models import TeamName, TeamStandings


class Command(BaseCommand):
    help = 'Create/Update current standings'

    def handle(self, *args, **options):
        # get latest groupid/current matchday/
        current_group_order_id_url = 'https://www.openligadb.de/api/getcurrentgroup/bl1'
        group_order_request = requests.get(current_group_order_id_url).json()
        current_group_order_id = int(group_order_request['GroupOrderID'])

        # initialize standings dictionary
        all_teams = TeamName.objects.all()
        standings = {}
        for item in all_teams:
            standings[item.teamID] = {}
            standings[item.teamID]['points'] = 0
            standings[item.teamID]['wins'] = 0
            standings[item.teamID]['loses'] = 0
            standings[item.teamID]['draws'] = 0

        # make requests to API for all matchdays until current date
        request_match_info = []
        for item in range(1, current_group_order_id + 1):
            url_address = 'https://www.openligadb.de/api/getmatchdata/bl1/2019/' + str(item)
            result_json = requests.get(url_address).json()
            request_match_info.append(result_json)

        # generate standings
        for matchday in request_match_info:
            for single_match in matchday:
                # check if match is over
                if len(single_match['MatchResults']) == 0:
                    print(f'Not finished yet! Update later, after the current round is over!')
                    return

                id_team1 = int(single_match['Team1']['TeamId'])
                id_team2 = int(single_match['Team2']['TeamId'])
                match_result = single_match['MatchResults'][0]
                score1 = int(match_result['PointsTeam1'])
                score2 = int(match_result['PointsTeam2'])

                # assign points
                if score1 > score2:
                    standings[id_team1]['points'] += 3
                    standings[id_team1]['wins'] += 1
                    standings[id_team2]['loses'] += 1
                elif score2 > score1:
                    standings[id_team2]['points'] += 3
                    standings[id_team2]['wins'] += 1
                    standings[id_team1]['loses'] += 1
                else:
                    standings[id_team1]['points'] += 1
                    standings[id_team1]['draws'] += 1
                    standings[id_team2]['points'] += 1
                    standings[id_team2]['draws'] += 1

        # write standings to database
        for obj in all_teams:
            standings_obj, created = TeamStandings.objects.get_or_create(team=obj)
            standings_obj.points = standings[obj.teamID]['points']
            standings_obj.wins = standings[obj.teamID]['wins']
            standings_obj.loses = standings[obj.teamID]['loses']
            standings_obj.draws = standings[obj.teamID]['draws']
            standings_obj.save()
        print(f'standings updated after round: {current_group_order_id}')
