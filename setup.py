# coding: utf-8

from setuptools import setup, find_packages

version = '0.1.0'


requirements = [
    'setuptools',
    'wechat',
    'pycrypto',
]


entry_points = """
      [console_scripts]
      sa-uptime = sa_tools_core.uptime:main
      # sa-dns = sa_tools_core.dns:main
      # sa-node = sa_tools_core.node:main
      # sa-rsync = sa_tools_core.rsync:main
      # sa-script = sa_tools_core.script:main
      # sa-lvs = sa_tools_core.lvs:main
      # sa-disk = sa_tools_core.disk:main
      sa-notify = sa_tools_core.notify:main
      # sa-icinga = sa_tools_core.icinga:main
      # sa-access = sa_tools_core.access:main
      # sa-bs = sa_tools_core.bs:main
      """

scripts = [
]

setup(name='sa-tools',
      version=version,
      description="SA Tools Core",
      long_description=open("README.md").read(),
      # Get more strings from
      # https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Programming Language :: Python",
      ],
      keywords='',
      author='sysadmin',
      author_email='sysadmin@douban.com',
      license='Douban',
      packages=find_packages(exclude=['examples*', 'tests*']),
      include_package_data=True,
      zip_safe=False,
      entry_points=entry_points,
      scripts=scripts,

      install_requires=requirements,
)  # NOQA
