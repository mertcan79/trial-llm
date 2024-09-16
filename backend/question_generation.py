few_shot_examples = {
    'factual': [
        "Q: What is the sample size?\nA: The study included 200 participants.",
        "Q: What was the primary endpoint?\nA: The primary endpoint was the proportion of patients achieving remission after 12 months.",
        "Q: What was the dosage of Drug A?\nA: Participants received 50mg of Drug A daily.",
        "Q: What is the follow-up period?\nA: The follow-up period was 5 years.",
        "Q: What is the study design?\nA: This was a randomized, double-blind, placebo-controlled trial with a sample size of 500 participants.",
        "Q: What was the dosage of Drug B administered?\nA: Participants received 100mg of Drug B every 8 hours for 2 weeks.",
        "Q: What is the duration of adverse event monitoring?\nA: Adverse events were monitored for 24 months after the trial completion.",
        "Q: How many participants reported adverse events?\nA: 35% of participants reported mild adverse events, including nausea and headaches."
    ],
    'comparative': [
        "Q: How does the efficacy of Drug A compare to Drug B?\nA: Drug A showed a 25% improvement in symptom reduction compared to 15% for Drug B over 12 months.",
        "Q: Compare the adverse events between Drug X and Drug Y.\nA: Drug X had fewer adverse events compared to Drug Y (15% vs. 25% respectively).",
        "Q: Compare the remission rates of Drug A and Drug B.\nA: Drug A showed a 40% remission rate, while Drug B showed a 35% remission rate.",
        "Q: How does Drug A compare with Drug B?\nA: Drug A showed a 20% higher efficacy than Drug B.",
        "Q: Compare the adverse event rates of Drug X versus Drug Y in patients over 60 years old.\nA: Drug X had an adverse event rate of 10%, while Drug Y had a rate of 15% in patients over 60 years old.",
        "Q: Compare the efficacy of Drug C and Drug D in treating rheumatoid arthritis.\nA: Drug C demonstrated a 30% reduction in symptoms compared to 25% for Drug D after 6 months of treatment.",
        "Q: How do the safety profiles of Drug E and Drug F differ in elderly patients?\nA: Drug E had fewer gastrointestinal side effects (10% vs. 20%) compared to Drug F."
    ],
    'inferential': [
        "Q: Predict the long-term impact of Drug C on remission rates.\nA: Based on trial data, Drug C is expected to maintain a remission rate of 65% over 5 years.",
        "Q: What are the potential long-term side effects of Drug D?\nA: Long-term use of Drug D may increase the risk of cardiovascular events by 10%.",
        "Q: What is the predicted efficacy over 5 years?\nA: Based on the data, the efficacy is expected to remain above 70% over 5 years.",
        "Q: Predict long-term safety profiles.\nA: Long-term use may increase the risk of adverse events by 10%.",
        "Q: Can we infer any correlation between dosage adjustments and reduction in adverse events for Drug D?\nA: The trial suggests that reducing the dosage of Drug D by 25% leads to a 10% reduction in adverse event frequency, primarily in patients with mild symptoms.",
        "Q: What is the expected impact of Drug F on mortality rates in diabetic patients over 5 years?\nA: The trial data indicates a 5% reduction in mortality rates for patients on Drug F over a 5-year period."
    ]
}

def construct_prompt(query, query_type, relevant_section_text, section_name):
    section_context = f"You are reading the {section_name} section of a clinical trial."
    
    examples = '\n\n'.join(few_shot_examples[query_type])
    
    prompt = f"{section_context}\n\nRelevant Section: {relevant_section_text}\n\n" \
             f"{examples}\n\nQ: {query}\nA:"
    
    return prompt

