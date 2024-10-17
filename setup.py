from setuptools import setup

setup(
    name="finguard",
    version="1.0.0",
    description="App to monitoring my finances",
    author="Gustavo Gomes",
    author_email="gustavo.gonosi@gmail.com",
    install_requires=[
        "django>=5.1.1"
        "psycopg2>=2.9.9"
        "python-dateutil>=2.9.0"
    ]
)