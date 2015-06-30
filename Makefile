PY=/usr/bin/python
NOSE=/usr/bin/nosetests -s -v --with-xunit --with-coverage --cover-erase --cover-package trols_stats
NOSE_ENV=.env/bin/nosetests -s -v --with-xunit --with-coverage --cover-erase --cover-package trols_stats
GIT=/usr/bin/git
COVERAGE=/usr/bin/coverage
COVERAGE_ENV=.env/bin/coverage
PYTHONPATH=.:../logga:../configa:../filer

# The TEST variable can be set to allow you to control which tests
# to run.  For example, if the current project has a test set defined at
# "tests/test_<name>.py", to run the "Test<class_name>" class:
#
# $ make test TEST=tests:Test<class_name>
#
# To run individual test cases within each test class:
#
# $ make test TEST=tests:Test<class_name>.test_<test_name>
#
# Note: for this to work you will need to import the test class into
# the current namespace via "tests/__init__.py"
TEST=trols_stats.tests:TestScraper \
	trols_stats.tests:TestStats \
	trols_stats.tests:TestDBSession \
	trols_stats.interface.tests:TestLoader \
	trols_stats.interface.tests:TestReporter \
	trols_stats.model.entities.tests:TestPlayer \
	trols_stats.model.entities.tests:TestFixture \
	trols_stats.model.aggregates.tests:TestGame \
	trols_stats.tests:TestConfig \
	trols_stats.tests:TestStore

sdist:
	$(PY) setup.py sdist

rpm:
	$(PY) setup.py bdist_rpm --fix-python

docs:
	PYTHONPATH=$(PYTHONPATH) sphinx-1.0-build -b html doc/source doc/build

build: rpm

test:
	 PYTHONPATH=$(PYTHONPATH) $(NOSE) $(TEST)

test_env:
	 $(NOSE_ENV) $(TEST)

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
