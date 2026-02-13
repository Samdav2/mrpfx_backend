from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db.session import get_session
from app.dependencies.auth import get_current_user
from app.model.user import User
from app.repo.wordpress.learnpress import LPCourseRepository
from app.schema.wordpress.learnpress import (
    LPCourse, LPCourseCreate, LPCourseUpdate,
    LPSectionCreate, LPSection as SchemaLPSection,
    LPItemCreate, LPItem, LPItemUpdate,
    LPQuestionCreate, LPQuestion,
    LPCurriculum, LPQuiz,
    LPSectionUpdate, LPQuestionUpdate,
    LPLearner, LPCourseStats, LPQuizSubmissionRead
)

router = APIRouter()

@router.post("/courses", response_model=LPCourse)
async def create_course(
    data: LPCourseCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    repo = LPCourseRepository(session)
    return await repo.create_course(user_id=current_user.ID, data=data)

@router.post("/courses/{course_id}/sections", response_model=SchemaLPSection)
async def create_section(
    course_id: int,
    data: LPSectionCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    repo = LPCourseRepository(session)
    # Verify course exists
    course = await repo.get_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    return await repo.create_section(course_id=course_id, data=data)

@router.post("/sections/{section_id}/items", response_model=LPItem)
async def create_item(
    section_id: int,
    data: LPItemCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    repo = LPCourseRepository(session)
    # Note: We might want to verify section exists, but repo will handle FK constraints or we can add a check
    return await repo.create_item(section_id=section_id, data=data)

@router.post("/quizzes/{quiz_id}/questions", response_model=LPQuestion)
async def add_question_to_quiz(
    quiz_id: int,
    data: LPQuestionCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    repo = LPCourseRepository(session)
    # Verify quiz exists
    quiz = await repo.get_quiz(quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    return await repo.add_question_to_quiz(quiz_id=quiz_id, data=data)

@router.put("/courses/{course_id}", response_model=LPCourse)
async def update_course(
    course_id: int,
    data: LPCourseUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    repo = LPCourseRepository(session)
    course = await repo.update_course(course_id=course_id, data=data)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.delete("/courses/{course_id}")
async def delete_course(
    course_id: int,
    force: bool = False,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    repo = LPCourseRepository(session)
    success = await repo.delete_course(course_id=course_id, force=force)
    if not success:
        raise HTTPException(status_code=404, detail="Course not found")

    msg = "Course permanently deleted" if force else "Course moved to trash"
    return {"status": "success", "message": msg}

@router.put("/items/{item_id}", response_model=LPItem)
async def update_item(
    item_id: int,
    data: LPItemUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    repo = LPCourseRepository(session)
    item = await repo.update_item(item_id=item_id, data=data)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.delete("/items/{item_id}")
async def delete_item(
    item_id: int,
    force: bool = False,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    repo = LPCourseRepository(session)
    success = await repo.delete_item(item_id=item_id, force=force)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")

    msg = "Item permanently deleted" if force else "Item moved to trash"
    return {"status": "success", "message": msg}

@router.get("/courses", response_model=List[LPCourse])
async def get_courses(
    limit: int = 10,
    offset: int = 0,
    status: str = "publish",
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    repo = LPCourseRepository(session)
    return await repo.get_courses(limit=limit, offset=offset, status=status)

@router.get("/courses/{course_id}", response_model=LPCourse)
async def get_course(
    course_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    repo = LPCourseRepository(session)
    course = await repo.get_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.get("/courses/{course_id}/curriculum", response_model=LPCurriculum)
async def get_curriculum(
    course_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    repo = LPCourseRepository(session)
    # Check course exists? optional but good practice
    course = await repo.get_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    return await repo.get_curriculum(course_id)

@router.get("/quizzes/{quiz_id}", response_model=LPQuiz)
async def get_quiz(
    quiz_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    repo = LPCourseRepository(session)
    quiz = await repo.get_quiz(quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz

@router.put("/sections/{section_id}", response_model=SchemaLPSection)
async def update_section(
    section_id: int,
    data: LPSectionUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    repo = LPCourseRepository(session)
    section = await repo.update_section(section_id, data)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    return section

@router.delete("/sections/{section_id}")
async def delete_section(
    section_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    repo = LPCourseRepository(session)
    success = await repo.delete_section(section_id)
    if not success:
        raise HTTPException(status_code=404, detail="Section not found")
    return {"status": "success", "message": "Section deleted"}

@router.put("/questions/{question_id}", response_model=LPQuestion)
async def update_question(
    question_id: int,
    data: LPQuestionUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    repo = LPCourseRepository(session)
    question = await repo.update_question(question_id, data)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@router.delete("/questions/{question_id}")
async def delete_question(
    question_id: int,
    force: bool = False,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    repo = LPCourseRepository(session)
    success = await repo.delete_question(question_id, force=force)
    if not success:
        raise HTTPException(status_code=404, detail="Question not found")

    msg = "Question permanently deleted" if force else "Question moved to trash"
    return {"status": "success", "message": msg}


# --- Reporting Endpoints ---

@router.get("/courses/{course_id}/learners", response_model=List[LPLearner])
async def get_course_learners(
    course_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """List all students enrolled in a course with their progress"""
    repo = LPCourseRepository(session)
    return await repo.get_course_learners(course_id)


@router.get("/courses/{course_id}/stats", response_model=LPCourseStats)
async def get_course_stats(
    course_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get aggregate performance statistics for a course"""
    repo = LPCourseRepository(session)
    return await repo.get_course_stats(course_id)


@router.get("/quizzes/{quiz_id}/submissions", response_model=List[LPQuizSubmissionRead])
async def get_quiz_submissions(
    quiz_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """List all student attempts for a specific quiz"""
    repo = LPUserItemRepository(session)
    return await repo.get_quiz_submissions(quiz_id)


@router.get("/submissions/{submission_id}", response_model=LPQuizSubmissionRead)
async def get_submission_details(
    submission_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get detailed results for a specific quiz submission"""
    repo = LPUserItemRepository(session)
    submission = await repo.get_quiz_submission_details(submission_id)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    return submission
