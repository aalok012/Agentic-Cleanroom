"""Run the assembled app:  python -m app"""
import uvicorn

from results.raw_results.minsky_qwen3coder_fp8.human.python.raw_spec_only.generated.Human.app import create_app

if __name__ == "__main__":
    uvicorn.run(create_app(), host="0.0.0.0", port=8000)
