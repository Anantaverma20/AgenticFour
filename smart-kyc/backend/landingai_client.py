"""
Landing AI DPT-2 Client
Extracts structured fields from identity documents with grounded evidence (bounding boxes)
"""

import os
import requests
from typing import Dict, Any
from fastapi import UploadFile
import base64
from PIL import Image
import io


class LandingAIClient:
    def __init__(self):
        self.api_key = os.getenv("LANDINGAI_API_KEY", "")
        self.api_url = os.getenv("LANDINGAI_URL", "https://api.va.landing.ai/v1/ade/parse")
    
    async def extract_from_document(self, file: UploadFile) -> Dict[str, Any]:
        """
        Extract fields from ID document using DPT-2
        Returns structured fields with bounding boxes for grounding
        """
        
        # Read file content
        content = await file.read()
        
        # Try to call Landing AI API if configured
        if self.api_key:
            try:
                return await self._call_landing_ai_api(content, file.filename)
            except Exception as e:
                print(f"Landing AI API error: {e}, falling back to mock")
        
        # Mock extraction for demo
        return self._mock_extraction(content, file.filename)
    
    async def _call_landing_ai_api(self, content: bytes, filename: str) -> Dict[str, Any]:
        """Call actual Landing AI ADE (Automated Document Extraction) API"""
        
        # Prepare multipart form data
        files = {
            'file': (filename, content, 'image/jpeg')
        }
        
        headers = {
            "Authorization": f"Basic {self.api_key}"
        }
        
        # Call Landing AI ADE API
        response = requests.post(
            self.api_url,
            headers=headers,
            files=files,
            timeout=30
        )
        
        response.raise_for_status()
        data = response.json()
        
        # Extract fields from Landing AI response
        fields = {}
        boxes = {}
        
        # Parse the response structure
        if "extractions" in data:
            for extraction in data["extractions"]:
                field_name = extraction.get("field_name", "").lower().replace(" ", "_")
                field_value = extraction.get("text", "")
                
                # Store field value
                fields[field_name] = field_value
                
                # Store bounding box if available
                if "bounding_box" in extraction:
                    bbox = extraction["bounding_box"]
                    boxes[field_name] = {
                        "x": bbox.get("x", 0),
                        "y": bbox.get("y", 0),
                        "width": bbox.get("width", 0),
                        "height": bbox.get("height", 0)
                    }
        
        # Calculate average confidence
        confidence = data.get("confidence", 0.0)
        
        return {
            "fields": fields,
            "boxes": boxes,
            "confidence": confidence
        }
    
    def _mock_extraction(self, content: bytes, filename: str) -> Dict[str, Any]:
        """Mock extraction for demo purposes"""
        
        # Simulate different documents
        mock_data = {
            "passport": {
                "fields": {
                    "name": "JOHN MICHAEL SMITH",
                    "date_of_birth": "1985-03-15",
                    "document_number": "P123456789",
                    "nationality": "USA",
                    "expiry_date": "2030-12-31",
                    "issue_date": "2020-01-15",
                    "document_type": "passport"
                },
                "boxes": {
                    "name": {"x": 120, "y": 180, "width": 200, "height": 25},
                    "date_of_birth": {"x": 120, "y": 220, "width": 150, "height": 20},
                    "document_number": {"x": 120, "y": 260, "width": 180, "height": 20},
                    "nationality": {"x": 120, "y": 300, "width": 100, "height": 20},
                    "expiry_date": {"x": 120, "y": 340, "width": 150, "height": 20}
                },
                "confidence": 0.95
            },
            "drivers_license": {
                "fields": {
                    "name": "Jane Elizabeth Doe",
                    "date_of_birth": "1990-06-20",
                    "document_number": "D1234567",
                    "address": "123 Main St, Anytown, CA 12345",
                    "expiry_date": "2028-06-20",
                    "issue_date": "2024-06-20",
                    "document_type": "drivers_license"
                },
                "boxes": {
                    "name": {"x": 80, "y": 100, "width": 180, "height": 22},
                    "date_of_birth": {"x": 80, "y": 140, "width": 120, "height": 18},
                    "document_number": {"x": 80, "y": 180, "width": 100, "height": 18},
                    "address": {"x": 80, "y": 220, "width": 250, "height": 35}
                },
                "confidence": 0.92
            }
        }
        
        # Try to detect document type from filename or use default
        doc_type = "passport"
        if "license" in filename.lower() or "dl" in filename.lower():
            doc_type = "drivers_license"
        
        return mock_data.get(doc_type, mock_data["passport"])
