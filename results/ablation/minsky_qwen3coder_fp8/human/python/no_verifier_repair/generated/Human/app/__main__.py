"""Run the assembled app:  python -m app"""
import uvicorn

from results.ablation.minsky_qwen3coder_fp8.human.python.no_verifier_repair.generated.Human.app import create_app

if __name__ == "__main__":
    uvicorn.run(create_app(), host="0.0.0.0", port=8000)
