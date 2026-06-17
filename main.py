import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

import json

from src.cleanroom.agents.dependency.agent import DependencyAnalyzer
from src.cleanroom.agents.spec_agent.agent import SpecAgent


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python main.py <path-to-srs.xml>")
        sys.exit(1)

    srs_path = Path(sys.argv[1])
    agent = SpecAgent()
    ir = agent.run(srs_path)

    print(f"\nExtracted from : {srs_path.name}")
    print(f"Project        : {ir.project_name}")
    print(f"Features       : {len(ir.features)}")
    for feature in ir.features:
        print(f"  - {feature.name} ({len(feature.functional_requirements)} req)")
    print(f"Specifications : {len(ir.specifications)}")
    print(f"Nonfunctional  : {len(ir.nonfunctional_requirements)}")
    if ir.extraction_notes:
        print(f"Notes          : {ir.extraction_notes}")

    # Agent 2: fold the dependency graph into the IR and re-save it.
    enriched = DependencyAnalyzer().enrich(ir.model_dump())
    dest = Path("outputs") / f"{srs_path.stem}_ir.json"
    dest.write_text(json.dumps(enriched, indent=2))

    graph = enriched["dependency_graph"]
    print(f"\nDependency graph ({len(graph['edges'])} edges):")
    for edge in graph["edges"]:
        print(f"  - {edge['source']} depends on {edge['target']}")
    print(f"Build order    : {' -> '.join(graph['build_order'])}")
    if graph["cycles"]:
        print(f"Cycles         : {graph['cycles']}")
    print(f"Saved          : {dest}")


if __name__ == "__main__":
    main()
