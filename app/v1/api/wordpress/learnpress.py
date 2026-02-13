from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.db.session import get_session
from app.repo.wordpress.learnpress import LPCourseRepository, LPUserItemRepository
from app.model.wordpress.core import WPPost
from app.model.wordpress.learnpress import LPUserItem
from app.dependencies.auth import get_current_user
from app.model.user import User

router = APIRouter()

from app.schema.wordpress.learnpress import (
    LPCourse, LPCurriculum, LPQuiz, LPSection, LPItem, LPQuestion,
    LPEnrollRequest, LPCompleteItemRequest, LPQuizSubmitRequest,
    LPCourseCreate, LPCourseUpdate, LPSectionCreate, LPSectionUpdate,
    LPItemCreate, LPItemUpdate, LPQuestionCreate, LPQuestionUpdate,
    LPLearner, LPQuizSubmissionRead, LPCourseStats
)

@router.get("/courses", response_model=List[LPCourse])
async def get_courses(
    skip: int = 0,
    limit: int = 10,
    status: str = "publish",
    session: Session = Depends(get_session)
):
    repo = LPCourseRepository(session)
    return await repo.get_courses(limit=limit, offset=skip, status=status)

@router.get("/courses/{course_id}", response_model=LPCourse)
async def get_course(
    course_id: int,
    session: Session = Depends(get_session)
):
    repo = LPCourseRepository(session)
    course = await repo.get_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.get("/courses/{course_id}/curriculum", response_model=LPCurriculum)
async def get_course_curriculum(
    course_id: int,
    session: Session = Depends(get_session)
):
    repo = LPCourseRepository(session)
    return await repo.get_curriculum(course_id)

