# This file is part of Hypothesis, which may be found at
# https://github.com/HypothesisWorks/hypothesis/
#
# Most of this work is copyright (C) 2013-2020 David R. MacIver
# (david@drmaciver.com), but it contains contributions by others. See
# CONTRIBUTING.rst for a full list of people who may hold copyright, and
# consult the git log if you need to determine who owns an individual
# contribution.
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at https://mozilla.org/MPL/2.0/.
#
# END HEADER

from __future__ import absolute_import, division, print_function

import subprocess
import sys

SHOULD_NOT_IMPORT_TEST_RUNNERS = """
import sys
import unittest
from hypothesis import given, strategies as st

class TestDoesNotImportRunners(unittest.TestCase):
    strat = st.integers() | st.floats() | st.sampled_from(["a", "b"])

    @given(strat)
    def test_does_not_import_unittest2(self, x):
        assert "unittest2" not in sys.modules

    @given(strat)
    def test_does_not_import_nose(self, x):
        assert "nose" not in sys.modules

    @given(strat)
    def test_does_not_import_pytest(self, x):
        assert "pytest" not in sys.modules

if __name__ == '__main__':
    unittest.main()
"""


def test_hypothesis_does_not_import_test_runners(tmp_path):
    # We obviously can't use pytest to check that pytest is not imported,
    # so for consistency we use unittest for all three non-stdlib test runners.
    # It's unclear which of our dependencies is importing unittest, but
    # since I doubt it's causing any spurious failures I don't really care.
    # See https://github.com/HypothesisWorks/hypothesis/pull/2204
    fname = str(tmp_path / "test.py")
    with open(fname, "w") as f:
        f.write(SHOULD_NOT_IMPORT_TEST_RUNNERS)
    subprocess.check_call([sys.executable, fname])
