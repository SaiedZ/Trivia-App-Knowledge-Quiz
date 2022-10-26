import random
from flask_cors import CORS
from flask import Flask, request, abort, jsonify

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_items(request, items):
    """Paginate items for the next page.

    Params:
        request object
        selection of items based on db models
    Returns:
        current_items: list of items for the next page
    """
    page = request.args.get("page", 1, type=int)
    pages = len(items) // QUESTIONS_PER_PAGE + 1

    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    formatted_items = [item.format() for item in items]

    return (
        formatted_items[start:end],
        page,
        pages
    )


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r"/*": {"origins": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        """Set response headers."""
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    def _get_categories_dict():
        """Return a dict of categories.

        keys are categories id and value are types,
        raises a 404 if there is no categories in the database
        """
        categories = Category.query.order_by(Category.id).all()

        if not categories:
            abort(404, 'Category not found')

        return {str(category.id): category.type for category in categories}

    @app.route("/categories")
    def retrieve_categories():
        """Retrieves all categories."""
        categories_dict = _get_categories_dict()

        return jsonify(
            {
                "success": True,
                "categories": categories_dict,
                "total_categories": len(categories_dict),
            }
        )

    @app.route("/questions")
    def retrieve_questions():
        """Retrieve all questions.

        questions are paginated,
        returns the current page number
        and the total pages number.
        """
        categories_dict = _get_categories_dict()

        questions = Question.query.order_by(Question.id).all()
        current_questions, page, pages = paginate_items(request, questions)

        if len(current_questions) == 0:
            abort(404, 'Questions not found')

        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "total_questions": len(Question.query.all()),
                "current_category": {},
                "categories": categories_dict,
                "current_page": page,
                "total_pages": pages
            }
        )

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)

            if question is None:
                abort(404)

            question.delete()

            return jsonify({"success": True, 'deleted': question_id})

        except Exception:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def handle_post_request_for_question():
        """Handle the creation or the search of questions."""

        body = request.get_json()

        searchTerm = body.get("searchTerm", None)

        if searchTerm:
            try:
                questions = Question.query.order_by(Question.id).filter(
                        Question.question.ilike(f"%{searchTerm}%")
                    ).all()
            except Exception:
                abort(422)

            formatted_questions = [question.format() for question in questions]
            return jsonify(
                {
                    "success": True,
                    "questions": formatted_questions,
                    "total_questions": len(questions),
                    "current_category": {},
                }
            )

        else:
            new_question = body.get("question", None)
            new_answer = body.get("answer", None)
            new_difficulty = body.get("difficulty", None)
            category = body.get("category", None)

            try:
                question = Question(
                    question=new_question, answer=new_answer,
                    difficulty=new_difficulty, category=int(category)
                )
                question.insert()
            except Exception:
                abort(422)

            return jsonify({"success": True}), 201

    @app.route("/categories/<int:category_id>/questions")
    def retrieve_questions_by_category(category_id):
        """Return all question of a given category

        question are filtered by the category_id parameter of the request.
        """

        current_category = Category.query.filter(
            Category.id == category_id).one_or_none()

        if current_category is None:
            abort(404, 'Category not found')

        categories_dict = _get_categories_dict()

        questions = Question.query.order_by(
            Question.id).filter_by(category=category_id).all()

        if len(questions) == 0:
            abort(404, 'Questions not found')

        formatted_questions = [question.format() for question in questions]

        return jsonify(
            {
                "success": True,
                "questions": formatted_questions,
                "total_questions": len(questions),
                "current_category": {
                    current_category.id: current_category.type},
                "categories": categories_dict,
            }
        )

    @app.route("/quizzes", methods=['POST'])
    def retrive_random_question_for_quiz():
        body = request.get_json()

        previous_questions_id = body.get("previous_questions", [])
        quiz_category = body.get("quiz_category", {})

        if not quiz_category:
            abort(400)

        try:
            quiz_category_id = int(quiz_category['id'])
            if quiz_category_id:
                category_questions = Question.query.filter_by(
                    category=quiz_category_id
                )
            else:
                category_questions = Question.query.all()

        except TypeError:
            abort(422)

        except Exception:
            abort(500)

        not_seen_questions = [
            question for question in category_questions
            if question.id not in previous_questions_id
        ]
        try:
            next_question = random.choice(not_seen_questions)
            next_question_formatted = next_question.format()
        except IndexError:  # No More questions
            return jsonify({'success': True})

        return jsonify({'question': next_question_formatted})

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify(
                {"success": False,
                 "error": 400,
                 "message": "bad request"}
            ),
            400
        )

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify(
                {"success": False,
                 "error": 404,
                 "message": error.description}
            ),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify(
                {"success": False,
                 "error": 422,
                 "message": "unprocessable"}
            ),
            422,
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            jsonify(
                {"success": False,
                 "error": 500,
                 "message": "Internal Server Error"}
            ),
            500
        )

    return app
