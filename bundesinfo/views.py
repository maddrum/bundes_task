from django.views.generic import TemplateView, ListView
from bundesinfo.models import TeamStandings
import requests
from django.utils import timezone


class IndexPage(TemplateView):
    template_name = 'bundesinfo/index.html'


class Standings(ListView):
    model = TeamStandings
    template_name = 'bundesinfo/standings.html'

    def get_queryset(self):
        qs = TeamStandings.objects.all()
        return qs


class NextRound(TemplateView):
    template_name = 'bundesinfo/next_round.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get latest groupid/current matchday/
        current_group_order_id_url = 'https://www.openligadb.de/api/getcurrentgroup/bl1'
        group_order_request = requests.get(current_group_order_id_url).json()
        current_group_order_id = int(group_order_request['GroupOrderID'])
        # get next round matches
        url_address = 'https://www.openligadb.de/api/getmatchdata/bl1/2019/' + str(current_group_order_id + 1)
        result_json = requests.get(url_address).json()
        matches = []
        for item in result_json:
            format_str = r'%Y-%m-%dT%H:%M:%SZ'
            time = timezone.make_aware(timezone.datetime.strptime(item['MatchDateTimeUTC'], format_str))
            team1 = item['Team1']['ShortName']
            team2 = item['Team2']['ShortName']
            team1_logo = item['Team1']['TeamIconUrl']
            team2_logo = item['Team2']['TeamIconUrl']
            temp_dict = {
                'time': time,
                'team1': team1,
                'team2': team2,
                'team1_logo': team1_logo,
                'team2_logo': team2_logo,
            }
            matches.append(temp_dict)
        context['matches'] = matches
        return context
