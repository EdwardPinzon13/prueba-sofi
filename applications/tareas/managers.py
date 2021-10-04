from datetime import datetime,timedelta

from django.db import  models
from django.db.models import  Q
from .models import *


class ActivityManager(models.Manager):

    def get_activities_finished_bloked(self):
        return self.filter(
            Q(stateActivity =2) | Q(stateActivity=4)
        )

    def get_activities_to_finish(self):
        activity = self.all()
        activities=[]
        for activity in activity:
            days=(activity.finishDate - datetime.now().date()) /timedelta(days=1)
            if days <= ((activity.estimatedTime).hour/24) :
                activities.append(activity)
        return activities

