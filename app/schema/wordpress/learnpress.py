from typing import List, Optional, Any, Dict
from pydantic import BaseModel
from datetime import datetime

class LPCourseMetadata(BaseModel):
    price: Optional[float] = None
    duration: Optional[str] = None
    level: Optional[str] = None
    students: Optional[int] = 0
    instructor_name: Optional[str] = None

    class Config:
        from_attributes = True

from app.schema.wordpress.post import WPImageRead

class LPCourse(BaseModel):
    id: int
    title: str
    content: str
    excerpt: str
    slug: str
    date_created: datetime
    status: str
    metadata: LPCourseMetadata
    featured_image: Optional[WPImageRead] = None

    class Config:
        from_attributes = True

class LPItem(BaseModel):
    id: int
    title: str
    type: str  # lp_lesson, lp_quiz
    status: str
    duration: Optional[str] = None
    preview: bool = False
    content: Optional[str] = None  # Added content

class LPSection(BaseModel):
    id: int
    title: str
    order: int
    description: Optional[str] = None
    items: List[LPItem] = []

class LPCurriculum(BaseModel):
    course_id: int
    sections: List[LPSection] = []

class LPQuestionOption(BaseModel):
    value: str
    title: str
    is_true: bool = False

class LPQuestion(BaseModel):
    id: int
    title: str
    content: Optional[str] = None # Added content field
    type: str
    status: str
    options: List[LPQuestionOption] = []

class LPQuiz(BaseModel):
    id: int
    title: str
    content: str
    duration: Optional[str] = None
    passing_grade: Optional[float] = None
    questions: List[LPQuestion] = []

class LPEnrollRequest(BaseModel):
    course_id: int

class LPCompleteItemRequest(BaseModel):
    item_id: int
    course_id: int

class LPQuizSubmission(BaseModel):
    question_id: int
    answer_value: str

class LPQuizSubmitRequest(BaseModel):
    quiz_id: int
    course_id: int
    answers: List[LPQuizSubmission]

class LPCourseCreate(BaseModel):
    title: str
    content: str = ""
    excerpt: str = ""
    status: str = "publish"
    price: float = 0.0
    duration: str = "10 weeks"
    level: str = "Beginner"
    students: int = 0

class LPSectionCreate(BaseModel):
    title: str
    description: str = ""
    order: int = 1

class LPItemCreate(BaseModel):
    title: str
    content: str = ""
    type: str = "lp_lesson" # lp_lesson or lp_quiz
    duration: str = "45 mins"
    preview: bool = False
    passing_grade: float = 0.0 # Only for quizzes

class LPQuestionCreate(BaseModel):
    title: str
    content: str = ""
    type: str = "true_or_false" # true_or_false, multi_choice, single_choice
    options: List[LPQuestionOption]

class LPCourseUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    excerpt: Optional[str] = None
    status: Optional[str] = None
    price: Optional[float] = None
    duration: Optional[str] = None
    level: Optional[str] = None
    students: Optional[int] = None

class LPItemUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    type: Optional[str] = None
    duration: Optional[str] = None
    preview: Optional[bool] = None
    passing_grade: Optional[float] = None

class LPSectionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None

class LPQuestionUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    type: Optional[str] = None
    options: Optional[List[LPQuestionOption]] = None

# --- Reporting Schemas ---

class LPLearner(BaseModel):
    user_id: int
    username: str
    display_name: str
    email: Optional[str] = None
    enrollment_date: Optional[datetime] = None
    status: str
    graduation: Optional[str] = None
    progress_percent: float = 0.0

class LPQuizResultDetail(BaseModel):
    user_mark: float
    question_count: int
    user_score: float
    passing_grade: float
    passed: bool
    questions: List[Dict[str, Any]] = []

class LPQuizSubmissionRead(BaseModel):
    user_item_id: int
    user_id: int
    user_display_name: str
    quiz_id: int
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: str
    graduation: str
    results: Optional[LPQuizResultDetail] = None

class LPCourseStats(BaseModel):
    total_students: int
    completed_students: int
    in_progress_students: int
    passing_rate: float
    average_quiz_score: float
