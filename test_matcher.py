"""
Test cases for DrugSymptomFinder matching engine.
Covering:
1. Exact clinical term search
2. Lay-term via synonym expansion
3. Partial/fuzzy term match
4. No match scenario
"""

import sys
from db import init_db
from matcher import search_drugs
from symptoms import expand_symptom_query

def run_tests():
    print("=" * 60)
    print("DRUG SYMPTOM FINDER - TEST SUITE FOR MATCHING LOGIC")
    print("=" * 60)
    
    # Ensure DB is populated
    init_db()

    # Test Case 1: Exact Clinical Term
    print("\n--- TEST CASE 1: Exact Clinical Term ('seizures') ---")
    res1 = search_drugs("seizures", min_score=50.0, limit=3)
    print(f"Query: 'seizures' | Found: {len(res1)} matches")
    for r in res1:
        print(f"  ➜ Drug: {r['drug_name']} | Confidence: {r['confidence_score']}%")
        print(f"    Indication: {r['indication'][:90]}...")
    assert len(res1) > 0, "Test Case 1 Failed: Expected matches for exact clinical term 'seizures'."
    print("✔ Test Case 1 Passed!")

    # Test Case 2: Lay-term via Synonym Expansion ("fever" -> "pyrexia")
    print("\n--- TEST CASE 2: Lay-term via Synonym ('fever') ---")
    expanded_terms = expand_symptom_query("fever")
    print(f"Expanded Terms for 'fever': {expanded_terms}")
    res2 = search_drugs("fever", min_score=50.0, limit=3)
    print(f"Query: 'fever' | Found: {len(res2)} matches")
    for r in res2:
        print(f"  ➜ Drug: {r['drug_name']} | Confidence: {r['confidence_score']}% | Matched: '{r['matched_term']}'")
        print(f"    Indication: {r['indication'][:90]}...")
    assert len(res2) > 0, "Test Case 2 Failed: Expected matches for lay-term 'fever'."
    print("✔ Test Case 2 Passed!")

    # Test Case 3: Partial / Fuzzy Match ("joint pain")
    print("\n--- TEST CASE 3: Partial/Fuzzy Match ('joint pain') ---")
    res3 = search_drugs("joint pain", min_score=45.0, limit=3)
    print(f"Query: 'joint pain' | Found: {len(res3)} matches")
    for r in res3:
        print(f"  ➜ Drug: {r['drug_name']} | Confidence: {r['confidence_score']}%")
        print(f"    Indication: {r['indication'][:90]}...")
    assert len(res3) > 0, "Test Case 3 Failed: Expected matches for fuzzy term 'joint pain'."
    print("✔ Test Case 3 Passed!")

    # Test Case 4: No Match Scenario ("xyz nonsense symptom")
    print("\n--- TEST CASE 4: No Match Scenario ('xyz nonsense symptom 99') ---")
    res4 = search_drugs("xyz nonsense symptom 99", min_score=60.0, limit=3)
    print(f"Query: 'xyz nonsense symptom 99' | Found: {len(res4)} matches")
    assert len(res4) == 0, "Test Case 4 Failed: Expected 0 matches for non-existent symptom."
    print("✔ Test Case 4 Passed!")

    print("\n" + "=" * 60)
    print("ALL MATCHING ENGINE TEST CASES PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
