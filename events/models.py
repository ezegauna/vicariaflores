from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models


class Parroquia(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class Integrante(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    birth_date = models.DateField()
    cellphone = models.CharField(
        max_length=20, null=True, blank=True, validators=[RegexValidator(r"^\d{1,10}$")]
    )
    place = models.ForeignKey(Parroquia, on_delete=models.CASCADE)
    is_attending = models.BooleanField(verbose_name="Representante", default=False)

    class Meta:
        unique_together = ("name", "surname", "birth_date", "place")

    def __str__(self):
        return f"{self.name}, {self.surname} ({self.place.name})"

    """
    def save(self, *args, **kwargs):
        if self.is_attending and self.user:
            self.user.is_staff = True
            try:
                Group.objects.get(name="Attending").user_set.add(self.user)
            except Group.DoesNotExist:
                raise ValidationError("Group does not exist")
            self.user.save()
        return super(Integrates, self).save(*args, **kwargs)
    """


class Evento(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField()

    def __str__(self):
        return self.name


class Mesa(models.Model):
    name = models.CharField(max_length=100)
    event = models.ForeignKey(Evento, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("name", "event")

    def __str__(self):
        return f"{self.name} ({self.event.name})"


class Invitado(models.Model):
    integrate = models.ForeignKey(
        Integrante, verbose_name="Integrante", on_delete=models.CASCADE
    )
    table = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    is_present = models.BooleanField(verbose_name="Esta presente", default=False)

    def __str__(self):
        return f"{self.integrate} ({self.table.name}) [{self.is_present}]"

    def save(self, *args, **kwargs):
        if Invitado.objects.filter(
            integrate=self.integrate, table__event=self.table.event
        ).exists():
            raise ValidationError("Ya existe un Invitado con este integrante y evento.")
        else:
            super(Invitado, self).save(*args, **kwargs)
