import os
from dotenv import load_dotenv

import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

load_dotenv()
DATABASE_PATH_TEST = os.environ['DB_URI_TEST']


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        # self.database_name = "trivia_test"
        self.database_path = DATABASE_PATH_TEST
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'What is the last Assassin Creed',
            'answer': 'Mirage',
            'category': 1,
            'difficulty': 4
        }
        self.new_category = {'type': 'Game'}
        self.wrong_category_id = 1000
        self.wrong_question_id = 1000
        self.test_category_id = 1
        with self.app.app_context():
            self.test_category = Category.query.filter(
                Category.id == self.test_category_id).one_or_none()

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        with self.app.app_context():
            test_quetions = Question.query.filter(
                Question.answer == self.new_question['answer']
            )
            for question in test_quetions:
                question.delete()

    def test_get_categories(self):

        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])
        self.assertTrue(len(data["categories"]))

    def test_post_categories_not_allowed(self):

        res = self.client().post("/categories")
        self.assertEqual(res.status_code, 405)

    def test_get_questions_by_category(self):

        res = self.client().get(
            f"/categories/{self.test_category_id}/questions"
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))
        self.assertEqual(
            data["current_category"],
            {str(self.test_category.id): self.test_category.type}
        )
        self.assertTrue(len(data["categories"]))

    def test_get_questions_wrong_category_returns_404(self):
        res = self.client().get(
            f"/categories/{self.wrong_category_id}/questions"
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'Category not found')

    def test_get_paginated_questions(self):

        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))
        self.assertEqual(data['current_page'], 1)
        self.assertTrue(data['total_pages'])

        res_page_2 = self.client().get("/questions?page=2")
        data_page_2 = json.loads(res_page_2.data)

        self.assertEqual(res_page_2.status_code, 200)
        self.assertEqual(data_page_2["success"], True)
        self.assertEqual(data_page_2['current_page'], 2)

    def test_create_new_question(self):

        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        with self.app.app_context():
            question = Question.query.filter_by(
                question=self.new_question['question']).one_or_none()

            self.assertIsNotNone(question)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)

    def test_create_new_question_fail_if_wrong_category(self):
        question = self.new_question
        question['category'] = self.wrong_category_id
        res = self.client().post("/questions", json=question)

        self.assertEqual(res.status_code, 422)

    def test_delete_question(self):

        with self.app.app_context():
            question = Question(
                question=self.new_question['question'],
                answer=self.new_question['answer'],
                category=self.new_question['category'],
                difficulty=self.new_question['difficulty']
            )
            question.insert()

            res_delete = self.client().delete(f"/questions/{question.id}")
            self.assertEqual(res_delete.status_code, 200)

        with self.app.app_context():
            deleted_question = Question.query.get(question.id)
            self.assertEqual(deleted_question, None)

    def test_delete_question_fail_if_wrong_question_id(self):
        res_delete = self.client().delete(
            f"/questions/{self.wrong_question_id}")

        self.assertEqual(res_delete.status_code, 422)

    def test_retrieve_question_quiz_success(self):
        json_data = {'previous_questions': [1],
                     'quiz_category': {'id': 1}}

        res = self.client().post("/quizzes", json=json_data)
        data = json.loads(res.data)

        category = data['question']['category']

        self.assertEqual(res.status_code, 200)
        self.assertEqual(category, json_data['quiz_category']['id'])

    def test_retrieve_question_quiz_fails(self):

        response = self.client().post('/quizzes', json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
