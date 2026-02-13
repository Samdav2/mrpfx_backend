import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_endpoints():
    print("Testing WooCommerce Endpoints...")
    try:
        response = requests.get(f"{BASE_URL}/wordpress/wc/orders")
        print(f"GET /wc/orders: {response.status_code}")
        if response.status_code == 200:
            print(f"  Found {len(response.json())} orders")
    except Exception as e:
        print(f"  Error: {e}")

    try:
        response = requests.get(f"{BASE_URL}/wordpress/wc/customers")
        print(f"GET /wc/customers: {response.status_code}")
        if response.status_code == 200:
            print(f"  Found {len(response.json())} customers")
    except Exception as e:
        print(f"  Error: {e}")

    print("\nTesting LearnPress Endpoints...")
    try:
        response = requests.get(f"{BASE_URL}/wordpress/learnpress/courses")
        print(f"GET /learnpress/courses: {response.status_code}")
        if response.status_code == 200:
            courses = response.json()
            print(f"  Found {len(courses)} courses")
            if courses:
                course_id = courses[0]['id']
                print(f"  Testing details for course {course_id}...")

                # Test Curriculum
                curr_resp = requests.get(f"{BASE_URL}/wordpress/learnpress/courses/{course_id}/curriculum")
                print(f"  GET /learnpress/courses/{course_id}/curriculum: {curr_resp.status_code}")

                # Test Enrollment (Expect 401/403 if not auth, or 200/400)
                # Since we don't have a valid user token in this script easily, we just check if endpoint exists (401 is good)
                enroll_resp = requests.post(f"{BASE_URL}/wordpress/learnpress/courses/{course_id}/enroll", json={"course_id": course_id})
                print(f"  POST /learnpress/courses/{course_id}/enroll: {enroll_resp.status_code} (Expected 401 without auth)")

    except Exception as e:
        print(f"  Error: {e}")

if __name__ == "__main__":
    test_endpoints()
