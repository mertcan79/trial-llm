from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, validator, ValidationError
from datetime import datetime

# Pydantic model for Metadata
class MetadataModel(BaseModel):
    authors: List[str]
    publication_date: Optional[str] = Field(
        None, regex=r"^\d{4}-\d{2}-\d{2}$", description="Date in format YYYY-MM-DD"
    )
    journal: Optional[str]
    impact_factor: Optional[float]

    @validator("publication_date")
    def check_date_format(cls, v):
        try:
            if v:
                datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format, should be YYYY-MM-DD")
        return v

# Pydantic model for Extracted Features
class ExtractedFeatureModel(BaseModel):
    description: str = Field(..., min_length=5)
    value: Any

# Pydantic model for Questions
class QuestionModel(BaseModel):
    question: str
    answer: str
    options: Optional[List[str]] = None
    correct_option: Optional[str] = None

    @validator("correct_option")
    def check_correct_option_in_options(cls, v, values):
        if v and v not in values.get("options", []):
            raise ValueError("'correct_option' must be one of the 'options'")
        return v

# Pydantic model for the main JSON structure
class OutputModel(BaseModel):
    description: str = Field(..., min_length=10)
    metadata: MetadataModel
    extracted_features: List[ExtractedFeatureModel]
    questions: Optional[List[QuestionModel]] = None
    outcome: str
    outcome_reasoning: str

# Validation function using Pydantic models
def validate_json_output(json_output: Dict[str, Any]) -> bool:
    """Validate the JSON output using Pydantic models."""
    try:
        validated_output = OutputModel(**json_output)
        print("Validation succeeded")
        return True
    except ValidationError as e:
        print("Validation failed:", e)
        return False

# Example usage
if __name__ == "__main__":
    sample_output = {
        "description": "This is a sample description.",
        "metadata": {
            "authors": ["John Doe", "Jane Smith"],
            "publication_date": "2023-04-15",
            "journal": "Sample Journal",
            "impact_factor": 3.5,
        },
        "extracted_features": [{"description": "Sample feature", "value": 42}],
        "questions": [
            {
                "question": "What is the capital of France?",
                "answer": "Paris",
                "options": ["London", "Berlin", "Paris", "Madrid"],
                "correct_option": "Paris",
            }
        ],
        "outcome": "Positive",
        "outcome_reasoning": "Based on the analysis...",
    }

    is_valid = validate_json_output(sample_output)
    print(f"Validation result: {'Valid' if is_valid else 'Invalid'}")
