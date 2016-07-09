PY=/usr/bin/python
NOSE=/usr/bin/nosetests -s -v --with-xunit --with-coverage --cover-erase --cover-package trols_stats
NOSE_ENV=.env/bin/nosetests -s -v --with-xunit --with-coverage --cover-erase --cover-package trols_stats
PYTEST=$(shell which py.test)
GIT=/usr/bin/git
COVERAGE=/usr/bin/coverage
COVERAGE_ENV=.env/bin/coverage
PYTHONPATH=.:../logga:../configa:../filer

# The TESTS variable can be set to allow you to control which tests
# to run.  For example, if the current project has a test set defined at
# "tests/test_<name>.py", to run the "Test<class_name>" class:
#
# $ make test TESTS=tests:Test<class_name>
#
# To run individual test cases within each test class:
#
# $ make test TESTS=tests:Test<class_name>.test_<test_name>
#
# Note: for this to work you will need to import the test class into
# the current namespace via "tests/__init__.py"
TESTS=trols_stats/tests/test_scraper.py::TestScraper \
	trols_stats/tests/test_stats.py::TestStats \
	trols_stats/tests/test_dbsession.py::TestDBSession \
	trols_stats/interface/tests/test_loader.py::TestLoader \
	trols_stats/interface/tests/test_reporter.py::TestReporter \
	trols_stats/model/entities/tests/test_player.py::TestPlayer \
	trols_stats/model/entities/tests/test_fixture.py::TestFixture \
	trols_stats/model/aggregates/tests/test_game.py::TestGame \
	trols_stats/tests/test_statistics.py::TestStatistics \
	trols_stats/tests/test_config.py::TestConfig \
	trols_stats/exception/tests/test_exception.py::TestTrolsStatsConfigError

sdist:
	$(PY) setup.py sdist

rpm:
	$(PY) setup.py bdist_rpm --fix-python

docs:
	PYTHONPATH=$(PYTHONPATH) sphinx-1.0-build -b html doc/source doc/build

build: rpm

tests:
	 PYTHONPATH=$(PYTHONPATH) $(PYTEST) --capture=no -v $(TESTS)

coverage: test
	$(COVERAGE) xml -i

coverage_env: test_env
	$(COVERAGE_ENV) xml -i

uninstall:
	$(RPM) -e python-trols-scraper

install:
	$(RPM) -ivh dist/python-trols-scraper-?.?.?-?.noarch.rpm

upgrade:
	$(RPM) -Uvh dist/python-trols-scraper-?.?.?-?.noarch.rpm

clean:
	$(GIT) clean -xdf

.PHONY: docs rpm test
