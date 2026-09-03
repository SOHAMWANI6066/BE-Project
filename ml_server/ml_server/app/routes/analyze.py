from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import asyncio
from concurrent.futures import ThreadPoolExecutor

from pipeline.analyze_clause import analyze_clause

router = APIRouter()

# 🔥 Controlled thread pool (prevents overload)
executor = ThreadPoolExecutor(max_workers=2)


class BatchRequest(BaseModel):
    clauses: List[str]


@router.post("/batch")
async def analyze_batch(request: BatchRequest):

    loop = asyncio.get_event_loop()

    async def process_clause(clause: str):
        try:
            # Run heavy ML work in background thread
            return await loop.run_in_executor(
                executor,
                analyze_clause,
                clause
            )
        except Exception as e:
            # 🔥 DO NOT CRASH SERVER
            return {
                "original_clause": clause,
                "clause_type": None,
                "risk_level": None,
                "simplified_text": None,
                "simplification_method": None,
                "decision_trace": None,
                "error": str(e)
            }

    tasks = [process_clause(clause) for clause in request.clauses]

    results = await asyncio.gather(*tasks)

    return {"results": results}