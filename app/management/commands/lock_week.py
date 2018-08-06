from django.core.management.base import BaseCommand
from app.models import Week

class Command(BaseCommand):
	help = 'Lock the games this week'

	def add_arguments(self, parser):
		parser.add_argument('week', nargs='+', type=int)

	def handle(self, *args, **options):

		week_num = options['week'][0]

		try:
			week = Week.objects.get(num=week_num)
		except Week.DoesNotExist:
			CommandError('That week could not be found')

		week.Lock()
		week.save()
