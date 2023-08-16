from django.db import models


class Category(models.Model):
    """Модель категории"""
    name = models.SlugField(verbose_name="Название категории",
                            primary_key=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Proxy(models.Model):
    """Модель прокси"""
    url = models.URLField(verbose_name="URL-адрес изображения",
                          primary_key=True)
    amount = models.PositiveBigIntegerField(verbose_name="Количество просмотров",
                                            default=0)
    categories = models.ManyToManyField(Category,
                                        related_name="proxies",
                                        verbose_name="Категории")

    class Meta:
        verbose_name = "Прокси"
        verbose_name_plural = "Прокси"
        ordering = ["-amount"]

    def __str__(self):
        return (f"Изображение: {self.url} ({self.pk}) - "
                f"осталось {self.amount} просмотров")
