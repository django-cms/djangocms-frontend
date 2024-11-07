#!/usr/bin/env python
import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner


def pytest_configure():
    os.environ["DJANGO_SETTINGS_MODULE"] = "tests.test_settings"
    django.setup()


if __name__ == "__main__":
    pytest_configure()

    argv = ["tests"] if sys.argv is None else sys.argv
    tests = argv[1:] if len(argv) > 1 else ["tests"]
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(tests)
    sys.exit(bool(failures))
