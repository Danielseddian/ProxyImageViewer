import csv
from io import StringIO

from django.core.validators import FileExtensionValidator, URLValidator
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile

from proxy.models import Proxy, Category, models


class IntValidator:
    def __init__(self, message=None):
        self.message = message

    def __call__(self, value):
        try:
            int(value)

        except (ValueError, TypeError):
            raise ValidationError(self.message, code="invalid")


def validate_and_create_proxys(
        request
) -> list[str] | ValidationError | list[csv.Error] | None:
    """Проверяет загруженный файл"""
    file: InMemoryUploadedFile = request.FILES.get('file')

    if not file:
        return ['Файл не выбран']

    # Проверка расширения файла
    try:
        FileExtensionValidator(['csv'])(file)

    except ValidationError as error:
        return error

    # Валидация данных
    try:
        proxy_qs: models.query.QuerySet[Proxy] = Proxy.objects.all()
        new_proxys: list[Proxy] = []
        categories: set[Category] = set()
        proxy_category = Proxy.categories.through
        proxy_categories: set[proxy_category] = set()

        for row, proxy in enumerate(
                csv.reader(StringIO(file.read().decode('utf-8')), delimiter=";")
        ):
            url: str = proxy[0]
            message: str = f"URL-адрес изображения в строке №{row} не валиден"
            URLValidator(message=message)(url)

            message: str = f"Количество просмотров в строке №{row} не валидно"
            IntValidator(message=message)(proxy[1])

            proxy_object: Proxy = proxy_qs.filter(url=url).first()

            if proxy_object:
                proxy_object.amount += int(proxy[1])

            else:
                new_proxys.append(Proxy(url=url, amount=int(proxy[1])))

            for category in proxy[2:]:
                categories.add(Category(category))
                proxy_categories.add((url, category))

        # Создание объектов и связей
        proxy_qs.bulk_update(proxy_qs, fields=['amount'])
        proxy_qs.bulk_create(new_proxys, ignore_conflicts=True)
        Category.objects.bulk_create(categories, ignore_conflicts=True)

        proxy_qs = Proxy.objects.all()
        category_qs = Category.objects.all()
        proxy_category.objects.bulk_create((proxy_category(
            proxy=proxy_qs.filter(url=m2m[0]).first(),
            category=category_qs.filter(name=m2m[1]).first()
        ) for m2m in proxy_categories), ignore_conflicts=True)
        return None

    except csv.Error as error:
        return [error]

    except ValidationError as error:
        return error
