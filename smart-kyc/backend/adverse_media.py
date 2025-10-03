"""
Adverse Media Scanner
Searches for negative news, sanctions, fraud, and other adverse information
"""

from typing import Dict, List, Any
import random


class AdverseMediaScanner:
    def __init__(self):
        # Mock adverse media database
        self.adverse_db = {
            "Vladimir Petrov": [
                {
                    "topic": "Sanctions Violation",
                    "source": "Reuters",
                    "date": "2023-08-15",
                    "snippet": "Vladimir Petrov allegedly involved in sanctions evasion scheme...",
                    "trigger_lines": ["sanctions evasion", "financial misconduct"],
                    "severity": "high"
                },
                {
                    "topic": "Money Laundering Investigation",
                    "source": "Financial Times",
                    "date": "2023-06-20",
                    "snippet": "Authorities investigating Petrov for potential money laundering activities...",
                    "trigger_lines": ["money laundering", "investigation"],
                    "severity": "high"
                }
            ],
            "Ahmed Rashid": [
                {
                    "topic": "Terrorism Financing",
                    "source": "UN Report",
                    "date": "2022-11-10",
                    "snippet": "Ahmed Rashid linked to organizations suspected of terrorism financing...",
                    "trigger_lines": ["terrorism financing", "suspicious transactions"],
                    "severity": "critical"
                }
            ],
            "Maria Santos": [
                {
                    "topic": "Political Corruption",
                    "source": "Associated Press",
                    "date": "2024-01-05",
                    "snippet": "Maria Santos named in corruption probe involving government contracts...",
                    "trigger_lines": ["corruption", "bribery", "government contracts"],
                    "severity": "high"
                }
            ],
            "John Smith": [
                {
                    "topic": "Tax Evasion",
                    "source": "Wall Street Journal",
                    "date": "2023-09-12",
                    "snippet": "John Smith accused of offshore tax evasion schemes...",
                    "trigger_lines": ["tax evasion", "offshore accounts"],
                    "severity": "medium"
                }
            ]
        }
    
    async def search(self, name: str) -> Dict[str, Any]:
        """
        Search for adverse media related to an entity
        Returns topics, snippets, and trigger lines
        """
        
        # Check if we have mock data for this name
        results = []
        
        # Exact match
        if name in self.adverse_db:
            results = self.adverse_db[name]
        else:
            # Fuzzy match (simple contains check)
            for db_name, articles in self.adverse_db.items():
                if name.lower() in db_name.lower() or db_name.lower() in name.lower():
                    results = articles
                    break
        
        return {
            "entity": name,
            "total_hits": len(results),
            "articles": results,
            "topics": list(set([r["topic"] for r in results])),
            "max_severity": self._get_max_severity(results)
        }
    
    def _get_max_severity(self, results: List[Dict[str, Any]]) -> str:
        """Get the highest severity level from results"""
        if not results:
            return "none"
        
        severity_order = {"critical": 4, "high": 3, "medium": 2, "low": 1, "none": 0}
        severities = [r.get("severity", "none") for r in results]
        max_sev = max(severities, key=lambda x: severity_order.get(x, 0))
        return max_sev
    
    def get_adverse_count(self, name: str) -> int:
        """Get count of adverse media hits for an entity"""
        if name in self.adverse_db:
            return len(self.adverse_db[name])
        
        # Fuzzy match
        for db_name, articles in self.adverse_db.items():
            if name.lower() in db_name.lower() or db_name.lower() in name.lower():
                return len(articles)
        
        return 0
