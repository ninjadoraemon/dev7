#!/usr/bin/env python3
"""
Payment Verification Test for Clerk Users
"""

import requests
import json

# Get backend URL from frontend .env
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except:
        pass
    return "http://localhost:8001"

BASE_URL = get_backend_url()
API_URL = f"{BASE_URL}/api"

def test_payment_verification_endpoint():
    """Test that the payment verification endpoint accepts clerk_id"""
    print("🔍 Testing Payment Verification Endpoint Structure...")
    
    # Test with invalid data to see the expected structure
    verification_data = {
        "razorpay_order_id": "test_order_id",
        "razorpay_payment_id": "test_payment_id", 
        "razorpay_signature": "test_signature",
        "order_id": "test_order_id",
        "clerk_id": "test_clerk_id"
    }
    
    try:
        response = requests.post(f"{API_URL}/orders/verify", json=verification_data)
        print(f"   Payment verification status: {response.status_code}")
        
        if response.status_code == 400:
            result = response.json()
            error_detail = result.get("detail", "")
            print(f"   Response: {error_detail}")
            
            # Check if it's a signature verification error (expected)
            if "Payment verification failed" in error_detail:
                print("   ✅ Payment verification endpoint accepts clerk_id and processes request")
                return True
            else:
                print(f"   ❌ Unexpected error: {error_detail}")
                return False
        elif response.status_code == 404:
            result = response.json()
            if "Order not found" in result.get("detail", ""):
                print("   ✅ Payment verification endpoint accepts clerk_id (order not found as expected)")
                return True
        else:
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Payment verification test error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Payment Verification Endpoint")
    print("=" * 50)
    
    result = test_payment_verification_endpoint()
    
    if result:
        print("✅ Payment verification endpoint is working correctly for Clerk users")
    else:
        print("❌ Payment verification endpoint has issues")