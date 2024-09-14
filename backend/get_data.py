import requests
import json


def query_clinical_trials(query):
    """
    Query the ClinicalTrials.gov API to retrieve clinical trial data related to immunology.
    """
    base_url = "https://clinicaltrials.gov/api/query/full_studies"
    params = {
        "expr": query,
        "max_rnk": 30,  # Get 30 trials
        "fmt": "json",
    }
    response = requests.get(base_url, params=params)
    return response.json()


# Example usage
immunology_trials = query_clinical_trials("immunology")
print(json.dumps(immunology_trials, indent=2))
