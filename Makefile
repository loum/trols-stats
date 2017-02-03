# Check if we have python3 available.
PY3_VERSION := $(shell python3 --version 2>/dev/null)
PY3_VERSION_FULL := $(wordlist 2, 4, $(subst ., , ${PY3_VERSION}))
PY3_VERSION_MAJOR := $(word 1, ${PY3_VERSION_FULL})
PY3_VERSION_MINOR := $(word 2, ${PY3_VERSION_FULL})
PY3_VERSION_PATCH := $(word 3, ${PY3_VERSION_FULL})
USE_PY3VENV := $(shell [ ${PY3_VERSION_MINOR} -ge 3 ] && echo 0 || echo 1)
ifneq ($(PY3_VERSION),)
  PY := $(shell which python3 2>/dev/null)
  ifeq ($(USE_PYVENV), 1)
    PY_VENV := pyvenv-${PY3_VERSION_MAJOR}.${PY3_VERSION_MINOR}
  endif
else
  PY_VENV := $(shell which virtualenv 2>/dev/null)
  PY := $(shell which python 2>/dev/null)
endif

# OK, set some globals.
WHEEL=~/wheelhouse

GIT=$(shell which git 2>/dev/null)

# Define the default test suit to run.
TESTS=trols_stats/tests/test_scraper.py::TestScraper \
  trols_stats/tests/test_stats.py::TestStats \
  trols_stats/tests/test_dbsession.py::TestDBSession \
  trols_stats/interface/tests/test_loader.py::TestLoader \
  trols_stats/interface/tests/test_reporter.py::TestReporter \
  trols_stats/model/entities/tests/test_player.py::TestPlayer \
  trols_stats/model/entities/tests/test_fixture.py::TestFixture \
  trols_stats/model/entities/tests/test_match_round.py::TestMatchRound \
  trols_stats/model/aggregates/tests/test_game.py::TestGame \
  trols_stats/tests/test_statistics.py::TestStatistics \
  trols_stats/tests/test_config.py::TestConfig \
  trols_stats/exception/tests/test_exception.py::TestTrolsStatsConfigError

tests:
	PYTHONPATH=$(PYTHONPATH) $(shell which py.test) \
	--cov-config .coveragerc --cov=trols_stats -sv $(TESTS)

docs:
	PYTHONPATH=$(PYTHONPATH) $(shell which sphinx-build) \
	-b html doc/source doc/build

clean:
	$(GIT) clean -xdf

VENV_DIR_EXISTS := $(shell [ -e "venv" ] && echo 1 || echo 0)
clear_env:
ifeq ($(VENV_DIR_EXISTS), 1)
	@echo \#\#\# Deleting existing environment venv ...
	$(shell which rm) -fr venv
	@echo \#\#\# venv delete done.
endif

init_env:
	@echo \#\#\# Creating virtual environment venv ...
ifneq ($(PY3_VERSION),)
    ifeq ($(USE_PY3VENV), 0)
		$(PY) -m venv venv
    else
		$(PY_VENV) venv
    endif
	@echo \#\#\# venv build done.

	@echo \#\#\# Installing package dependencies ...
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -e .
	@echo \#\#\# Package install done.
else
	@echo \#\#\# Hmmm, cannot find python3 exe.
	@echo \#\#\# Virtual environment not created.
endif

init: clear_env init_env

init_env_from_wheel:
	@echo \#\#\# Creating virtual environment venv.
	@echo \#\#\# Using wheel house $(WHEEL) ...
ifneq (${PY3_VERSION},)
    ifeq ($(USE_PY3VENV), 0)
		$(PY) -m venv venv
    else
		$(PY_VENV) venv
    endif
	@echo \#\#\# venv build done.

	@echo \#\#\# Preparing wheel environment and directory ...
	$(shell which mkdir) -pv $(WHEEL) 2>/dev/null
	venv/bin/pip install --upgrade pip
	venv/bin/pip install wheel
	@echo \#\#\# wheel env done.

	@echo \#\#\# Installing package dependencies ...
	venv/bin/pip wheel --wheel-dir $(WHEEL) --find-links=$(WHEEL) .
	venv/bin/pip install --use-wheel --find-links=$(WHEEL) -e .
	@echo \#\#\# Package install done.
else
	@echo \#\#\# Hmmm, cannot find python3 exe.
	@echo \#\#\# Virtual environment not created.
endif

init_wheel: clear_env init_env_from_wheel

init_build: init_env_from_wheel build

build:
	@echo \#\#\# Building package ...
	venv/bin/python setup.py sdist bdist_wheel -d $(WHEEL)
	@echo \#\#\# Build done.

upload:
	$(PY) setup.py sdist upload -r internal

py_versions:
	@echo python3 version: ${PY3_VERSION}
	@echo python3 minor: ${PY3_VERSION_MINOR}
	@echo USE_PY3VENV: ${USE_PY3VENV}
	@echo python3 virtualenv command: ${PY_VENV}
	@echo path to python executable: ${PY}

.PHONY: tests docs py_versions init build upload
