# Copilot instructions

## Commands

Run commands from `viikko4/tdd-ostoskori`. The project requires Python 3.14 or
newer and uses `uv`; pytest is the development dependency.

```text
uv sync
set PYTHONPATH=src
uv run pytest -q
```

Run one test with its pytest node identifier:

```text
set PYTHONPATH=src
uv run pytest -q src/tests/ostoskori_test.py::TestOstoskori::test_ostoskorin_hinta_ja_tavaroiden_maara_alussa
```

There is no project-specific build or lint command configured.

## Architecture

This is a small TDD shopping-cart exercise using a flat `src` layout:

- `tuote.py` defines `Tuote`, a product with a name and unit price.
- `ostos.py` defines `Ostos`, which wraps one product and tracks its quantity.
  A new purchase starts with quantity one; decreasing below zero clamps the
  quantity to zero; total price is quantity multiplied by the product price.
- `ostoskori.py` defines `Ostoskori`, the collection being developed in the
  exercise. Its public operations cover adding/removing products, clearing the
  cart, reading its contents, counting items, and calculating the total.
- `src/tests/ostoskori_test.py` contains the current `unittest.TestCase`
  tests. The implementation is intentionally incomplete as part of the TDD
  progression.

Modules are imported as top-level modules (for example, `from ostoskori import
Ostoskori`), so keep `PYTHONPATH=src` when running tests from the project root.

## Conventions

- Keep changes limited to this exercise; do not couple it to the other
  `viikko4` projects.
- Preserve the Finnish public method names and the existing method signatures.
- Tests use `unittest.TestCase`, `setUp`, and focused assertions. Extend the
  existing test class when adding behavior.
- Keep quantity and cart state encapsulated in the existing private attributes
  (`_lukumaara` and `_tuotteet`) rather than exposing new public state.
- Follow the existing simple object model: `Ostos` delegates product name and
  unit-price behavior to `Tuote`, while `Ostoskori` manages `Ostos` instances.

## Rules
- Tests executed with uv run pytest
- Code of ostos.py and tuote.py should not be changed
- Tests should not be edited unless explicitly asked
- Always implement absolutely minimal code that makes the tests pass