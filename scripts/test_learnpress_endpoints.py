import asyncio
import httpx
import json

BASE_URL = "http://localhost:8000/api/v1/admin/learnpress"
# Assuming we have a way to authenticate or the endpoints differ in auth requirements.
# If auth is required, we might need a token.
# For now, let's assume we can mock or use a known user if the local dev setup allows,
# or we might hit 401.
# UPDATE: The endpoints typically use `get_current_user` dependency.
# We might need to login first or mock the dependency if we were running unit tests.
# Since we are running against a live server, we need a valid token.
# Let's assume there is a login endpoint or we can skip auth for local debug if configured,
# OR we can try to hit it and see. If 401, we might need to ask user or find a token.

# However, looking at the user state, `uvicorn` is running with reload.
# Let's try to find a way to get a token or use a known user.
# Generally in these envs, there might include a debug override or we can create a script that uses the internal functions directly to test usage which bypasses HTTP auth,
# BUT the user asked to "test it also" which implies hitting the endpoints.

# Let's check if there is a login endpoint in `app/main.py` or similar.
# For now, I will write a script that tries to hit the endpoints, and prints the result.

async def test_endpoints():
    async with httpx.AsyncClient() as client:
        # 1. Create Course
        course_data = {
            "title": "Test Course 101",
            "content": "<h1>Course Content</h1><p>Welcome to the course.</p>",
            "excerpt": "A test course",
            "status": "publish",
            "price": 0,
            "duration": "10 weeks",
            "level": "Beginner",
            "students": 0
        }
        res = await client.post(f"{BASE_URL}/courses", json=course_data)
        if res.status_code == 401:
            print("Auth required. Cannot test without token.")
            return

        print(f"Create Course: {res.status_code}")
        if res.status_code != 200:
            print(res.text)
            return

        course = res.json()
        course_id = course["id"]
        print(f"Course ID: {course_id}")

        # 2. Create Section
        section_data = {
            "title": "Module 1",
            "description": "Introduction",
            "order": 1
        }
        res = await client.post(f"{BASE_URL}/courses/{course_id}/sections", json=section_data)
        print(f"Create Section: {res.status_code}")
        section = res.json()
        section_id = section["id"]

        # 3. Create Lesson (Item)
        lesson_data = {
            "title": "Lesson 1",
            "content": "<p>This is the first lesson.</p>",
            "type": "lp_lesson",
            "duration": "10 mins",
            "preview": True
        }
        res = await client.post(f"{BASE_URL}/sections/{section_id}/items", json=lesson_data)
        print(f"Create Lesson: {res.status_code}")
        lesson = res.json()

        # 4. Create Quiz (Item)
        quiz_data = {
            "title": "Quiz 1",
            "content": "<p>Quiz description.</p>",
            "type": "lp_quiz",
            "duration": "20 mins",
            "preview": False,
            "passing_grade": 80.0
        }
        res = await client.post(f"{BASE_URL}/sections/{section_id}/items", json=quiz_data)
        print(f"Create Quiz: {res.status_code}")
        quiz = res.json()
        quiz_id = quiz["id"]

        # 5. Add Question
        question_data = {
            "title": "Is this a test?",
            "content": "Select true.",
            "type": "true_or_false",
            "options": [
                {"title": "True", "value": "1", "is_true": True},
                {"title": "False", "value": "0", "is_true": False}
            ]
        }
        res = await client.post(f"{BASE_URL}/quizzes/{quiz_id}/questions", json=question_data)
        print(f"Add Question: {res.status_code}")
        question = res.json()
        question_id = question["id"]

        # 6. Update Question
        update_data = {
            "title": "Is this an UPDATED test?",
            "options": [
                {"title": "Yes", "value": "yes", "is_true": True},
                {"title": "No", "value": "no", "is_true": False}
            ]
        }
        res = await client.put(f"{BASE_URL}/questions/{question_id}", json=update_data)
        print(f"Update Question: {res.status_code}")
        print(json.dumps(res.json(), indent=2))

        # 7. Delete Question
        res = await client.delete(f"{BASE_URL}/questions/{question_id}")
        print(f"Delete Question: {res.status_code}")
        print(res.json())

if __name__ == "__main__":
    asyncio.run(test_endpoints())
