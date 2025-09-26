# from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.triggers.cron import CronTrigger
# from django_apscheduler.jobstores import DjangoJobStore
# from django.core.management.base import BaseCommand
# from django.conf import settings
# import logging
# from ticketapp.management.commands.check_sla import Command as CheckSlaCommand

# logger = logging.getLogger(__name__)

# def check_sla_job():
#     # Directly call the handle() method of your existing check_sla command
#     cmd = CheckSlaCommand()
#     cmd.handle()

# class Command(BaseCommand):
#     help = "Runs APScheduler to schedule periodic jobs."

#     def handle(self, *args, **options):
#         scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
#         scheduler.add_jobstore(DjangoJobStore(), "default")

#         # Schedule the SLA check job every 15 minutes
#         scheduler.add_job(
#             check_sla_job,
#             trigger=CronTrigger(minute="*/15"),
#             id="check_sla_job",
#             max_instances=1,
#             replace_existing=True,
#         )

#         logger.info("Starting APScheduler...")
#         try:
#             scheduler.start()
#         except KeyboardInterrupt:
#             logger.info("APScheduer stopped manually.")
