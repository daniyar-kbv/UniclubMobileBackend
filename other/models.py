from django.db import models


class TimestampModel(models.Model):
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class GradeTypeGroup(TimestampModel):
    name = models.CharField('Название', max_length=100)

    class Meta:
        verbose_name = 'Группа занятий'
        verbose_name_plural = 'Группы занятий'

    def __str__(self):
        return f'({self.id}) {self.name}'


class GradeType(TimestampModel):
    class Meta:
        verbose_name = "Вид занятия"
        verbose_name_plural = "Виды занятий"

    name = models.CharField("Название", max_length=120)
    group = models.ForeignKey(
        GradeTypeGroup,
        verbose_name='Группа занятий',
        related_name='types',
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return f'({self.id}) {self.name}'


class AdministrativeDivision(TimestampModel):
    class Meta:
        verbose_name = 'Административное деление'
        verbose_name_plural = 'Административные деления'

    name = models.CharField("Название", max_length=256)

    def __str__(self):
        return f'({self.id}) {self.name}'


class AgeGroup(TimestampModel):
    from_age = models.PositiveSmallIntegerField('От')
    to_age = models.PositiveSmallIntegerField('До')

    class Meta:
        verbose_name = 'Возрастная группа'
        verbose_name_plural = 'Возрастные группы'
        ordering = ['from_age']

    def __str__(self):
        return f'({self.id}) {self.from_age} - {self.to_age}'


class AttendanceType(TimestampModel):
    name = models.CharField('Название', max_length=100)

    class Meta:
        verbose_name = 'Вид посещения'
        verbose_name_plural = 'Виды посещения'

    def __str__(self):
        return f'({self.id}) {self.name}'
