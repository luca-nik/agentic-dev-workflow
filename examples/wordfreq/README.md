# Example — `wordfreq`

A tiny, runnable project that demonstrates the **agentic-dev-workflow** end to end:
blueprints with acceptance examples, self-contained work orders, component-phased
planning with a fake, a Verifier-written contract test, and the full log trail.

`wordfreq` counts word frequencies in text. It has two components, which is just
enough to show component phasing and the integration endgame:

- **tokenizer** — `tokenize(text) -> list[str]`, lowercase, split on non-alphanumeric.
- **counter** — `count_frequencies(tokens) -> dict[str, int]`, the top-N consumer.

This example carries the **tokenizer** all the way through (blueprint → work order →
implementation → gate / contract test), and shows **counter** as a planned downstream
phase that develops against a `FakeTokenizer` until integration retires the fake.

## What to look at

| Path | Shows |
|------|-------|
| `agentic/blueprints/TOKENIZER_BLUEPRINT.md` | A blueprint with acceptance examples — the testable contract |
| `agentic/blueprints/COUNTER_BLUEPRINT.md` | The interface the fake must match exactly |
| `agentic/plan/DEVELOPMENT_PLAN.md` | Component phases, each with a named gate command |
| `agentic/plan/TASKS.md` | Globally sequential IDs; gate tasks; the fake; integration phase |
| `agentic/plan/tasks/TASK-001.md` | A self-contained work order |
| `agentic/logs/AGENT_LOG.md` | Append-only question/response pair (D3 format) — the apostrophe decision |
| `agentic/logs/DEVLOG.md` | A Developer orchestrator session log |
| `agentic/logs/DEVIATIONS.md` | Where implementation diverged from blueprint (with blueprint update) |
| `agentic/logs/CLARIFICATIONS.md` | An interpretive ambiguity resolved without a blueprint change |
| `tests/contract/test_tokenizer.py` | Black-box contract tests the Verifier derived from the blueprint |
| `tests/fakes/fake_tokenizer.py` | The exact-interface fake counter develops against |
| `src/wordfreq/tokenizer.py` | The implementation |

## Run it

```bash
cd examples/wordfreq
python -m pytest -q
```

The contract tests pass against the real tokenizer; the fake exists for `counter`'s
phase, which is not yet implemented in this snapshot.
