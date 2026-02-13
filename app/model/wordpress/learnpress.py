"""
LearnPress LMS database models.
Maps to tables with prefix 8jH_learnpress_*
"""
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class LPSection(SQLModel, table=True):
    """LearnPress sections (8jH_learnpress_sections)"""
    __tablename__ = "8jH_learnpress_sections"

    section_id: Optional[int] = Field(default=None, primary_key=True)
    section_name: str = Field(max_length=255, default="")
    section_course_id: int = Field(default=0)
    section_order: int = Field(default=1)
    section_description: str = Field(default="")


class LPSectionItem(SQLModel, table=True):
    """LearnPress section items (8jH_learnpress_section_items)"""
    __tablename__ = "8jH_learnpress_section_items"

    section_item_id: Optional[int] = Field(default=None, primary_key=True)
    section_id: int = Field(default=0, foreign_key="8jH_learnpress_sections.section_id")
    item_id: int = Field(default=0)
    item_order: int = Field(default=0)
    item_type: Optional[str] = Field(default=None, max_length=45)


class LPQuizQuestion(SQLModel, table=True):
    """LearnPress quiz questions (8jH_learnpress_quiz_questions)"""
    __tablename__ = "8jH_learnpress_quiz_questions"

    quiz_question_id: Optional[int] = Field(default=None, primary_key=True)
    quiz_id: int = Field(default=0)
    question_id: int = Field(default=0)
    question_order: int = Field(default=1)


class LPQuestionAnswer(SQLModel, table=True):
    """LearnPress question answers (8jH_learnpress_question_answers)"""
    __tablename__ = "8jH_learnpress_question_answers"

    question_answer_id: Optional[int] = Field(default=None, primary_key=True)
    question_id: int = Field(default=0)
    title: str = Field(default="")
    value: str = Field(max_length=32, default="")
    order: int = Field(default=1)
    is_true: Optional[str] = Field(default=None, max_length=3)


class LPQuestionAnswerMeta(SQLModel, table=True):
    """LearnPress question answer meta (8jH_learnpress_question_answermeta)"""
    __tablename__ = "8jH_learnpress_question_answermeta"

    meta_id: Optional[int] = Field(default=None, primary_key=True)
    learnpress_question_answer_id: int = Field(foreign_key="8jH_learnpress_question_answers.question_answer_id")
    meta_key: str = Field(max_length=255, default="")
    meta_value: Optional[str] = Field(default=None)


class LPUserItem(SQLModel, table=True):
    """LearnPress user items (8jH_learnpress_user_items)"""
    __tablename__ = "8jH_learnpress_user_items"

    user_item_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=0, foreign_key="8jH_users.ID")
    item_id: int = Field(default=0)
    start_time: Optional[datetime] = Field(default=None)
    end_time: Optional[datetime] = Field(default=None)
    item_type: str = Field(max_length=45, default="")
    status: str = Field(max_length=45, default="")
    graduation: Optional[str] = Field(default=None, max_length=20)
    access_level: int = Field(default=50)
    ref_id: int = Field(default=0)
    ref_type: Optional[str] = Field(default="", max_length=45)
    parent_id: int = Field(default=0)


class LPUserItemMeta(SQLModel, table=True):
    """LearnPress user item meta (8jH_learnpress_user_itemmeta)"""
    __tablename__ = "8jH_learnpress_user_itemmeta"

    meta_id: Optional[int] = Field(default=None, primary_key=True)
    learnpress_user_item_id: int = Field(foreign_key="8jH_learnpress_user_items.user_item_id")
    meta_key: str = Field(max_length=255, default="")
    meta_value: Optional[str] = Field(default=None)
    extra_value: Optional[str] = Field(default=None)


class LPUserItemResult(SQLModel, table=True):
    """LearnPress user item results (8jH_learnpress_user_item_results)"""
    __tablename__ = "8jH_learnpress_user_item_results"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_item_id: int = Field(foreign_key="8jH_learnpress_user_items.user_item_id")
    result: Optional[str] = Field(default=None)


class LPOrderItem(SQLModel, table=True):
    """LearnPress order items (8jH_learnpress_order_items)"""
    __tablename__ = "8jH_learnpress_order_items"

    order_item_id: Optional[int] = Field(default=None, primary_key=True)
    order_item_name: str = Field(default="")
    order_id: int = Field(default=0)
    item_id: int = Field(default=0)
    item_type: str = Field(max_length=45, default="")


class LPOrderItemMeta(SQLModel, table=True):
    """LearnPress order item meta (8jH_learnpress_order_itemmeta)"""
    __tablename__ = "8jH_learnpress_order_itemmeta"

    meta_id: Optional[int] = Field(default=None, primary_key=True)
    learnpress_order_item_id: int = Field(default=0, foreign_key="8jH_learnpress_order_items.order_item_id")
    meta_key: str = Field(max_length=255, default="")
    meta_value: Optional[str] = Field(default=None)
    extra_value: Optional[str] = Field(default=None)


class LPSession(SQLModel, table=True):
    """LearnPress sessions (8jH_learnpress_sessions)"""
    __tablename__ = "8jH_learnpress_sessions"

    session_id: int = Field(primary_key=True)
    session_key: str = Field(max_length=32, default="")
    session_value: str = Field(default="")
    session_expiry: int = Field(default=0)


class LPReviewLog(SQLModel, table=True):
    """LearnPress review logs (8jH_learnpress_review_logs)"""
    __tablename__ = "8jH_learnpress_review_logs"

    review_log_id: Optional[int] = Field(default=None, primary_key=True)
    course_id: int = Field(default=0)
    user_id: int = Field(default=0, foreign_key="8jH_users.ID")
    message: str = Field(default="")
    date: Optional[datetime] = Field(default=None)
    status: str = Field(max_length=45, default="")
    user_type: str = Field(max_length=45, default="")
