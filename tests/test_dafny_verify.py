"""Stage-4 Dafny verify adapter: parse a clean verification and a proof failure.

Skipped unless a Dafny toolchain is present (LemmaFit's `npm install` provides it)."""

import textwrap
from pathlib import Path

import pytest

from src.cleanroom.utils.dafny_verify import dafny_available, verify_dafny

requires_dafny = pytest.mark.skipif(not dafny_available(), reason="dafny toolchain not installed")

_GOOD = textwrap.dedent('''\
    function Double(x: int): int { x + x }

    lemma DoubleIsEven(x: int)
      ensures Double(x) % 2 == 0
    {}
''')

_BAD = textwrap.dedent('''\
    function Double(x: int): int { x + x }

    lemma WrongClaim(x: int)
      ensures Double(x) == x   // false for x != 0
    {}
''')


@requires_dafny
def test_verifies_correct_proof(tmp_path: Path):
    f = tmp_path / "good.dfy"
    f.write_text(_GOOD)
    res = verify_dafny(f)
    assert res.ok, res.raw
    assert res.verified >= 1 and res.errors == 0


@requires_dafny
def test_reports_failed_proof_with_location(tmp_path: Path):
    f = tmp_path / "bad.dfy"
    f.write_text(_BAD)
    res = verify_dafny(f)
    assert not res.ok
    assert res.errors >= 1
    assert res.messages and res.messages[0]["line"] > 0  # has a source location to feed back
