from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class Status(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название статуса")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

class Type(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название типа")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"

class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название категории")
    type = models.ForeignKey(Type, on_delete=models.CASCADE, verbose_name="Тип")

    def __str__(self):
        return f"{self.title} ({self.type.title})"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class SubCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название подкатегории")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")

    def __str__(self):
        return f"{self.title} ({self.category.title})"

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"

class CashflowRecord(models.Model):
    date = models.DateField(default=timezone.now, verbose_name="Дата")
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name="Статус")
    type = models.ForeignKey(Type, on_delete=models.CASCADE, verbose_name="Тип")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, verbose_name="Подкатегория")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
    comment = models.TextField(verbose_name="Комментарий", blank=True)

    def clean(self):
        errors = {}

        if hasattr(self, 'sub_category') and self.sub_category and self.category:
            if self.sub_category.category != self.category:
                errors['sub_category'] = "Подкатегория должна относиться к выбранной категории."

        if hasattr(self, 'category') and self.category and self.type:
            if self.category.type != self.type:
                errors['category'] = "Категория должна относиться к выбранному типу."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.amount if self.amount else 'Без суммы'} ({self.date if self.date else 'Без даты'}) - {self.category if self.category else 'Без категории'} / {self.sub_category if self.sub_category else 'Без подкатегории'}"

    class Meta:
        verbose_name = "Запись о движении средств"
        verbose_name_plural = "Записи о движении средств"