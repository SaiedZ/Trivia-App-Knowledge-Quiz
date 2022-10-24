# Full Stack Trivia App

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)    ![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)    ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)    ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)

## :page_with_curl: What's it ?

Trivia is a knowledge quiz app. It allows users to see who's the most knowledgeable of the bunch. The application provides functionnalities such as:

1. Display questions - both all questions and by category. Users can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

## :mag: About the Stack

### Backend

The [backend](./backend/README.md) directory contains a Flask and SQLAlchemy server. Endpoints are defined in the `__init__.py` of the `flaskr` folder which references models and db config. 

Directory folders:

1. `backend/flaskr/__init__.py` : Flask app where endpoints are defined.
2. `backend/test_flaskr.py`: Unittest
3. `backend/models.py`: models for DB and SQLAlchemy setup

> View the [Backend README](./backend/README.md) for more details.

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. 

> View the [Frontend README](./frontend/README.md) for more details.

##  📖  API Reference

### Getting Started

- **Base URL**: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.

- **Authentication**: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:
```json
{
    "success": false, 
    "error": 400,
    "message": "bad request",
}
```

The API will return three error types when requests fail:

- 400: Bad Request
- 404: {Resource} Not Found (Ressource is relplaced by the model's name: Category, Question...)
- 422: Not Processable
- 500: Internal Server Error 

### Endpoints
    
#### GET ` /categories `

- Sample: ` curl http://127.0.0.1:5000/categories `

- General:
    - Fetchs a list of category objects, success value, and total number of categories.
    - Request Arguments: None

```json  
{
  "categories": {
      "1": "Science", 
      "2": "Art", 
      "3": "Geography", 
      "4": "History", 
      "5": "Entertainment", 
      "6": "Sports"
  }, 
  "success": true,
  "total_categories": 6
}
```

---

#### GET ` /questions?page={integer} `
    
- Sample: ` curl http://127.0.0.1:5000/questions `
- Sample with page request argument: ` curl http://127.0.0.1:5000/questions?page=2 `
    
- General:
    - Fetchs a list of question objects, total number of questions, success value, current page number, the total page number and all categories.
    - Request Arguments: Include a request argument to choose page number, starting from 1.
    - Results are paginated in groups of 10. 

```json  
{
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    ...
  ],
  "total_questions": 19
  "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
  },
  "current_category": {},
  "current_page": 1,
  "success": true,
  "total_pages": 2,
}
```

- Example of error:
    - case: no questions to return
        ```json
        {
            "success": false,
             "error": "404",
             "message": "Questions not found"
         }
        ```
---
    
#### GET ` /categories/{id}/questions `

- Sample: ` curl http://127.0.0.1:5000/questions `
- Sample with page request argument: ` curl http://127.0.0.1:5000/questions?page=2 `
    
- General:
    - Fetchs a list of questions for a cateogry specified by id request argument.
    - Request Arguments: `id` - integer.
    - Result: An object with questions for the specified category, total questions, and current category string

```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 4
    }
  ],
  "totalQuestions": 100,
  "currentCategory": "History"
}
```

- Example of error:
    - case: no questions to return
        ```json
        {
            "success": false,
             "error": "404",
             "message": "Questions not found"
         }
        ```
    - case: category id does't exist
        ```json
        {
            "success": false,
             "error": "404",
             "message": "Category not found"
         }
        ```
---

#### DELETE ` /questions/{id} `

- Sample: ` curl http://127.0.0.1:5000/questions/6 -X DELETE `
    
- General:
    - Deletes a question by id using url parameters.
    - Request Arguments: ` id ` - integer.
    - Returns success message and the id of the deleted question.
    
```json
{
  "deleted": 6, 
  "success": true
}
```
  
---
    
#### POST ` /questions ` 

- Sample: ` curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"What is the capital of France?", "answer":"Paris", "difficulty":"1", "category":"3"}'
 `

- General:
    - Creates a new question using the submitted `question`, `answer`, `difficulty` and `category`.
    - Request body:
        ```json
        {
          "question": "Heres a new question string",
          "answer": "Heres a new answer string",
          "difficulty": 1,
          "category": 3
        }
        ```
    - Returns JSON Object with success value set to true:
       ```json
        {
            "success": true
        }
       ```
---
    
#### POST ` /questions `
    
- Sample: ` curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"france"}'`

- General:
    - Sends a post request in order to search for a specific question by search term
    - Request Body:
    ```json
    {
      "searchTerm": "this is the term the user is looking for"
    }
    ```
    - Returns JSON Object with success value set to true, list of all questions that match with the search and the total number of questions:

    ```json
      {
      "questions": [
          {
              "answer": "France", 
              "category": 3, 
              "difficulty": 2, 
              "id": 9, 
              "question": "What is the capital of France?"
          }, 
      ], 
      "success": true, 
      "total_questions": 1
    }
    ```

- Example of error:
    - case: no questions found with search terme in question attribut
        ```json
        {
            "success": false,
             "error": "422",
             "message": "unprocessable"
         }
        ```
--- 

#### POST ` /quizzes `
    
- Sample: ` curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [2, 5], "quiz_category": {"type": "Science", "id": "1"}}' `
- General:
    - Sends a post request in order to get the next question
    - Request Body:
    ```json
    {
        "previous_questions": [2, 5],
        "quiz_category": {"type": "Science", "id": "1"}
     }
    ```
    - Returns JSON Object with the next question:

    ```json
      {
          "question": {
              "answer": "France", 
              "category": 3, 
              "difficulty": 2, 
              "id": 9, 
              "question": "What is the capital of France?"
          }, 
      }
    ```

--- 