@router.get("/quizzes/{quiz_id}", response_model=LPQuiz)
async def get_quiz(
    quiz_id: int,
    session: Session = Depends(get_session)
):
    repo = LPCourseRepository(session)
    quiz = await repo.get_quiz(quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz

@router.get("/my-courses", response_model=List[LPUserItem])
async def get_my_courses(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    repo = LPUserItemRepository(session)
    # Assuming current_user.ID maps to WP user ID. If not, we need a mapping.
    # For now, we'll assume they are synced or the same.
    return await repo.get_user_items(user_id=current_user.ID)

@router.get("/progress/{course_id}", response_model=LPUserItem)
async def get_course_progress(
    course_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    repo = LPUserItemRepository(session)
    progress = await repo.get_course_progress(user_id=current_user.ID, course_id=course_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found for this course")
    return progress

@router.post("/courses/{course_id}/enroll", response_model=LPUserItem)
async def enroll_course(
    course_id: int,
    request: LPEnrollRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if request.course_id != course_id:
        raise HTTPException(status_code=400, detail="Course ID mismatch")

    repo = LPCourseRepository(session)
    return await repo.enroll_course(user_id=current_user.ID, course_id=course_id)

@router.post("/items/{item_id}/complete", response_model=LPUserItem)
async def complete_item(
    item_id: int,
    request: LPCompleteItemRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if request.item_id != item_id:
        raise HTTPException(status_code=400, detail="Item ID mismatch")

    repo = LPCourseRepository(session)
    try:
        return await repo.complete_item(
            user_id=current_user.ID,
            course_id=request.course_id,
            item_id=item_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/quizzes/{quiz_id}/submit", response_model=LPUserItem)
async def submit_quiz(
    quiz_id: int,
    request: LPQuizSubmitRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if request.quiz_id != quiz_id:
        raise HTTPException(status_code=400, detail="Quiz ID mismatch")

    repo = LPCourseRepository(session)
    try:
        # Convert Pydantic models to dicts for repo
        answers_dict = [a.dict() for a in request.answers]
        return await repo.submit_quiz(
            user_id=current_user.ID,
            course_id=request.course_id,
            quiz_id=quiz_id,
            answers=answers_dict
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/my-progress/{course_id}", response_model=LPLearner)
async def get_my_detailed_progress(
    course_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get detailed progress for the current user in a specific course"""
    repo = LPCourseRepository(session)
    learners = await repo.get_course_learners(course_id)
    # Find current user in the learners list
    me = next((l for l in learners if l.user_id == current_user.ID), None)
    if not me:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return me


@router.get("/quizzes/{quiz_id}/my-results", response_model=List[LPQuizSubmissionRead])
async def get_my_quiz_results(
    quiz_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all attempts and results for the current user for a specific quiz"""
    repo = LPUserItemRepository(session)
    return await repo.get_quiz_submissions(quiz_id=quiz_id, user_id=current_user.ID)



# ============== ADMIN CRUD ENDPOINTS ==============

# --- Course CRUD ---

@router.post("/courses", response_model=LPCourse)
async def create_course(
    course_data: LPCourseCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new LearnPress course"""
    repo = LPCourseRepository(session)
    return await repo.create_course(user_id=current_user.ID, data=course_data)


@router.put("/courses/{course_id}", response_model=LPCourse)
async def update_course(
    course_id: int,
    course_data: LPCourseUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    repo = LPCourseRepository(session)
    course = await repo.update_course(course_id, course_data)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.get("/courses/{course_id}/thumbnail")
async def get_course_thumbnail(
    course_id: int,
    session: Session = Depends(get_session)
):
    """Get the course thumbnail (featured image)"""
    repo = LPCourseRepository(session)
    image = await repo.get_course_thumbnail(course_id)
    if not image:
        raise HTTPException(status_code=404, detail="No thumbnail set")
    return image


@router.put("/courses/{course_id}/thumbnail")
async def set_course_thumbnail(
    course_id: int,
    attachment_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Set the course thumbnail (featured image)"""
    repo = LPCourseRepository(session)
    success = await repo.set_course_thumbnail(course_id, attachment_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to set thumbnail")
    return {"message": "Thumbnail set successfully"}


@router.delete("/courses/{course_id}/thumbnail")
async def remove_course_thumbnail(
    course_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Remove the course thumbnail"""
    from app.repo.wordpress.posts import WPPostRepository
    repo = WPPostRepository(session)
    # Using post repo directly for removal as it's just meta
    # But ideally should be in LPCourseRepository if we want strict encapsulation
    # For now, let's reuse valid WP post logic
    success = await repo.remove_featured_image(course_id)
    if not success:
        raise HTTPException(status_code=404, detail="No thumbnail to remove")
    return {"message": "Thumbnail removed successfully"}



@router.delete("/courses/{course_id}")
async def delete_course(
    course_id: int,
    force: bool = False,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete (trash) or permanently delete a LearnPress course"""
    repo = LPCourseRepository(session)
    success = await repo.delete_course(course_id, force=force)
    if not success:
        raise HTTPException(status_code=404, detail="Course not found")
    return {"message": "Course deleted successfully"}


# --- Section CRUD ---

@router.post("/courses/{course_id}/sections", response_model=LPSection)
async def create_section(
    course_id: int,
    section_data: LPSectionCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new section in a course"""
    repo = LPCourseRepository(session)
    return await repo.create_section(course_id, section_data)


@router.put("/sections/{section_id}", response_model=LPSection)
async def update_section(
    section_id: int,
    section_data: LPSectionUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update an existing section"""
    repo = LPCourseRepository(session)
    section = await repo.update_section(section_id, section_data)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    return section


@router.delete("/sections/{section_id}")
async def delete_section(
    section_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a section"""
    repo = LPCourseRepository(session)
    success = await repo.delete_section(section_id)
    if not success:
        raise HTTPException(status_code=404, detail="Section not found")
    return {"message": "Section deleted successfully"}


# --- Item (Lesson/Quiz) CRUD ---

@router.post("/sections/{section_id}/items", response_model=LPItem)
async def create_item(
    section_id: int,
    item_data: LPItemCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new item (lesson or quiz) in a section"""
    repo = LPCourseRepository(session)
    return await repo.create_item(section_id, item_data)


@router.put("/items/{item_id}", response_model=LPItem)
async def update_item(
    item_id: int,
    item_data: LPItemUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update an existing item (lesson or quiz)"""
    repo = LPCourseRepository(session)
    item = await repo.update_item(item_id, item_data)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.delete("/items/{item_id}")
async def delete_item(
    item_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete (trash) an item"""
    repo = LPCourseRepository(session)
    success = await repo.delete_item(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}


# --- Question CRUD ---

@router.post("/quizzes/{quiz_id}/questions", response_model=LPQuestion)
async def create_question(
    quiz_id: int,
    question_data: LPQuestionCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Add a question to a quiz"""
    repo = LPCourseRepository(session)
    return await repo.add_question_to_quiz(quiz_id, question_data)


@router.put("/questions/{question_id}", response_model=LPQuestion)
async def update_question(
    question_id: int,
    question_data: LPQuestionUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update an existing question"""
    repo = LPCourseRepository(session)
    question = await repo.update_question(question_id, question_data)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@router.delete("/questions/{question_id}")
async def delete_question(
    question_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a question"""
    repo = LPCourseRepository(session)
    success = await repo.delete_question(question_id)
    if not success:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"message": "Question deleted successfully"}
