import inquirer
from inquirer.questions import Question
from .prompt_data import InputQuestionData
from typing import List


def query_builder(questions: List[InputQuestionData]) -> List[Question]:
    """
    Converts a list of dictionary-based question definitions into a list
    of inquirer Question objects.
    """

    inquirer_questions: List[Question] = []

    for q_data in questions:
        q_type = q_data.get("type")
        q_name = q_data.get("name", "temp_name")  # Ensure a name is always available
        q_message = q_data.get("message", "Default Message")

        if q_type == "confirm":
            # Extract required fields and initialize inquirer.Confirm
            inquirer_questions.append(
                inquirer.Confirm(
                    name=q_name,
                    message=q_data["message"],
                    default=q_data.get("default", None),
                )
            )
        elif q_type == "text":
            # Extract fields and initialize inquirer.Text
            inquirer_questions.append(
                inquirer.Text(
                    name=q_name,
                    message=q_message,
                    default=q_data.get("default", None),
                    validate=q_data.get("validate"),
                )
            )
        elif q_type == "list":
            # Extract fields and initialize inquirer.List
            inquirer_questions.append(
                inquirer.List(
                    name=q_name,
                    message=q_data["message"],
                    choices=q_data.get("choices", []),
                    default=q_data.get("default", None),
                    carousel=q_data.get("carousel", None),
                )
            )

    return inquirer_questions
