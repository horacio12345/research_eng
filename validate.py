#!/usr/bin/env python3
"""
Quick validation script to check if main.py can be imported and basic functions work.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def test_imports():
    """Test that all imports work."""
    print("✓ Testing imports...")
    try:
        import main
        print("  ✓ main.py imports successfully")
        return True
    except Exception as e:
        print(f"  ✗ Import failed: {e}")
        return False

def test_dataclasses():
    """Test dataclass creation."""
    print("✓ Testing data models...")
    try:
        from main import Result, Topic, SearchConfig
        
        result = Result(
            title="Test",
            url="https://example.com",
            snippet="Test snippet"
        )
        print(f"  ✓ Result dataclass works: {result.title}")
        
        topic = Topic(
            name="Test Topic",
            keywords=["ai", "engineering"],
            search_variations=["test query"]
        )
        print(f"  ✓ Topic dataclass works: {topic.name}")
        
        return True
    except Exception as e:
        print(f"  ✗ Dataclass test failed: {e}")
        return False

def test_config_loading():
    """Test config file loading."""
    print("✓ Testing config loading...")
    try:
        from main import load_config
        
        config = load_config('config.yaml')
        print(f"  ✓ Config loaded: {len(config.topics)} topics found")
        print(f"  ✓ Search depth: {config.search_depth}")
        print(f"  ✓ AI model: {config.ai_model}")
        return True
    except Exception as e:
        print(f"  ✗ Config loading failed: {e}")
        return False

def test_query_generation():
    """Test query generation."""
    print("✓ Testing query generation...")
    try:
        from main import build_queries_for_topic, Topic
        
        topic = Topic(
            name="Test",
            keywords=["AI", "engineering"],
            search_variations=["custom query"]
        )
        
        queries = build_queries_for_topic(topic, min_year=2024)
        print(f"  ✓ Generated {len(queries)} queries")
        for q in queries[:2]:
            print(f"    - {q}")
        return True
    except Exception as e:
        print(f"  ✗ Query generation failed: {e}")
        return False

def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("Research Automation Tool - Validation Tests")
    print("="*60 + "\n")
    
    tests = [
        test_imports,
        test_dataclasses,
        test_config_loading,
        test_query_generation
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
            print()
        except Exception as e:
            print(f"✗ Test failed with exception: {e}\n")
            results.append(False)
    
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All validation tests passed!")
        print("\nThe tool is ready to use. To run a full search:")
        print("  1. Add your API keys to .env file")
        print("  2. Run: python src/main.py")
    else:
        print("❌ Some tests failed. Please review errors above.")
    
    print("="*60 + "\n")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
