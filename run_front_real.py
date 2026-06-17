"""One-off: run Spec -> Dependency -> Planning with the REAL model, stop at planning.

Mirrors run_pipeline.run()'s front three stages but does not enter Code/Test, so a
token-spending run produces the real (non-stub) per-FR contracts cheaply. Writes the
same per-stage JSON snapshots into outputs/ via each agent's enrich(output_dir=...).
"""
import sys
from pathlib import Path

from dotenv import load_dotenv

from src.cleanroom.agents.spec_agent.agent import SpecAgent
from src.cleanroom.agents.dependency.agent import DependencyAnalyzer
from src.cleanroom.agents.planning.agent import PlanningAgent
from src.cleanroom.llms.callbacks.metric import GLOBAL_METRICS

load_dotenv()

srs = Path(sys.argv[1])
out = Path("outputs")

# [1] Spec: deterministic parse + real LLM FR/NFR classification.
spec = SpecAgent()
ir = spec.run(srs, output_dir=out).model_dump()
ir = spec.enrich(ir, output_dir=out)
print(f"[1] Spec      : {len(ir['features'])} features")

# [2] Dependency: deterministic outer + inner (matches real run: llm=None).
ir = DependencyAnalyzer(llm=None).enrich(ir, output_dir=out)
print(f"[2] Dependency: build_order = {' -> '.join(ir['dependency_graph']['build_order'])}")

# [3] Planning: real LLM, one structured call per feature.
ir = PlanningAgent(llm=None).enrich(ir, output_dir=out)
contracts = ir["planning"]["contracts"]
print(f"[3] Planning  : {len(contracts)} contracts written to outputs/{srs.stem}_planning.json")

m = GLOBAL_METRICS
print(f"\nTokens: in={m.input_tokens} out={m.output_tokens} total={m.total_tokens} calls={len(m.calls)}")
