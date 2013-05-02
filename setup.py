from setuptools import setup

setup(
    name = 'radio_django',
    version = '0.0alpha',
    author = 'Wessie',
    author_email = 'radiodjango@wessie.info',
    description = ("The website framework used by R/a/dio"),
    license = "BSD",
    install_requires = [
        "Django>=1.5",
        "psycopg2",
        "south",
        "django-audit-log",
        "django-celery",
        "celery-haystack",
        "mutagen",
        "django-tastypie",
                        ],
)
