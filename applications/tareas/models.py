from django.db import models
from django.conf import settings
from .managers import ActivityManager

# Create your models here.
class State(models.Model):
    stateActivity  = models.CharField(max_length=50,verbose_name="Estado de Actividad")

    class Meta:
        verbose_name = ('State')
        verbose_name_plural = ("States")

    def __str__(self):
        return self.stateActivity

class Activity(models.Model):
    descriptionActivity  = models.CharField(max_length=250)
    stateActivity= models.ForeignKey(State, verbose_name=("Estado de Actividad"), on_delete=models.CASCADE,related_name='activityToState')
    taskOwner =  models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=("Responsable de la Tarea"), on_delete=models.CASCADE)
    observation = models.CharField(max_length=100, blank=True, verbose_name="Observación de Actividad")
    assignmentDate = models.DateField(("Fecha de Asignación"), auto_now=False, auto_now_add=False)
    estimatedTime = models.TimeField(("Tiempo Estimado para la Tarea"), auto_now=False, auto_now_add=False)
    finishDate = models.DateField(("Fecha de Finalización"), auto_now=False, auto_now_add=False)
    objects = ActivityManager()
    class Meta:
        verbose_name = ("Activity")
        verbose_name_plural = ("Activities")

    def __str__(self):
        return self.descriptionActivity + ' - ' + self.stateActivity.stateActivity + ' - ' +  self.taskOwner.username



