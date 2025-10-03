"""
KYC Service
Orchestrates screening workflow across all components
"""

import pandas as pd
import io
from typing import Dict, List, Any
from fastapi import UploadFile


class KYCService:
    def __init__(self, pathway_engine, landing_ai, adverse_media, explain_service):
        self.pathway_engine = pathway_engine
        self.landing_ai = landing_ai
        self.adverse_media = adverse_media
        self.explain_service = explain_service
    
    async def process_csv(self, file: UploadFile) -> List[Dict[str, Any]]:
        """Process CSV file with applicants"""
        content = await file.read()
        df = pd.read_csv(io.BytesIO(content))
        
        results = []
        for _, row in df.iterrows():
            applicant_data = row.to_dict()
            result = await self.screen_applicant(applicant_data)
            results.append(result)
        
        return results
    
    async def screen_applicant(self, applicant_data: Dict[str, Any]) -> Dict[str, Any]:
        """Screen a single applicant through the full workflow"""
        
        # Get adverse media count
        name = applicant_data.get("name", "")
        adverse_count = self.adverse_media.get_adverse_count(name)
        applicant_data["adverse_media_count"] = adverse_count
        
        # Run through pathway engine
        screening_result = self.pathway_engine.evaluate_rules(applicant_data)
        
        # Generate explanation
        explanation = self.explain_service.explain_decision(screening_result)
        
        # Combine results
        return {
            "applicant": {
                "name": applicant_data.get("name"),
                "email": applicant_data.get("email"),
                "country": applicant_data.get("country"),
                "dob": applicant_data.get("dob")
            },
            "decision": screening_result["decision"],
            "triggered_rule": screening_result["triggered_rule"],
            "match_result": screening_result["match_result"],
            "adverse_media_count": adverse_count,
            "explanation": explanation,
            "timestamp": screening_result["timestamp"]
        }
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics"""
        return self.pathway_engine.get_metrics()
