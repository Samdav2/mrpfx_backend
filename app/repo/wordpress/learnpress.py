from typing import List, Optional, Dict, Any
import json
from datetime import datetime
from sqlmodel import select, col
from sqlmodel.ext.asyncio.session import AsyncSession
from app.model.wordpress.learnpress import (
    LPUserItem, LPUserItemMeta, LPOrderItem, LPOrderItemMeta,
    LPSection, LPSectionItem, LPQuizQuestion, LPQuestionAnswer,
    LPUserItemResult
)
from app.model.wordpress.core import WPPost, WPPostMeta, WPUser
from app.schema.wordpress.learnpress import (
    LPCourse, LPCourseMetadata, LPCurriculum, LPSection as SchemaLPSection,
    LPItem, LPQuiz, LPQuestion, LPQuestionOption,
    LPSectionUpdate, LPQuestionUpdate,
    LPLearner, LPQuizSubmissionRead, LPQuizResultDetail, LPCourseStats
)

class LPCourseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _get_user_display_name(self, user_id: int) -> str:
        stmt = select(WPUser).where(WPUser.ID == user_id)
        result = await self.session.exec(stmt)
        user = result.first()
        return user.display_name if user else ""

    async def get_course(self, course_id: int) -> Optional[LPCourse]:
        # Fetch course post
        statement = select(WPPost).where(
            WPPost.ID == course_id,
            WPPost.post_type == "lp_course"
        )
        result = await self.session.exec(statement)
        post = result.first()

        if not post:
            return None

        # Fetch metadata
        meta_stmt = select(WPPostMeta).where(WPPostMeta.post_id == course_id)
        meta_result = await self.session.exec(meta_stmt)
        meta_items = meta_result.all()

        meta_dict = {item.meta_key: item.meta_value for item in meta_items}

        instructor_name = await self._get_user_display_name(post.post_author)

        metadata = LPCourseMetadata(
            price=float(meta_dict.get("_lp_price", 0) or 0),
            duration=meta_dict.get("_lp_duration", ""),
            level=meta_dict.get("_lp_level", ""),
            students=int(meta_dict.get("_lp_students", 0) or 0),
            instructor_name=instructor_name
        )

        course = LPCourse(
            id=post.ID,
            title=post.post_title,
            content=post.post_content,
            excerpt=post.post_excerpt,
            slug=post.post_name,
            date_created=post.post_date,
            status=post.post_status,
            metadata=metadata
        )

        # Attach featured image
        thumb = await self.get_course_thumbnail(course_id)
        if thumb:
            from app.schema.wordpress.post import WPImageRead
            course.featured_image = WPImageRead(**thumb)

        return course

    async def get_courses(self, limit: int = 10, offset: int = 0, status: str = "publish") -> List[LPCourse]:
        statement = select(WPPost).where(
            WPPost.post_type == "lp_course"
        )

        if status != "any":
            statement = statement.where(WPPost.post_status == status)

        statement = statement.limit(limit).offset(offset)
        result = await self.session.exec(statement)
        posts = result.all()

        courses = []
        for post in posts:
            # Fetch essential metadata for list view
            # Optimization: Could fetch all meta in one query if needed, but for now per-course is okay for small limits
            meta_stmt = select(WPPostMeta).where(WPPostMeta.post_id == post.ID)
            meta_result = await self.session.exec(meta_stmt)
            meta_items = meta_result.all()
            meta_dict = {item.meta_key: item.meta_value for item in meta_items}

            instructor_name = await self._get_user_display_name(post.post_author)

            metadata = LPCourseMetadata(
                price=float(meta_dict.get("_lp_price", 0) or 0),
                duration=meta_dict.get("_lp_duration", ""),
                level=meta_dict.get("_lp_level", ""),
                students=int(meta_dict.get("_lp_students", 0) or 0),
                instructor_name=instructor_name
            )

            course = LPCourse(
                id=post.ID,
                title=post.post_title,
                content=post.post_content,
                excerpt=post.post_excerpt,
                slug=post.post_name,
                date_created=post.post_date,
                status=post.post_status,
                metadata=metadata
            )

            # Attach featured image
            thumb = await self.get_course_thumbnail(post.ID)
            if thumb:
                from app.schema.wordpress.post import WPImageRead
                course.featured_image = WPImageRead(**thumb)

            courses.append(course)
        return courses

    async def get_curriculum(self, course_id: int) -> LPCurriculum:
        # Fetch sections
        stmt = select(LPSection).where(LPSection.section_course_id == course_id).order_by(LPSection.section_order)
        result = await self.session.exec(stmt)
        sections = result.all()

        schema_sections = []
        for section in sections:
            # Fetch items for this section
            item_stmt = select(LPSectionItem).where(
                LPSectionItem.section_id == section.section_id
            ).order_by(LPSectionItem.item_order)
            item_result = await self.session.exec(item_stmt)
            section_items = item_result.all()

            items = []
            for si in section_items:
                # Fetch item details (Post)
                post_stmt = select(WPPost).where(WPPost.ID == si.item_id)
                post_result = await self.session.exec(post_stmt)
                post = post_result.first()

                if post:
                    # Fetch item meta
                    meta_stmt = select(WPPostMeta).where(WPPostMeta.post_id == post.ID)
                    meta_result = await self.session.exec(meta_stmt)
                    meta_items = meta_result.all()
                    meta_dict = {item.meta_key: item.meta_value for item in meta_items}

                    items.append(LPItem(
                        id=post.ID,
                        title=post.post_title,
                        type=post.post_type, # lp_lesson or lp_quiz
                        status=post.post_status,
                        duration=meta_dict.get("_lp_duration", ""),
                        preview=(meta_dict.get("_lp_preview") == "yes"),
                        content=post.post_content
                    ))

            schema_sections.append(SchemaLPSection(
                id=section.section_id,
                title=section.section_name,
                order=section.section_order,
                description=section.section_description,
                items=items
            ))

        return LPCurriculum(course_id=course_id, sections=schema_sections)

    async def get_quiz(self, quiz_id: int) -> Optional[LPQuiz]:
        # Fetch quiz post
        stmt = select(WPPost).where(WPPost.ID == quiz_id, WPPost.post_type == "lp_quiz")
        result = await self.session.exec(stmt)
        post = result.first()

        if not post:
            return None

        # Fetch quiz meta
        meta_stmt = select(WPPostMeta).where(WPPostMeta.post_id == quiz_id)
        meta_result = await self.session.exec(meta_stmt)
        meta_items = meta_result.all()
        meta_dict = {item.meta_key: item.meta_value for item in meta_items}

        # Fetch questions
        q_stmt = select(LPQuizQuestion).where(LPQuizQuestion.quiz_id == quiz_id).order_by(LPQuizQuestion.question_order)
        q_result = await self.session.exec(q_stmt)
        quiz_questions = q_result.all()

        questions = []
        for qq in quiz_questions:
            # Fetch question post
            qp_stmt = select(WPPost).where(WPPost.ID == qq.question_id)
            qp_result = await self.session.exec(qp_stmt)
            qp = qp_result.first()

            if qp:
                # Fetch answers
                a_stmt = select(LPQuestionAnswer).where(
                    LPQuestionAnswer.question_id == qq.question_id
                ).order_by(LPQuestionAnswer.order)
                a_result = await self.session.exec(a_stmt)
                answers = a_result.all()

                options = [
                    LPQuestionOption(
                        value=a.value,
                        title=a.title,
                        is_true=(a.is_true == "yes")
                    ) for a in answers
                ]

                questions.append(LPQuestion(
                    id=qp.ID,
                    title=qp.post_title,
                    content=qp.post_content,
                    type=qp.post_type, # lp_question
                    status=qp.post_status,
                    options=options
                ))

        return LPQuiz(
            id=post.ID,
            title=post.post_title,
            content=post.post_content,
            duration=meta_dict.get("_lp_duration", ""),
            passing_grade=float(meta_dict.get("_lp_passing_grade", 0) or 0),
            questions=questions
        )

    async def enroll_course(self, user_id: int, course_id: int) -> LPUserItem:
        # Check if already enrolled
        stmt = select(LPUserItem).where(
            LPUserItem.user_id == user_id,
            LPUserItem.item_id == course_id,
            LPUserItem.item_type == "lp_course"
        )
        result = await self.session.exec(stmt)
        existing = result.first()

        if existing:
            return existing

        # Create new enrollment
        new_item = LPUserItem(
            user_id=user_id,
            item_id=course_id,
            start_time=datetime.now(),
            item_type="lp_course",
            status="enrolled",
            graduation="in-progress",
            access_level=50
        )
        self.session.add(new_item)
        await self.session.commit()
        await self.session.refresh(new_item)
        return new_item

    async def complete_item(self, user_id: int, course_id: int, item_id: int) -> LPUserItem:
        # Check if enrolled in course
        course_stmt = select(LPUserItem).where(
            LPUserItem.user_id == user_id,
            LPUserItem.item_id == course_id,
            LPUserItem.item_type == "lp_course"
        )
        course_result = await self.session.exec(course_stmt)
        course_item = course_result.first()

        if not course_item:
            raise ValueError("User not enrolled in course")

        # Check if item entry exists
        stmt = select(LPUserItem).where(
            LPUserItem.user_id == user_id,
            LPUserItem.item_id == item_id,
            LPUserItem.ref_id == course_id
        )
        result = await self.session.exec(stmt)
        item = result.first()

        if not item:
            item = LPUserItem(
                user_id=user_id,
                item_id=item_id,
                ref_id=course_id,
                item_type="lp_lesson",
                status="completed",
                graduation="passed",
                start_time=datetime.now(),
                end_time=datetime.now()
            )
            self.session.add(item)
        else:
            item.status = "completed"
            item.graduation = "passed"
            item.end_time = datetime.now()

        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def submit_quiz(self, user_id: int, course_id: int, quiz_id: int, answers: List[Dict[str, Any]]) -> LPUserItem:
        # Check enrollment
        course_stmt = select(LPUserItem).where(
            LPUserItem.user_id == user_id,
            LPUserItem.item_id == course_id,
            LPUserItem.item_type == "lp_course"
        )
        course_result = await self.session.exec(course_stmt)
        course_item = course_result.first()

        if not course_item:
            raise ValueError("User not enrolled in course")

        # Fetch quiz to get correct answers and passing grade
        quiz = await self.get_quiz(quiz_id)
        if not quiz:
            raise ValueError("Quiz not found")

        # Calculate score
        correct_count = 0
        total_questions = len(quiz.questions)

        for q in quiz.questions:
            # Find submitted answer for this question
            submitted = next((a for a in answers if a.get("question_id") == q.id), None)
            if submitted:
                submitted_val = submitted.get("answer_value")
                # Find correct option
                correct_option = next((o for o in q.options if o.is_true), None)
                if correct_option and correct_option.value == submitted_val:
                    correct_count += 1

        score_percent = (correct_count / total_questions * 100) if total_questions > 0 else 0
        passed = score_percent >= (quiz.passing_grade or 0)

        graduation = "passed" if passed else "failed"
        status = "completed"

        # Create/Update quiz attempt (LPUserItem)
        stmt = select(LPUserItem).where(
            LPUserItem.user_id == user_id,
            LPUserItem.item_id == quiz_id,
            LPUserItem.ref_id == course_id
        )
        result = await self.session.exec(stmt)
        item = result.first()

        if not item:
            item = LPUserItem(
                user_id=user_id,
                item_id=quiz_id,
                ref_id=course_id,
                item_type="lp_quiz",
                status=status,
                graduation=graduation,
                start_time=datetime.now(),
                end_time=datetime.now()
            )
            self.session.add(item)
            await self.session.commit()
            await self.session.refresh(item)
        else:
            item.status = status
            item.graduation = graduation
            item.end_time = datetime.now()
            self.session.add(item)
            await self.session.commit()
            await self.session.refresh(item)

        # Save results (LPUserItemResult)
        result_data = {
            "questions": answers,
            "results": {
                "user_mark": correct_count,
                "question_count": total_questions,
                "user_score": score_percent,
                "passing_grade": quiz.passing_grade,
                "passed": passed
            }
        }

        # Check if result exists
        res_stmt = select(LPUserItemResult).where(LPUserItemResult.user_item_id == item.user_item_id)
        res_result = await self.session.exec(res_stmt)
        user_result = res_result.first()

        if not user_result:
            user_result = LPUserItemResult(
                user_item_id=item.user_item_id,
                result=json.dumps(result_data)
            )
            self.session.add(user_result)
        else:
            user_result.result = json.dumps(result_data)
            self.session.add(user_result)

        await self.session.commit()
        await self.session.refresh(item)

        return item

    async def create_course(self, user_id: int, data: Any) -> LPCourse:
        # Create Post
        new_post = WPPost(
            post_author=user_id,
            post_title=data.title,
            post_content=data.content,
            post_excerpt=data.excerpt,
            post_status=data.status,
            post_type="lp_course",
            post_name=data.title.lower().replace(" ", "-"), # Simple slug generation
            post_date=datetime.now(),
            post_date_gmt=datetime.now(),
            post_modified=datetime.now(),
            post_modified_gmt=datetime.now()
        )
        self.session.add(new_post)
        await self.session.commit()
        await self.session.refresh(new_post)

        # Add Meta
        meta_data = {
            "_lp_price": str(data.price),
            "_lp_duration": data.duration,
            "_lp_level": data.level,
            "_lp_students": str(data.students),
            "_lp_retake_count": "0"
        }

        for key, value in meta_data.items():
            meta = WPPostMeta(
                post_id=new_post.ID,
                meta_key=key,
                meta_value=value
            )
            self.session.add(meta)

        course_id = new_post.ID
        await self.session.commit()

        return await self.get_course(course_id)

    async def create_section(self, course_id: int, data: Any) -> SchemaLPSection:
        # Create Section
        new_section = LPSection(
            section_course_id=course_id,
            section_name=data.title,
            section_description=data.description,
            section_order=data.order
        )
        self.session.add(new_section)
        await self.session.commit()
        await self.session.refresh(new_section)

        return SchemaLPSection(
            id=new_section.section_id,
            title=new_section.section_name,
            order=new_section.section_order,
            description=new_section.section_description,
            items=[]
        )

    async def create_item(self, section_id: int, data: Any) -> LPItem:
        # Create Item Post (Lesson or Quiz)
        new_post = WPPost(
            post_author=1, # Default admin or passed user
            post_title=data.title,
            post_content=data.content,
            post_status="publish",
            post_type=data.type,
            post_name=data.title.lower().replace(" ", "-"),
            post_date=datetime.now(),
            post_date_gmt=datetime.now(),
            post_modified=datetime.now(),
            post_modified_gmt=datetime.now()
        )
        self.session.add(new_post)
        await self.session.commit()
        await self.session.refresh(new_post)

        # Add Item Meta
        meta_data = {
            "_lp_duration": data.duration,
            "_lp_preview": "yes" if data.preview else "no"
        }

        if data.type == "lp_quiz":
            meta_data["_lp_passing_grade"] = str(data.passing_grade)

        for key, value in meta_data.items():
            meta = WPPostMeta(
                post_id=new_post.ID,
                meta_key=key,
                meta_value=value
            )
            self.session.add(meta)

        # Link to Section
        # Find max order
        stmt = select(LPSectionItem).where(LPSectionItem.section_id == section_id).order_by(col(LPSectionItem.item_order).desc())
        result = await self.session.exec(stmt)
        last_item = result.first()
        order = (last_item.item_order + 1) if last_item else 1

        section_item = LPSectionItem(
            section_id=section_id,
            item_id=new_post.ID,
            item_order=order,
            item_type=data.type
        )
        self.session.add(section_item)
        await self.session.commit()
        await self.session.refresh(new_post)

        return LPItem(
            id=new_post.ID,
            title=new_post.post_title,
            type=new_post.post_type,
            duration=data.duration,
            preview=data.preview,
            content=new_post.post_content
        )

    async def add_question_to_quiz(self, quiz_id: int, data: Any) -> LPQuestion:
        # Create Question Post
        new_post = WPPost(
            post_author=1,
            post_title=data.title,
            post_content=data.content,
            post_status="publish",
            post_type="lp_question",
            post_name=data.title.lower().replace(" ", "-"),
            post_date=datetime.now(),
            post_date_gmt=datetime.now()
        )
        self.session.add(new_post)
        await self.session.commit()
        await self.session.refresh(new_post)

        # Add Question Meta
        # Type (true_or_false, etc)
        meta = WPPostMeta(
            post_id=new_post.ID,
            meta_key="_lp_type",
            meta_value=data.type
        )
        self.session.add(meta)

        # Add Answers
        for idx, opt in enumerate(data.options):
            answer = LPQuestionAnswer(
                question_id=new_post.ID,
                title=opt.title,
                value=opt.value,
                order=idx + 1,
                is_true="yes" if opt.is_true else "no"
            )
            self.session.add(answer)

        # Link to Quiz
        # Find max order
        stmt = select(LPQuizQuestion).where(LPQuizQuestion.quiz_id == quiz_id).order_by(col(LPQuizQuestion.question_order).desc())
        result = await self.session.exec(stmt)
        last_q = result.first()
        order = (last_q.question_order + 1) if last_q else 1

        quiz_q = LPQuizQuestion(
            quiz_id=quiz_id,
            question_id=new_post.ID,
            question_order=order
        )
        self.session.add(quiz_q)
        await self.session.commit()
        await self.session.refresh(new_post)

        return LPQuestion(
            id=new_post.ID,
            title=new_post.post_title,
            content=new_post.post_content,
            type=data.type,
            options=data.options
        )

    async def update_course(self, course_id: int, data: Any) -> Optional[LPCourse]:
        # Fetch course
        stmt = select(WPPost).where(WPPost.ID == course_id, WPPost.post_type == "lp_course")
        result = await self.session.exec(stmt)
        post = result.first()

        if not post:
            return None

        # Update Post fields
        if data.title is not None:
            post.post_title = data.title
            post.post_name = data.title.lower().replace(" ", "-")
        if data.content is not None:
            post.post_content = data.content
        if data.excerpt is not None:
            post.post_excerpt = data.excerpt
        if data.status is not None:
            post.post_status = data.status

        post.post_modified = datetime.now()
        post.post_modified_gmt = datetime.now()

        self.session.add(post)

        # Update Meta
        meta_updates = {}
        if data.price is not None:
            meta_updates["_lp_price"] = str(data.price)
        if data.duration is not None:
            meta_updates["_lp_duration"] = data.duration
        if data.level is not None:
            meta_updates["_lp_level"] = data.level
        if data.students is not None:
            meta_updates["_lp_students"] = str(data.students)

        for key, value in meta_updates.items():
            # Check if meta exists
            m_stmt = select(WPPostMeta).where(WPPostMeta.post_id == course_id, WPPostMeta.meta_key == key)
            m_result = await self.session.exec(m_stmt)
            meta = m_result.first()

            if meta:
                meta.meta_value = value
                self.session.add(meta)
            else:
                new_meta = WPPostMeta(post_id=course_id, meta_key=key, meta_value=value)
                self.session.add(new_meta)

        await self.session.commit()
        await self.session.refresh(post)

        return await self.get_course(course_id)

    async def set_course_thumbnail(self, course_id: int, attachment_id: int) -> bool:
        """Set course featured image"""
        course = await self.session.get(WPPost, course_id)
        if not course or course.post_type != "lp_course":
            return False

        # Verify attachment
        attachment = await self.session.get(WPPost, attachment_id)
        if not attachment or attachment.post_type != "attachment":
            return False

        # Set meta
        from app.repo.wordpress.posts import WPPostRepository
        post_repo = WPPostRepository(self.session)
        await post_repo.set_post_meta(course_id, "_thumbnail_id", str(attachment_id))
        return True

    async def get_course_thumbnail(self, course_id: int) -> Optional[dict]:
        """Get course featured image"""
        from app.repo.wordpress.posts import WPPostRepository
        post_repo = WPPostRepository(self.session)
        return await post_repo.get_featured_image(course_id)

    async def delete_course(self, course_id: int, force: bool = False) -> bool:
        """Delete (trash) a course. If force=True, permanently delete."""
        # Fetch course
        stmt = select(WPPost).where(WPPost.ID == course_id, WPPost.post_type == "lp_course")
        result = await self.session.exec(stmt)
        post = result.first()

        if not post:
            return False

        if force:
            # Permanently delete post and its meta
            meta_stmt = select(WPPostMeta).where(WPPostMeta.post_id == course_id)
            meta_result = await self.session.exec(meta_stmt)
            for meta in meta_result.all():
                await self.session.delete(meta)

            await self.session.delete(post)
        else:
            # Soft delete (trash)
            post.post_status = "trash"
            self.session.add(post)

        await self.session.commit()
        return True

    async def get_course_learners(self, course_id: int) -> List[LPLearner]:
        """Get all learners enrolled in a course"""
        stmt = select(LPUserItem, WPUser).join(
            WPUser, LPUserItem.user_id == WPUser.ID
        ).where(
            LPUserItem.item_id == course_id,
            LPUserItem.item_type == "lp_course"
        )
        result = await self.session.exec(stmt)
        rows = result.all()

        learners = []
        for lp_item, user in rows:
            # Calculate progress (approximate as count of completed items / total items)
            # 1. Total items in curriculum
            curriculum = await self.get_curriculum(course_id)
            total_items = sum(len(s.items) for s in curriculum.sections)

            # 2. Completed items by user
            comp_stmt = select(LPUserItem).where(
                LPUserItem.user_id == user.ID,
                LPUserItem.ref_id == course_id,
                LPUserItem.status == "completed"
            )
            comp_res = await self.session.exec(comp_stmt)
            completed_count = len(comp_res.all())

            progress = (completed_count / total_items * 100) if total_items > 0 else 0

            learners.append(LPLearner(
                user_id=user.ID,
                username=user.user_login,
                display_name=user.display_name,
                email=user.user_email,
                enrollment_date=lp_item.start_time,
                status=lp_item.status,
                graduation=lp_item.graduation,
                progress_percent=round(progress, 2)
            ))
        return learners

    async def get_course_stats(self, course_id: int) -> LPCourseStats:
        """Get aggregate stats for a course"""
        stmt = select(LPUserItem).where(
            LPUserItem.item_id == course_id,
            LPUserItem.item_type == "lp_course"
        )
        result = await self.session.exec(stmt)
        enrollments = result.all()

        total = len(enrollments)
        completed = len([e for e in enrollments if e.status == "completed"])
        in_progress = total - completed

        passing_rate = (len([e for e in enrollments if e.graduation == "passed"]) / total * 100) if total > 0 else 0

        # Average quiz scores
        # 1. Find all quizzes in this course
        curriculum = await self.get_curriculum(course_id)
        quiz_ids = [item.id for section in curriculum.sections for item in section.items if item.type == "lp_quiz"]

        total_score = 0
        score_count = 0

        if quiz_ids:
            for qid in quiz_ids:
                res_stmt = select(LPUserItemResult).join(
                    LPUserItem, LPUserItem.user_item_id == LPUserItemResult.user_item_id
                ).where(
                    LPUserItem.item_id == qid,
                    LPUserItem.ref_id == course_id
                )
                res_results = await self.session.exec(res_stmt)
                for res in res_results.all():
                    try:
                        data = json.loads(res.result)
                        results = data.get("results", {})
                        total_score += results.get("user_score", 0)
                        score_count += 1
                    except:
                        continue

        avg_score = (total_score / score_count) if score_count > 0 else 0

        return LPCourseStats(
            total_students=total,
            completed_students=completed,
            in_progress_students=in_progress,
            passing_rate=round(passing_rate, 2),
            average_quiz_score=round(avg_score, 2)
        )

    async def update_section(self, section_id: int, data: LPSectionUpdate) -> Optional[SchemaLPSection]:
        statement = select(LPSection).where(LPSection.section_id == section_id)
        result = await self.session.exec(statement)
        section = result.first()

        if not section:
            return None

        if data.title is not None:
            section.section_name = data.title
        if data.description is not None:
            section.section_description = data.description
        if data.order is not None:
            section.section_order = data.order

        self.session.add(section)
        await self.session.commit()
        await self.session.refresh(section)

        # We need to fetch items to return SchemaLPSection, or return empty for now
        # For simplicity, returning empty items or fetching if needed.
        # Let's fetch strict basics
        return SchemaLPSection(
            id=section.section_id,
            title=section.section_name,
            order=section.section_order,
            description=section.section_description,
            items=[] # Items unchanged/unfetched
        )

    async def delete_section(self, section_id: int) -> bool:
        statement = select(LPSection).where(LPSection.section_id == section_id)
        result = await self.session.exec(statement)
        section = result.first()

        if not section:
            return False

        # Should probably delete section items connections too or cascade?
        # Manually delete section items relation
        item_stmt = select(LPSectionItem).where(LPSectionItem.section_id == section_id)
        item_res = await self.session.exec(item_stmt)
        items = item_res.all()
        for i in items:
            self.session.delete(i)

        self.session.delete(section)
        await self.session.commit()
        return True

    async def update_question(self, question_id: int, data: LPQuestionUpdate) -> Optional[LPQuestion]:
        stmt = select(WPPost).where(WPPost.ID == question_id)
        result = await self.session.exec(stmt)
        post = result.first()

        if not post:
            return None

        if data.title is not None:
            post.post_title = data.title
            post.post_name = data.title.lower().replace(" ", "-")
        if data.content is not None:
            post.post_content = data.content
        if data.type is not None:
            # Update meta _lp_type
            meta_stmt = select(WPPostMeta).where(
                WPPostMeta.post_id == question_id,
                WPPostMeta.meta_key == "_lp_type"
            )
            meta_res = await self.session.exec(meta_stmt)
            meta = meta_res.first()
            if meta:
                meta.meta_value = data.type
                self.session.add(meta)
            else:
                self.session.add(WPPostMeta(post_id=question_id, meta_key="_lp_type", meta_value=data.type))

        post.post_modified = datetime.now()
        post.post_modified_gmt = datetime.now()
        self.session.add(post)

        if data.options is not None:
            # Replace options/answers
            # 1. Delete existing
            del_stmt = select(LPQuestionAnswer).where(LPQuestionAnswer.question_id == question_id)
            del_res = await self.session.exec(del_stmt)
            for old in del_res.all():
                await self.session.delete(old)

            # 2. Add new
            for idx, opt in enumerate(data.options):
                answer = LPQuestionAnswer(
                    question_id=question_id,
                    title=opt.title,
                    value=opt.value,
                    order=idx + 1,
                    is_true="yes" if opt.is_true else "no"
                )
                self.session.add(answer)

        await self.session.commit()
        await self.session.refresh(post)

        # Refetch to construct return object properly
        # Or manually construct if we are confident
        # Let's manually construct to save a query if we updated everything
        return LPQuestion(
            id=post.ID,
            title=post.post_title,
            content=post.post_content,
            type=data.type if data.type else "lp_question", # Placeholder if not fetched
            status=post.post_status,
            options=data.options if data.options else []
        )

    async def delete_question(self, question_id: int, force: bool = False) -> bool:
        # Delete Post (trash or permanent)
        return await self.delete_item(question_id, force=force)

    async def update_item(self, item_id: int, data: Any) -> Optional[LPItem]:
        # Fetch item
        stmt = select(WPPost).where(WPPost.ID == item_id)
        result = await self.session.exec(stmt)
        post = result.first()

        if not post:
            return None

        # Update Post fields
        if data.title is not None:
            post.post_title = data.title
            post.post_name = data.title.lower().replace(" ", "-")
        if data.content is not None:
            post.post_content = data.content
        if data.type is not None:
            post.post_type = data.type

        post.post_modified = datetime.now()
        post.post_modified_gmt = datetime.now()

        self.session.add(post)

        # Update Meta
        meta_updates = {}
        if data.duration is not None:
            meta_updates["_lp_duration"] = data.duration
        if data.preview is not None:
            meta_updates["_lp_preview"] = "yes" if data.preview else "no"
        if data.passing_grade is not None and post.post_type == "lp_quiz":
            meta_updates["_lp_passing_grade"] = str(data.passing_grade)

        for key, value in meta_updates.items():
            m_stmt = select(WPPostMeta).where(WPPostMeta.post_id == item_id, WPPostMeta.meta_key == key)
            m_result = await self.session.exec(m_stmt)
            meta = m_result.first()

            if meta:
                meta.meta_value = value
                self.session.add(meta)
            else:
                new_meta = WPPostMeta(post_id=item_id, meta_key=key, meta_value=value)
                self.session.add(new_meta)

        await self.session.commit()
        await self.session.refresh(post)

        # Re-fetch item to return LPItem
        # Simplified return for now
        return LPItem(
            id=post.ID,
            title=post.post_title,
            type=post.post_type,
            status=post.post_status,
            duration=data.duration, # Might be None if not updated, strictly should fetch
            preview=data.preview if data.preview is not None else False,
            content=post.post_content
        )

    async def delete_item(self, item_id: int, force: bool = False) -> bool:
        """Delete (trash) an item. If force=True, permanently delete."""
        # Fetch item
        stmt = select(WPPost).where(WPPost.ID == item_id)
        result = await self.session.exec(stmt)
        post = result.first()

        if not post:
            return False

        if force:
            # Permanently delete post and its meta
            meta_stmt = select(WPPostMeta).where(WPPostMeta.post_id == item_id)
            meta_result = await self.session.exec(meta_stmt)
            for meta in meta_result.all():
                await self.session.delete(meta)

            await self.session.delete(post)
        else:
            # Soft delete (trash)
            post.post_status = "trash"
            self.session.add(post)

        await self.session.commit()
        return True

class LPUserItemRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_item(self, user_item_id: int) -> Optional[LPUserItem]:
        return await self.session.get(LPUserItem, user_item_id)

    async def get_user_items(self, user_id: int, item_type: str = "lp_course") -> List[LPUserItem]:
        statement = select(LPUserItem).where(
            LPUserItem.user_id == user_id,
            LPUserItem.item_type == item_type
        )
        result = await self.session.exec(statement)
        return result.all()

    async def get_course_progress(self, user_id: int, course_id: int) -> Optional[LPUserItem]:
        statement = select(LPUserItem).where(
            LPUserItem.user_id == user_id,
            LPUserItem.item_id == course_id,
            LPUserItem.item_type == "lp_course"
        )
        result = await self.session.exec(statement)
        return result.first()

    async def get_quiz_submissions(self, quiz_id: int, user_id: Optional[int] = None) -> List[LPQuizSubmissionRead]:
        """Get all submissions for a quiz"""
        stmt = select(LPUserItem, WPUser).join(
            WPUser, LPUserItem.user_id == WPUser.ID
        ).where(
            LPUserItem.item_id == quiz_id,
            LPUserItem.item_type == "lp_quiz"
        )

        if user_id:
            stmt = stmt.where(LPUserItem.user_id == user_id)

        result = await self.session.exec(stmt)
        rows = result.all()

        submissions = []
        for lp_item, user in rows:
            # Fetch result data
            res_stmt = select(LPUserItemResult).where(LPUserItemResult.user_item_id == lp_item.user_item_id)
            res_result = await self.session.exec(res_stmt)
            res_obj = res_result.first()

            detail = None
            if res_obj and res_obj.result:
                try:
                    data = json.loads(res_obj.result)
                    res_data = data.get("results", {})
                    detail = LPQuizResultDetail(
                        user_mark=res_data.get("user_mark", 0),
                        question_count=res_data.get("question_count", 0),
                        user_score=res_data.get("user_score", 0),
                        passing_grade=res_data.get("passing_grade", 0),
                        passed=res_data.get("passed", False),
                        questions=data.get("questions", [])
                    )
                except:
                    pass

            submissions.append(LPQuizSubmissionRead(
                user_item_id=lp_item.user_item_id,
                user_id=user.ID,
                user_display_name=user.display_name,
                quiz_id=quiz_id,
                start_time=lp_item.start_time,
                end_time=lp_item.end_time,
                status=lp_item.status,
                graduation=lp_item.graduation,
                results=detail
            ))
        return submissions

    async def get_quiz_submission_details(self, user_item_id: int) -> Optional[LPQuizSubmissionRead]:
        """Get details for a specific quiz submission"""
        stmt = select(LPUserItem, WPUser).join(
            WPUser, LPUserItem.user_id == WPUser.ID
        ).where(
            LPUserItem.user_item_id == user_item_id
        )
        result = await self.session.exec(stmt)
        row = result.first()

        if not row:
            return None

        lp_item, user = row

        # Fetch result data
        res_stmt = select(LPUserItemResult).where(LPUserItemResult.user_item_id == lp_item.user_item_id)
        res_result = await self.session.exec(res_stmt)
        res_obj = res_result.first()

        detail = None
        if res_obj and res_obj.result:
            try:
                data = json.loads(res_obj.result)
                res_data = data.get("results", {})
                detail = LPQuizResultDetail(
                    user_mark=res_data.get("user_mark", 0),
                    question_count=res_data.get("question_count", 0),
                    user_score=res_data.get("user_score", 0),
                    passing_grade=res_data.get("passing_grade", 0),
                    passed=res_data.get("passed", False),
                    questions=data.get("questions", [])
                )
            except:
                pass

        return LPQuizSubmissionRead(
            user_item_id=lp_item.user_item_id,
            user_id=user.ID,
            user_display_name=user.display_name,
            quiz_id=lp_item.item_id,
            start_time=lp_item.start_time,
            end_time=lp_item.end_time,
            status=lp_item.status,
            graduation=lp_item.graduation,
            results=detail
        )

class LPOrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_order_items(self, order_id: int) -> List[LPOrderItem]:
        statement = select(LPOrderItem).where(LPOrderItem.order_id == order_id)
        result = await self.session.exec(statement)
        return result.all()
