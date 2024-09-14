from jsonschema import Draft7Validator
from typing import Any, Dict, List, Union
import datetime

def generate_dynamic_schema(datapoints: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a dynamic schema based on the provided datapoints."""
    schema = {
        "type": "object",
        "properties": {
            "description": {"type": "string"},
            "metadata": {
                "type": "object",
                "properties": {},
                "required": []
            },
            "extracted_features": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "description": {"type": "string"},
                        "value": {}
                    },
                    "required": ["description", "value"]
                }
            },
            "questions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "question": {"type": "string"},
                        "answer": {"type": "string"},
                    },
                    "required": ["question", "answer"]
                }
            },
            "outcome": {"type": "string"},
            "outcome_reasoning": {"type": "string"}
        },
        "required": ["description", "metadata", "extracted_features", "outcome", "outcome_reasoning"]
    }

    # Dynamically add metadata fields based on datapoints
    for key, value in datapoints.get("metadata", {}).items():
        schema["properties"]["metadata"]["properties"][key] = {"type": infer_type(value)}
        schema["properties"]["metadata"]["required"].append(key)

    # Add optional fields to questions if present in datapoints
    if "questions" in datapoints and datapoints["questions"]:
        sample_question = datapoints["questions"][0]
        if "options" in sample_question:
            schema["properties"]["questions"]["items"]["properties"]["options"] = {
                "type": "array",
                "items": {"type": "string"}
            }
            schema["properties"]["questions"]["items"]["required"].append("options")
        if "correct_option" in sample_question:
            schema["properties"]["questions"]["items"]["properties"]["correct_option"] = {"type": "string"}
            schema["properties"]["questions"]["items"]["required"].append("correct_option")

    return schema

def infer_type(value: Any) -> str:
    """Infer the JSON Schema type based on the Python type."""
    if isinstance(value, str):
        return "string"
    elif isinstance(value, bool):
        return "boolean"
    elif isinstance(value, int):
        return "integer"
    elif isinstance(value, float):
        return "number"
    elif isinstance(value, list):
        return "array"
    elif isinstance(value, dict):
        return "object"
    else:
        return "string"  # Default to string for unknown types

def validate_json_output(json_output: Dict[str, Any]) -> bool:
    """Validate the JSON output against a dynamically generated schema and perform custom validations."""
    schema = generate_dynamic_schema(json_output)
    validator = Draft7Validator(schema)
    errors = sorted(validator.iter_errors(json_output), key=lambda e: e.path)

    if errors:
        for error in errors:
            print(f"Schema validation error: {error.message}")
        return False

    if not custom_validation(json_output):
        return False

    return True

def custom_validation(data: Dict[str, Any]) -> bool:
    """Perform custom validations on the data."""
    # Validate description
    if not isinstance(data.get('description'), str) or len(data['description']) < 10:
        print("Validation error: 'description' must be a string with at least 10 characters")
        return False

    # Validate metadata
    metadata = data.get('metadata', {})
    if 'publication_date' in metadata:
        try:
            datetime.datetime.strptime(metadata['publication_date'], '%Y-%m-%d')
        except ValueError:
            print("Validation error: 'publication_date' must be in the format YYYY-MM-DD")
            return False

    # Validate extracted_features
    for feature in data.get('extracted_features', []):
        if not isinstance(feature.get('description'), str) or len(feature['description']) < 5:
            print("Validation error: Feature description must be a string with at least 5 characters")
            return False

    # Validate questions
    for question in data.get('questions', []):
        if 'options' in question and 'correct_option' in question:
            if question['correct_option'] not in question['options']:
                print("Validation error: 'correct_option' must be one of the 'options'")
                return False

    return True

# Example usage
if __name__ == "__main__":
    sample_output = {
        "description": "This is a sample description.",
        "metadata": {
            "authors": ["John Doe", "Jane Smith"],
            "publication_date": "2023-04-15",
            "journal": "Sample Journal",
            "impact_factor": 3.5
        },
        "extracted_features": [
            {"description": "Sample feature", "value": 42}
        ],
        "questions": [
            {
                "question": "What is the capital of France?",
                "answer": "Paris",
                "options": ["London", "Berlin", "Paris", "Madrid"],
                "correct_option": "Paris"
            }
        ],
        "outcome": "Positive",
        "outcome_reasoning": "Based on the analysis..."
    }

    is_valid = validate_json_output(sample_output)
    print(f"Validation result: {'Valid' if is_valid else 'Invalid'}")
