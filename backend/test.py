from advanced_prompting_system import advanced_prompting_system

# Example 1: Simple Clinical Trial Document
clinical_trial_text_1 = """
INTRODUCTION
This clinical trial investigates the effects of Drug A on patients with lupus.

METHODS
The study was conducted on 200 participants, each receiving 50mg of Drug A daily.

RESULTS
The results showed a 70% improvement in symptoms over 5 years.

ADVERSE EVENTS
10% of participants experienced mild adverse events.
"""

query_1 = "What is the predicted efficacy over 5 years?"

# Example 2: Complex Comparative Query
clinical_trial_text_2 = """
INTRODUCTION
This comparative study evaluates the efficacy and safety of Drug A and Drug B for treating rheumatoid arthritis.

METHODS
Participants were randomized into two groups. Group A received 50mg of Drug A, and Group B received 100mg of Drug B.

RESULTS
After 12 months, Group A demonstrated a 40% reduction in symptoms, while Group B demonstrated a 35% reduction.

ADVERSE EVENTS
Group A reported a 12% adverse event rate, while Group B reported a 15% adverse event rate.
"""

query_2 = "How does the efficacy of Drug A compare to Drug B for rheumatoid arthritis?"

# Example 3: Inference-Based Query
clinical_trial_text_3 = """
INTRODUCTION
This clinical trial investigates the impact of long-term use of Drug C on the remission rates in patients with chronic arthritis.

METHODS
Participants were observed over a period of 5 years. Drug C was administered at a dosage of 200mg daily.

RESULTS
The study showed that 70% of participants maintained remission during the first year. However, by year 5, remission rates dropped to 50%.

ADVERSE EVENTS
15% of the participants reported moderate adverse events during the study.
"""

query_3 = "What is the expected remission rate for Drug C over 5 years?"

# Example 4: Safety Comparison in Elderly
clinical_trial_text_4 = """
INTRODUCTION
This study compares the safety profiles of Drug X and Drug Y in elderly patients (over 65) with diabetes.

METHODS
Participants were split into two groups: Group X received 50mg of Drug X daily, and Group Y received 100mg of Drug Y daily.

RESULTS
Adverse events were reported in 25% of Group X participants and 35% of Group Y participants.

ADVERSE EVENTS
Common adverse events included dizziness, nausea, and fatigue.
"""

query_4 = "Compare the adverse event rates between Drug X and Drug Y in elderly patients."

# Running the tests
#result_1 = advanced_prompting_system(query_1, clinical_trial_text_1)
#result_2 = advanced_prompting_system(query_2, clinical_trial_text_2)
#result_3 = advanced_prompting_system(query_3, clinical_trial_text_3)
result_4 = advanced_prompting_system(query_4, clinical_trial_text_4)

# Print the results
#print(result_1)
#print(result_2)
#print(result_3)
print(result_4)
