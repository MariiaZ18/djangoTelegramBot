from django.db import models

class University(models.Model):
    name = models.CharField(max_length=100,verbose_name="Назва університету")

    class Meta:
        verbose_name = "Університет"
        verbose_name_plural="Університети"
    def __str__(self):
        return self.name

class Katedra(models.Model):
    name = models.CharField(max_length=100,verbose_name="Кафедра")
    university = models.ForeignKey(
        University,
        on_delete=models.DO_NOTHING,
    )

    class Meta:
        verbose_name="Кафедра",
        verbose_name_plural="Кафедри"

    def __str__(self):
        return self.name

class Subject(models.Model):
    name=models.CharField(max_length=100, verbose_name="Предмет")
    descr=models.TextField(verbose_name="Додаткова інформація", null=True)
    katedra = models.ForeignKey(Katedra, on_delete=models.PROTECT)
    upload = models.FileField(null=True)
    class Meta:
        verbose_name="Предмет",
        verbose_name_plural="Предмети"

    def __str__(self):
        return self.name
