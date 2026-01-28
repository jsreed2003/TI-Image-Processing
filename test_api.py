"""
Test script for FastAPI Keystone Correction API
Run this to verify the API is working correctly
"""

import requests
import json
from pathlib import Path

# Configuration
API_URL = "http://localhost:8000"
TEST_IMAGE_PATH = "test_projection.jpg"  # Replace with your test image path

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check endpoint...")
    response = requests.get(f"{API_URL}/health")
    
    if response.status_code == 200:
        print("✅ Health check passed")
        print(f"   Response: {response.json()}")
    else:
        print(f"❌ Health check failed: {response.status_code}")
    
    return response.status_code == 200


def test_corner_detection():
    """Test corner detection endpoint"""
    print("\nTesting corner detection endpoint...")
    
    # Check if test image exists
    if not Path(TEST_IMAGE_PATH).exists():
        print(f"❌ Test image not found: {TEST_IMAGE_PATH}")
        print("   Please provide a test image or update TEST_IMAGE_PATH")
        return False
    
    # Send request
    with open(TEST_IMAGE_PATH, 'rb') as f:
        files = {'file': f}
        response = requests.post(
            f"{API_URL}/api/detect_corners",
            files=files
        )
    
    if response.status_code == 200:
        print("✅ Corner detection passed")
        data = response.json()
        print(f"   Success: {data['success']}")
        print(f"   Message: {data['message']}")
        print(f"   Image size: {data['imageWidth']} x {data['imageHeight']}")
        print(f"   Original corners:")
        for i, corner in enumerate(data['originalCorners']):
            labels = ['Top-left', 'Top-right', 'Bottom-right', 'Bottom-left']
            print(f"     {labels[i]}: ({corner[0]:.1f}, {corner[1]:.1f})")
        print(f"   Optimal corners:")
        for i, corner in enumerate(data['optimalCorners']):
            labels = ['Top-left', 'Top-right', 'Bottom-right', 'Bottom-left']
            print(f"     {labels[i]}: ({corner[0]:.1f}, {corner[1]:.1f})")
    elif response.status_code == 422:
        print(f"❌ Corner detection failed (validation error)")
        print(f"   {response.json()}")
    else:
        print(f"❌ Corner detection failed: {response.status_code}")
        print(f"   {response.text}")
    
    return response.status_code == 200


def test_process_image():
    """Test full image processing endpoint"""
    print("\nTesting full processing endpoint...")
    
    if not Path(TEST_IMAGE_PATH).exists():
        print(f"❌ Test image not found: {TEST_IMAGE_PATH}")
        return False
    
    with open(TEST_IMAGE_PATH, 'rb') as f:
        files = {'file': f}
        response = requests.post(
            f"{API_URL}/api/process_image",
            files=files
        )
    
    if response.status_code == 200:
        print("✅ Full processing passed")
        data = response.json()
        print(f"   Success: {data['success']}")
        print(f"   Message: {data['message']}")
        print(f"   Has optimal input corners: {'optimalInputCorners' in data['data']}")
    else:
        print(f"❌ Full processing failed: {response.status_code}")
    
    return response.status_code == 200


def test_error_handling():
    """Test error handling with invalid input"""
    print("\nTesting error handling...")
    
    # Test with invalid file
    files = {'file': ('test.txt', b'not an image', 'text/plain')}
    response = requests.post(
        f"{API_URL}/api/detect_corners",
        files=files
    )
    
    if response.status_code in [400, 422, 500]:
        print("✅ Error handling works correctly")
        print(f"   Status code: {response.status_code}")
        print(f"   Error message: {response.json().get('detail', 'No detail')}")
    else:
        print(f"❌ Unexpected response for invalid input: {response.status_code}")
    
    return True


def test_api_docs():
    """Test that API documentation is accessible"""
    print("\nTesting API documentation...")
    
    # Test OpenAPI schema
    response = requests.get(f"{API_URL}/openapi.json")
    if response.status_code == 200:
        print("✅ OpenAPI schema accessible")
    else:
        print("❌ OpenAPI schema not accessible")
    
    # Test Swagger UI
    response = requests.get(f"{API_URL}/docs")
    if response.status_code == 200:
        print("✅ Swagger UI accessible at /docs")
    else:
        print("❌ Swagger UI not accessible")
    
    return True


def main():
    """Run all tests"""
    print("=" * 60)
    print("FastAPI Keystone Correction API - Test Suite")
    print("=" * 60)
    
    tests = [
        ("Health Check", test_health_check),
        ("Corner Detection", test_corner_detection),
        ("Full Processing", test_process_image),
        ("Error Handling", test_error_handling),
        ("API Documentation", test_api_docs),
    ]
    
    results = {}
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except requests.exceptions.ConnectionError:
            print(f"\n❌ Connection Error: Cannot connect to {API_URL}")
            print("   Make sure the FastAPI server is running:")
            print("   python main.py")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error in {name}: {e}")
            results[name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    for name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {name}")
    
    print("\n" + "=" * 60)
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed. Check the output above.")
    print("=" * 60)


if __name__ == "__main__":
    main()
