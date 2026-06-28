import json


def get_resume_prompt(resume_text):
    """
    Creates a structured prompt for Gemini AI.
    The AI must return ONLY valid JSON.
    """

    schema = {
        "ats_score": 0,
        "summary": "",
        "strengths": [],
        "weaknesses": [],
        "missing_skills": [],
        "recommended_jobs": [],
        "suggestions": []
    }

    return f"""
You are an expert ATS (Applicant Tracking System) and Senior HR Recruiter.

Analyze the resume below.

Return ONLY valid JSON.

Do NOT include markdown.
Do NOT use ```json.
Do NOT write explanations.

The JSON must follow exactly this structure:

{json.dumps(schema, indent=4)}

Resume:

{resume_text}
"""