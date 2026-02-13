import asyncio
import httpx
import json

BASE_URL = "http://localhost:8000/api/v1/admin/learnpress"

async def test_duplication():
    async with httpx.AsyncClient() as client:
        # 0. Setup: Create Course, Section, Quiz
        print("Setting up dependencies...")
        # Course
        res = await client.post(f"{BASE_URL}/courses", json={"title": "Debug Course", "content": "Debug", "excerpt": "", "status": "publish", "price": 0, "duration": "10h", "level": "All", "students": 0})
        course_id = res.json()["id"]
        # Section
        res = await client.post(f"{BASE_URL}/courses/{course_id}/sections", json={"title": "Debug Section", "description": "", "order": 1})
        section_id = res.json()["id"]
        # Quiz
        res = await client.post(f"{BASE_URL}/sections/{section_id}/items", json={"title": "Debug Quiz", "content": "", "type": "lp_quiz", "duration": "10m", "preview": False, "passing_grade": 0})
        quiz_id = res.json()["id"]
        print(f"Setup Complete. Quiz ID: {quiz_id}")

        # 1. Create a Question
        print("Creating Question...")
        question_data = {
            "title": "Duplication Test Question",
            "content": "Test content",
            "type": "true_or_false",
            "options": [
                {"title": "True", "value": "1", "is_true": True},
                {"title": "False", "value": "0", "is_true": False}
            ]
        }
        res = await client.post(f"{BASE_URL}/quizzes/{quiz_id}/questions", json=question_data)
        if res.status_code != 200:
            print(f"Failed to create: {res.text}")
            return

        q_id = res.json()["id"]
        print(f"Created Question ID: {q_id}")
        print(f"Initial Options Count: {len(res.json()['options'])}")

        # 2. Update the Question (should replace options)
        print("Updating Question...")
        update_data = {
            "title": "Duplication Test Question Updated",
            "type": "true_or_false",
            "options": [
                {"title": "True", "value": "1", "is_true": True},
                {"title": "False", "value": "0", "is_true": False}
            ]
        }
        res = await client.put(f"{BASE_URL}/questions/{q_id}", json=update_data)
        if res.status_code != 200:
            print(f"Failed to update: {res.text}")
            return

        updated_q = res.json()
        print(f"Updated Question ID: {updated_q['id']}")
        print(f"Updated Options Count: {len(updated_q['options'])}")

        for opt in updated_q['options']:
            print(f" - {opt['title']} (True: {opt['is_true']})")

        if len(updated_q['options']) > 2:
            print("BUG DETECTED: Duplicate options found!")
        else:
            print("SUCCESS: Options replaced correctly.")

        # 3. Cleanup
        await client.delete(f"{BASE_URL}/questions/{q_id}")

if __name__ == "__main__":
    asyncio.run(test_duplication())
