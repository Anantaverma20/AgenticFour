"""
Pathway Engine for KYC Screening
Handles fuzzy matching, rule evaluation, and real-time metrics
"""

import yaml
import pandas as pd
from fuzzywuzzy import fuzz
from typing import Dict, List, Any, Optional
from datetime import datetime


class PathwayEngine:
    def __init__(self):
        self.sanctions_df = None
        self.rules_config = None
        self.metrics = {
            "total_screened": 0,
            "approved": 0,
            "review": 0,
            "blocked": 0,
            "by_rule": {},
            "last_updated": None
        }
        self.load_sanctions()
        self.load_rules()
    
    def load_sanctions(self):
        """Load sanctions and PEP lists"""
        try:
            self.sanctions_df = pd.read_csv("data/sanctions.csv")
        except Exception as e:
            print(f"Warning: Could not load sanctions list: {e}")
            self.sanctions_df = pd.DataFrame(columns=["id", "name", "aliases", "country", "source", "list_type"])
    
    def load_rules(self):
        """Load rules from YAML"""
        try:
            with open("rules.yaml", "r") as f:
                self.rules_config = yaml.safe_load(f)
        except Exception as e:
            print(f"Warning: Could not load rules: {e}")
            self.rules_config = {"thresholds": {}, "rules": []}
    
    def reload_rules(self):
        """Reload rules (called after teach_rule)"""
        self.load_rules()
    
    def fuzzy_match_name(self, name: str, threshold: Optional[int] = None) -> Dict[str, Any]:
        """Perform fuzzy matching against sanctions/PEP lists"""
        if threshold is None:
            threshold = self.rules_config.get("thresholds", {}).get("fuzzy_match_threshold", 85)
        
        best_match = {
            "matched": False,
            "match_score": 0,
            "matched_entity": None,
            "list_type": None,
            "source": None,
            "country": None
        }
        
        if self.sanctions_df is None or len(self.sanctions_df) == 0:
            return best_match
        
        for _, row in self.sanctions_df.iterrows():
            # Check main name
            score = fuzz.ratio(name.lower(), row["name"].lower())
            
            # Check aliases
            if pd.notna(row.get("aliases")):
                aliases = str(row["aliases"]).split("|")
                for alias in aliases:
                    alias_score = fuzz.ratio(name.lower(), alias.lower())
                    score = max(score, alias_score)
            
            if score > best_match["match_score"]:
                best_match = {
                    "matched": score >= threshold,
                    "match_score": score,
                    "matched_entity": row["name"],
                    "list_type": row.get("list_type", "UNKNOWN"),
                    "source": row.get("source", "UNKNOWN"),
                    "country": row.get("country", "UNKNOWN")
                }
        
        return best_match
    
    def evaluate_condition(self, condition: Dict[str, Any], applicant_data: Dict[str, Any]) -> bool:
        """Evaluate a single condition"""
        field = condition.get("field")
        op = condition.get("op")
        value = condition.get("value")
        
        if field not in applicant_data:
            return False
        
        field_value = applicant_data[field]
        
        if op == "equals":
            return field_value == value
        elif op == "gte":
            return field_value >= value
        elif op == "gt":
            return field_value > value
        elif op == "lte":
            return field_value <= value
        elif op == "lt":
            return field_value < value
        elif op == "in":
            return field_value in value
        elif op == "contains":
            return value in str(field_value)
        else:
            return False
    
    def evaluate_rules(self, applicant_data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate all rules for an applicant"""
        # Perform fuzzy matching
        match_result = self.fuzzy_match_name(applicant_data.get("name", ""))
        
        # Enrich applicant data with match results
        enriched_data = {
            **applicant_data,
            "sanctions_match_score": match_result["match_score"],
            "pep_match": match_result["matched"] and match_result["list_type"] == "PEP",
            "sanctions_match": match_result["matched"] and match_result["list_type"] == "SANCTIONS",
            "adverse_media_count": applicant_data.get("adverse_media_count", 0),
            "match_details": match_result
        }
        
        # Evaluate rules in priority order
        rules = sorted(self.rules_config.get("rules", []), key=lambda x: x.get("priority", 999))
        
        triggered_rule = None
        for rule in rules:
            if not rule.get("enabled", True):
                continue
            
            conditions = rule.get("conditions", [])
            
            # Empty conditions means always trigger (default rule)
            if len(conditions) == 0:
                triggered_rule = rule
                break
            
            # All conditions must be true
            all_conditions_met = all(
                self.evaluate_condition(cond, enriched_data)
                for cond in conditions
            )
            
            if all_conditions_met:
                triggered_rule = rule
                break
        
        decision = triggered_rule["outcome"] if triggered_rule else "REVIEW"
        
        # Update metrics
        self.metrics["total_screened"] += 1
        if decision == "APPROVE":
            self.metrics["approved"] += 1
        elif decision == "REVIEW":
            self.metrics["review"] += 1
        elif decision == "BLOCK":
            self.metrics["blocked"] += 1
        
        rule_id = triggered_rule["id"] if triggered_rule else "unknown"
        self.metrics["by_rule"][rule_id] = self.metrics["by_rule"].get(rule_id, 0) + 1
        self.metrics["last_updated"] = datetime.now().isoformat()
        
        return {
            "decision": decision,
            "triggered_rule": triggered_rule,
            "match_result": match_result,
            "enriched_data": enriched_data,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics"""
        total = self.metrics["total_screened"]
        return {
            **self.metrics,
            "percentages": {
                "approved": round(self.metrics["approved"] / total * 100, 1) if total > 0 else 0,
                "review": round(self.metrics["review"] / total * 100, 1) if total > 0 else 0,
                "blocked": round(self.metrics["blocked"] / total * 100, 1) if total > 0 else 0
            }
        }
    
    def reset_metrics(self):
        """Reset metrics (for testing)"""
        self.metrics = {
            "total_screened": 0,
            "approved": 0,
            "review": 0,
            "blocked": 0,
            "by_rule": {},
            "last_updated": None
        }
