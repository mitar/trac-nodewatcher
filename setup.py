from setuptools import setup

VERSION = '0.1'
PACKAGE = 'trac_nodewatcher'

setup(
	name = 'NodewatcherPlugin',
	version = VERSION,
	description = "nodewatcher integration with Trac.",
	author = 'Mitar',
	author_email = 'mitar.trac@tnode.com',
	url = 'http://mitar.tnode.com/',
	keywords = 'trac plugin',
	license = "GPLv3",
	packages = [PACKAGE],
    include_package_data = True,
	install_requires = [],
	zip_safe = False,
	entry_points = {
		'trac.plugins': '%s = %s' % (PACKAGE, PACKAGE),
	},
)
