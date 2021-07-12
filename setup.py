from setuptools import setup

setup(
    name='GunicornLogsParser',
    version='0.0.1',
    description='Simple python app for parsing logs from gunicorn',
    url='https://github.com/iCurbix/GunicornLogsParser',
    author='Adam Korytowski',
    author_email='icurbix@protonmain.com',
    packages=['guniparse'],
    python_requires='>=3.8, <4',
    entry_points={
        'console_scripts': [
            'guniparse=guniparse.main:main',
        ],
    },
)
