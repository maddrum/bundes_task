from django.db import models
from django.core import validators


class TeamName(models.Model):
    """Holds information about teams"""

    teamID = models.IntegerField(validators=[
        validators.MinValueValidator(1),
    ])
    team_name = models.CharField(max_length=255)
    team_logo = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.team_name)


class TeamStandings(models.Model):
    """Holds information about team standings"""

    class Meta:
        ordering = ('-points', '-wins')

    team = models.OneToOneField(TeamName, on_delete=models.CASCADE)
    points = models.IntegerField(validators=[
        validators.MinValueValidator(0),
    ], null=True)
    wins = models.IntegerField(validators=[
        validators.MinValueValidator(0),
        validators.MaxValueValidator(34),
    ], null=True)
    loses = models.IntegerField(validators=[
        validators.MinValueValidator(0),
        validators.MaxValueValidator(34),
    ], null=True)
    draws = models.IntegerField(validators=[
        validators.MinValueValidator(0),
        validators.MaxValueValidator(34),
    ], null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.team) + '-points: ' + str(self.points) + ' wins: ' + str(self.wins) + ' draws: ' + str(
            self.draws) + ' loses: ' + str(self.loses)
