from optparse import make_option
from django.core.management.base import BaseCommand
from boto.mturk.question import (AnswerSpecification, Overview, Question,
        QuestionContent, QuestionForm, FreeTextAnswer, FormattedContent)
from cogpheno.apps.turk.utils import get_connection, get_worker_url


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '--account-balance',
            action='store_true',
            dest='account_balance',
            default=False,
            help='Print account balance '),
        make_option(
            '--sample-hit',
            action='store_true',
            dest='sample_hit',
            default=False,
            help=('Create sample "favorite color" hit')),
    )

    def check_account_balance(self):
        print self.mtc.get_account_balance()

    def handle(self, *args, **options):
        self.mtc = get_connection()

        if options['account_balance']:
            self.check_account_balance()

        if options['sample_hit']:
            #TODO: Function to create hit
