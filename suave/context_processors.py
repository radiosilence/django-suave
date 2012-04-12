from .models import Section


def nav(request):
    return dict(
        nav_sections=Section.objects.live()
    )
