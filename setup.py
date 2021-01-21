# coding: utf-8

from io import open
from setuptools import setup, find_packages

version = '0.3.5'

requirements = [
    'setuptools',
    'six>=1.12.0',

    # sa-notify
    'wechat3',
    'requests',

    # sa-dns
    'pydnspod2',

    # sa-access
    'elasticsearch>=7.0.0',

    # sa-disk
    'humanize',
]

# see also https://setuptools.readthedocs.io/en/latest/setuptools.html#declaring-extras-optional-features-with-their-own-dependencies  # NOQA
extras_require = {
    # sa-script
    'script': [
        'ansible>=2.8',
        # 'paramiko',  # sa-script use ssh by default
        'progressbar2',
        'terminaltables',
    ],
    # sa-icinga
    'icinga': [
        'sentry-sdk',
        'Mako',
        'icinga2py',
        'inflect',
    ],
    # sa-tc
    'tencentcloud': [
        'tencentcloud-sdk-python',
        'PyYAML',
        'inflection',
    ],
}

entry_points = """
    [console_scripts]
    sa-uptime = sa_tools_core.uptime:main
    sa-dns = sa_tools_core.dns:main
    sa-disk = sa_tools_core.disk:main
    sa-notify = sa_tools_core.notify:main
    sa-access = sa_tools_core.access:main
    sa-script = sa_tools_core.script:main [script]
    sa-icinga = sa_tools_core.icinga:main [icinga]
    sa-tc = sa_tools_core.tc:main [tencentcloud]
    sa-github = sa_tools_core.github:main
    # sa-node = sa_tools_core.node:main
    # sa-lvs = sa_tools_core.lvs:main
    # sa-rsync = sa_tools_core.rsync:main
"""

scripts = []

setup(
    name='sa-tools-core',
    version=version,
    description="SA Tools Core",
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    # Get more strings from
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    url='https://github.com/douban/sa-tools-core',
    keywords=['sa-tools', 'sysadmin', 'command line tools'],
    author='sysadmin',
    author_email='sysadmin@douban.com',
    license='BSD',
    packages=find_packages(exclude=['examples*', 'tests*']),
    include_package_data=True,
    zip_safe=False,
    entry_points=entry_points,
    scripts=scripts,
    install_requires=requirements,
    extras_require=extras_require,
)  # NOQA
