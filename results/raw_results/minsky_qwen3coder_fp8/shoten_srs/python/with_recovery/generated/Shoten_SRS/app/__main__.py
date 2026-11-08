"""Run the assembled app:  python -m app"""
import uvicorn

from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.with_recovery.generated.Shoten_SRS.app import create_app

if __name__ == "__main__":
    uvicorn.run(create_app(), host="0.0.0.0", port=8000)
