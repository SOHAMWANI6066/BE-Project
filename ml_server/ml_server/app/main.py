import os
import sys
from fastapi import FastAPI

# 1. System Path Setup (Must happen BEFORE imports that rely on it)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
ML_RESEARCH_PATH = os.path.join(PROJECT_ROOT, "ml-research")

if ML_RESEARCH_PATH not in sys.path:
    sys.path.insert(0, ML_RESEARCH_PATH)

# 2. Imports (Now that the path is set, these won't fail)
try:
    from app.routes.analyze import router as analyze_router
except ImportError as e:
    print(f"CRITICAL: Could not find analyze_router. Check your path: {ML_RESEARCH_PATH}")
    raise e

# 3. App Initialization
app = FastAPI(title="ZeroPaper ML Service")

# 4. Route Definitions (After app exists)
@app.get("/health")
def health():
    return {"status": "online"}

app.include_router(analyze_router, prefix="/analyze")

# Diagnostic output
if __name__ == "__main__":
    print("ML_RESEARCH_PATH:", ML_RESEARCH_PATH)
    print("Path Exists:", os.path.exists(ML_RESEARCH_PATH))