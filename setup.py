from setuptools import setup, find_packages

project_url = 'https://github.com/LudwigCRON/vpm'

requires = ['python_version>="3.5"']

setup(
    name='pyvpm',
    use_scm_version={
        "relative_to": __file__,
        "write_to": "vpm/version.py",
    },
    url=project_url,
    license='MIT license',
    author='Ludwig CRON',
    author_email='ludwig.cron@gmail.com',
    description='Verilog Package Manager',
    long_description=open("README.md").read(),
    zip_safe=False,
    classifiers=[],
    platforms='any',
    packages=["vpm"],
    include_package_data=True,
    install_requires=requires,
    setup_requires=[
        'setuptools_scm',
    ],
    entry_points={
        'console_scripts': [
            'vpm = vpm:cli_main',
        ],
    },
    keywords=['vpm', 'verilog', 'package'],
)
