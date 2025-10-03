"""
Explanation Service
Generates human-readable explanations for screening decisions and drafts reports
"""

from typing import Dict, Any
from datetime import datetime


class ExplainService:
    def explain_decision(self, decision_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate explanation for a screening decision with citations
        """
        decision = decision_data.get("decision", "UNKNOWN")
        triggered_rule = decision_data.get("triggered_rule", {})
        match_result = decision_data.get("match_result", {})
        enriched_data = decision_data.get("enriched_data", {})
        
        # Build explanation
        explanation_parts = []
        citations = []
        
        # Decision summary
        if decision == "BLOCK":
            explanation_parts.append(f"❌ **Decision: BLOCKED**")
        elif decision == "REVIEW":
            explanation_parts.append(f"⚠️ **Decision: FLAGGED FOR REVIEW**")
        elif decision == "APPROVE":
            explanation_parts.append(f"✅ **Decision: APPROVED**")
        
        # Rule explanation
        if triggered_rule:
            rule_desc = triggered_rule.get("description", "No description")
            rule_id = triggered_rule.get("id", "unknown")
            explanation_parts.append(f"\n**Triggered Rule:** {rule_desc} (ID: `{rule_id}`)")
            citations.append({
                "type": "rule",
                "id": rule_id,
                "description": rule_desc
            })
        
        # Match details
        if match_result.get("matched"):
            matched_entity = match_result.get("matched_entity")
            match_score = match_result.get("match_score")
            list_type = match_result.get("list_type")
            source = match_result.get("source")
            
            explanation_parts.append(
                f"\n**Match Found:** {matched_entity} ({list_type})\n"
                f"- Match Score: {match_score}%\n"
                f"- Source: {source}\n"
                f"- Country: {match_result.get('country', 'Unknown')}"
            )
            
            citations.append({
                "type": "sanctions_match",
                "entity": matched_entity,
                "score": match_score,
                "list_type": list_type,
                "source": source
            })
        
        # Adverse media
        adverse_count = enriched_data.get("adverse_media_count", 0)
        if adverse_count > 0:
            explanation_parts.append(
                f"\n**Adverse Media:** {adverse_count} article(s) found with negative coverage"
            )
            citations.append({
                "type": "adverse_media",
                "count": adverse_count
            })
        
        # Risk factors
        risk_factors = []
        if enriched_data.get("country") in ["North Korea", "Iran", "Syria", "Sudan"]:
            risk_factors.append(f"High-risk jurisdiction: {enriched_data.get('country')}")
        
        if enriched_data.get("pep_match"):
            risk_factors.append("Politically Exposed Person (PEP)")
        
        if risk_factors:
            explanation_parts.append("\n**Risk Factors:**")
            for factor in risk_factors:
                explanation_parts.append(f"- {factor}")
        
        # Recommendation
        if decision == "BLOCK":
            recommendation = "Do not onboard. Escalate to compliance officer immediately."
        elif decision == "REVIEW":
            recommendation = "Conduct Enhanced Due Diligence (EDD) before proceeding."
        else:
            recommendation = "Proceed with standard onboarding process."
        
        explanation_parts.append(f"\n**Recommendation:** {recommendation}")
        
        return {
            "explanation": "\n".join(explanation_parts),
            "citations": citations,
            "decision": decision,
            "confidence": self._calculate_confidence(decision_data),
            "timestamp": datetime.now().isoformat()
        }
    
    def _calculate_confidence(self, decision_data: Dict[str, Any]) -> float:
        """Calculate confidence score for the decision"""
        match_result = decision_data.get("match_result", {})
        
        if match_result.get("matched"):
            # High confidence if strong match
            return min(match_result.get("match_score", 0) / 100.0, 0.99)
        
        # Medium confidence for rule-based decisions
        return 0.75
    
    def draft_edd(self, applicant_data: Dict[str, Any]) -> str:
        """Draft Enhanced Due Diligence report"""
        name = applicant_data.get("name", "Unknown")
        country = applicant_data.get("country", "Unknown")
        
        report = f"""
# Enhanced Due Diligence Report

**Subject:** {name}  
**Date:** {datetime.now().strftime("%Y-%m-%d")}  
**Prepared By:** Smart KYC Screener (Automated)

## Executive Summary
This Enhanced Due Diligence (EDD) report has been prepared for {name} following automated Level-1 screening that flagged potential risk factors requiring additional review.

## Screening Results
- **Sanctions Screening:** {applicant_data.get('match_result', {}).get('matched_entity', 'No match')}
- **PEP Screening:** {'Match found' if applicant_data.get('pep_match') else 'No match'}
- **Adverse Media:** {applicant_data.get('adverse_media_count', 0)} article(s) found
- **Jurisdiction:** {country}

## Risk Assessment
Based on automated screening, the following risk factors were identified:
- Match score: {applicant_data.get('match_result', {}).get('match_score', 0)}%
- List type: {applicant_data.get('match_result', {}).get('list_type', 'N/A')}

## Recommendations
1. Verify identity through additional documentation
2. Conduct source of funds analysis
3. Review beneficial ownership structure (if applicable)
4. Obtain senior management approval before onboarding

## Next Steps
- [ ] Request additional documentation
- [ ] Conduct manual review of adverse media
- [ ] Verify sanctions list match manually
- [ ] Escalate to compliance officer

---
*This report was generated automatically by Smart KYC Screener. Manual review required.*
"""
        return report.strip()
    
    def draft_sar(self, applicant_data: Dict[str, Any]) -> str:
        """Draft Suspicious Activity Report"""
        name = applicant_data.get("name", "Unknown")
        
        report = f"""
# Suspicious Activity Report (SAR) - DRAFT

**Report Date:** {datetime.now().strftime("%Y-%m-%d")}  
**Subject:** {name}  
**Status:** DRAFT - REQUIRES REVIEW

## Part I - Subject Information
**Name:** {name}  
**Country:** {applicant_data.get('country', 'Unknown')}  
**Date of Birth:** {applicant_data.get('dob', 'Unknown')}  
**Email:** {applicant_data.get('email', 'Unknown')}

## Part II - Suspicious Activity
The following suspicious indicators were identified during automated KYC screening:

### Sanctions/PEP Match
- **Matched Entity:** {applicant_data.get('match_result', {}).get('matched_entity', 'N/A')}
- **Match Score:** {applicant_data.get('match_result', {}).get('match_score', 0)}%
- **List Type:** {applicant_data.get('match_result', {}).get('list_type', 'N/A')}
- **Source:** {applicant_data.get('match_result', {}).get('source', 'N/A')}

### Adverse Media
- **Articles Found:** {applicant_data.get('adverse_media_count', 0)}
- **Topics:** Sanctions violations, money laundering (see attached)

## Part III - Analysis
Automated screening flagged this individual due to:
1. High-confidence match with sanctions/PEP list
2. Presence of adverse media coverage
3. High-risk jurisdiction indicators

## Part IV - Recommendation
**Recommended Action:** DO NOT ONBOARD - File SAR with FinCEN

---
*DRAFT ONLY - This SAR draft was generated automatically. Compliance officer must review, verify, and complete before filing.*
"""
        return report.strip()
