"""
Smart KYC Screener - FastAPI Backend
Handles KYC screening with Pathway engine, Landing AI DPT-2, and live rule editing
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import yaml
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from pathway_engine import PathwayEngine
from landingai_client import LandingAIClient
from adverse_media import AdverseMediaScanner
from explain import ExplainService
from kyc_service import KYCService

app = FastAPI(title="Smart KYC Screener API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
pathway_engine = PathwayEngine()
landing_ai = LandingAIClient()
adverse_media = AdverseMediaScanner()
explain_service = ExplainService()
kyc_service = KYCService(pathway_engine, landing_ai, adverse_media, explain_service)

# Pydantic models
class ScreenRequest(BaseModel):
    name: str
    country: Optional[str] = None
    dob: Optional[str] = None
    email: Optional[str] = None
    document_type: Optional[str] = None

class TeachRuleRequest(BaseModel):
    rule_id: str
    description: str
    conditions: List[Dict[str, Any]]
    outcome: str
    priority: int = 50
    enabled: bool = True

class UpdateThresholdRequest(BaseModel):
    threshold_name: str
    value: Any

@app.get("/")
async def root():
    return {
        "service": "Smart KYC Screener",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    """Upload CSV file with applicants for batch screening"""
    try:
        results = await kyc_service.process_csv(file)
        return {
            "success": True,
            "total": len(results),
            "results": results,
            "metrics": kyc_service.get_metrics()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/upload-id")
async def upload_id(file: UploadFile = File(...)):
    """Upload ID document for DPT-2 extraction"""
    try:
        extraction_result = await landing_ai.extract_from_document(file)
        return {
            "success": True,
            "fields": extraction_result["fields"],
            "bounding_boxes": extraction_result["boxes"],
            "confidence": extraction_result["confidence"]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/screen")
async def screen_applicant(request: ScreenRequest):
    """Screen a single applicant"""
    try:
        result = await kyc_service.screen_applicant(request.dict())
        return {
            "success": True,
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/metrics")
async def get_metrics():
    """Get current screening metrics"""
    return kyc_service.get_metrics()

@app.get("/rules")
async def get_rules():
    """Get current rules configuration"""
    with open("rules.yaml", "r") as f:
        rules = yaml.safe_load(f)
    return rules

@app.post("/teach-rule")
async def teach_rule(request: TeachRuleRequest):
    """Teach the system a new rule (live editing)"""
    try:
        # Load current rules
        with open("rules.yaml", "r") as f:
            config = yaml.safe_load(f)
        
        # Add or update rule
        new_rule = {
            "id": request.rule_id,
            "description": request.description,
            "enabled": request.enabled,
            "priority": request.priority,
            "conditions": request.conditions,
            "outcome": request.outcome
        }
        
        # Check if rule exists
        rule_exists = False
        for i, rule in enumerate(config["rules"]):
            if rule["id"] == request.rule_id:
                config["rules"][i] = new_rule
                rule_exists = True
                break
        
        if not rule_exists:
            config["rules"].append(new_rule)
        
        # Sort by priority
        config["rules"].sort(key=lambda x: x.get("priority", 999))
        
        # Save updated rules
        with open("rules.yaml", "w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        
        # Reload rules in pathway engine
        pathway_engine.reload_rules()
        
        return {
            "success": True,
            "message": f"Rule '{request.rule_id}' {'updated' if rule_exists else 'added'} successfully",
            "rule": new_rule
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/update-threshold")
async def update_threshold(request: UpdateThresholdRequest):
    """Update a threshold value"""
    try:
        with open("rules.yaml", "r") as f:
            config = yaml.safe_load(f)
        
        if request.threshold_name not in config["thresholds"]:
            raise HTTPException(status_code=404, detail=f"Threshold '{request.threshold_name}' not found")
        
        config["thresholds"][request.threshold_name] = request.value
        
        with open("rules.yaml", "w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        
        pathway_engine.reload_rules()
        
        return {
            "success": True,
            "message": f"Threshold '{request.threshold_name}' updated to {request.value}"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/adverse-media/{name}")
async def get_adverse_media(name: str):
    """Get adverse media for an entity"""
    try:
        results = await adverse_media.search(name)
        return {
            "success": True,
            "entity": name,
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/explain")
async def explain_decision(decision_data: Dict[str, Any]):
    """Get explanation for a screening decision"""
    try:
        explanation = explain_service.explain_decision(decision_data)
        return {
            "success": True,
            "explanation": explanation
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/draft-edd")
async def draft_edd(applicant_data: Dict[str, Any]):
    """Draft Enhanced Due Diligence report"""
    try:
        report = explain_service.draft_edd(applicant_data)
        return {
            "success": True,
            "report": report
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/draft-sar")
async def draft_sar(applicant_data: Dict[str, Any]):
    """Draft Suspicious Activity Report"""
    try:
        report = explain_service.draft_sar(applicant_data)
        return {
            "success": True,
            "report": report
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
