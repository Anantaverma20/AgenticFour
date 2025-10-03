#!/usr/bin/env python3
"""
Test script for Smart KYC Screener API
Run this after starting the backend to verify all endpoints work
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        print("✅ Health check passed")
        print(f"   Response: {response.json()}")
        return True
    else:
        print(f"❌ Health check failed: {response.status_code}")
        return False

def test_metrics():
    """Test metrics endpoint"""
    print("\n🔍 Testing /metrics endpoint...")
    response = requests.get(f"{BASE_URL}/metrics")
    if response.status_code == 200:
        print("✅ Metrics endpoint working")
        data = response.json()
        print(f"   Total screened: {data.get('total_screened', 0)}")
        return True
    else:
        print(f"❌ Metrics failed: {response.status_code}")
        return False

def test_rules():
    """Test rules endpoint"""
    print("\n🔍 Testing /rules endpoint...")
    response = requests.get(f"{BASE_URL}/rules")
    if response.status_code == 200:
        print("✅ Rules endpoint working")
        data = response.json()
        print(f"   Rules loaded: {len(data.get('rules', []))}")
        return True
    else:
        print(f"❌ Rules failed: {response.status_code}")
        return False

def test_screen_applicant():
    """Test screening a single applicant"""
    print("\n🔍 Testing /screen endpoint...")
    payload = {
        "name": "Vladimir Petrov",
        "country": "Russia",
        "dob": "1975-03-15",
        "email": "vpetrov@example.com",
        "document_type": "passport"
    }
    response = requests.post(f"{BASE_URL}/screen", json=payload)
    if response.status_code == 200:
        print("✅ Screen endpoint working")
        data = response.json()
        result = data.get('result', {})
        print(f"   Decision: {result.get('decision')}")
        print(f"   Match score: {result.get('match_result', {}).get('match_score', 0)}%")
        return True
    else:
        print(f"❌ Screen failed: {response.status_code}")
        return False

def test_adverse_media():
    """Test adverse media endpoint"""
    print("\n🔍 Testing /adverse-media endpoint...")
    response = requests.get(f"{BASE_URL}/adverse-media/Vladimir Petrov")
    if response.status_code == 200:
        print("✅ Adverse media endpoint working")
        data = response.json()
        print(f"   Articles found: {data.get('total_hits', 0)}")
        return True
    else:
        print(f"❌ Adverse media failed: {response.status_code}")
        return False

def test_teach_rule():
    """Test teaching a new rule"""
    print("\n🔍 Testing /teach-rule endpoint...")
    payload = {
        "rule_id": "test_api_rule",
        "description": "Test rule created by API test",
        "outcome": "REVIEW",
        "priority": 100,
        "conditions": [
            {"field": "country", "op": "equals", "value": "TestLand"}
        ],
        "enabled": True
    }
    response = requests.post(f"{BASE_URL}/teach-rule", json=payload)
    if response.status_code == 200:
        print("✅ Teach rule endpoint working")
        data = response.json()
        print(f"   Message: {data.get('message')}")
        return True
    else:
        print(f"❌ Teach rule failed: {response.status_code}")
        return False

def test_upload_csv():
    """Test CSV upload (requires applicants.csv)"""
    print("\n🔍 Testing /upload-csv endpoint...")
    try:
        with open("backend/data/applicants.csv", "rb") as f:
            files = {"file": ("applicants.csv", f, "text/csv")}
            response = requests.post(f"{BASE_URL}/upload-csv", files=files)
            if response.status_code == 200:
                print("✅ CSV upload working")
                data = response.json()
                print(f"   Total processed: {data.get('total', 0)}")
                metrics = data.get('metrics', {})
                print(f"   Approved: {metrics.get('approved', 0)}")
                print(f"   Review: {metrics.get('review', 0)}")
                print(f"   Blocked: {metrics.get('blocked', 0)}")
                return True
            else:
                print(f"❌ CSV upload failed: {response.status_code}")
                return False
    except FileNotFoundError:
        print("⚠️  CSV file not found, skipping test")
        return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("Smart KYC Screener - API Test Suite")
    print("=" * 60)
    
    tests = [
        test_health,
        test_metrics,
        test_rules,
        test_screen_applicant,
        test_adverse_media,
        test_teach_rule,
        test_upload_csv
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test error: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("✅ All tests passed! API is ready for demo.")
        sys.exit(0)
    else:
        print("⚠️  Some tests failed. Check the backend logs.")
        sys.exit(1)

if __name__ == "__main__":
    main()
