import random

from django.shortcuts import render, redirect, reverse
from django.conf import settings

from proxy.models import Proxy, models
from proxy.validators import validate_and_create_proxys


def upload_file(request):
    """Позволяет администратору загружать .csv файл
        с параметрами для проксирования изображений"""
    # Предлагает авторизоваться в качестве админа
    if not request.user.is_authenticated:
        return redirect(f"{reverse('admin:login')}?next={request.path}")

    # Страница доступна только администраторам
    if not request.user.is_superuser:
        return redirect(reverse("home"))

    if request.method == 'POST':
        errors = validate_and_create_proxys(request)

        if errors:
            return render(
                request, 'proxy/upload.html', {'errors': errors}
            )
        success: str = "Файл успешно загружен"
        return render(
            request, 'proxy/upload.html', {'success': success}
        )
    return render(request, 'proxy/upload.html')


def index(request):
    """Главная страница"""
    # Находим все изображения кроме тех, у которых исчерпан лимит
    proxy_qs: models.query.QuerySet[Proxy] = Proxy.objects.prefetch_related(
        "categories"
    ).exclude(amount=0)
    categories = request.GET.getlist("category[]")

    # если в запросе есть параметр category
    if categories:  # Выбираем те, которые соответствуют категориям
        proxy_qs = proxy_qs.filter(categories__name__in=categories)
    proxy_qs = proxy_qs[:settings.VARIABILITY]
    proxy: Proxy = random.choice(proxy_qs) if proxy_qs else None

    if proxy:
        proxy.amount -= 1  # Снимаем лимит просмотров.
        proxy.save()
        categories = proxy.categories.values_list("name", flat=True)
    return render(request, 'proxy/index.html', {
        "categories": categories, "image": proxy.url if proxy else None
    })
