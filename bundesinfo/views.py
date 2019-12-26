from django.views.generic import TemplateView, ListView
from bundesinfo.models import TeamStandings


class IndexPage(TemplateView):
    template_name = 'bundesinfo/index.html'


class Standings(ListView):
    model = TeamStandings
    template_name = 'bundesinfo/standings.html'

    def get_queryset(self):
        qs = TeamStandings.objects.all()
        return qs
