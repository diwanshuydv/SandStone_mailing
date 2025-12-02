# linkedin_analyzer.py

import os
import google.generativeai as genai

def get_gemini_analysis(profile_data: str, company_name) -> str:
    """
    Analyzes a LinkedIn profile using the Gemini API.

    Args:
        profile_data: A string containing the scraped text of a LinkedIn profile.

    Returns:
        A string containing the AI-generated analysis, or an error message.
    """
    try:
        # --- 1. CONFIGURE YOUR API KEY ---
        # It's best practice to set your API key as an environment variable
        # to avoid hardcoding it in your script.
        # api_key = os.environ.get("GEMINI_API_KEY")
        # if not api_key:
        #     return "Error: GEMINI_API_KEY environment variable not set. Please set it to your API key."
            
        genai.configure(api_key="YOUR_API_KEY")

        # --- 2. INITIALIZE THE MODEL ---
        # Using the 'gemini-1.5-flash' model for speed and efficiency.
        # You can also use 'gemini-pro' or other available models.
        model = genai.GenerativeModel('gemini-2.0-flash-lite')

        # --- 3. CRAFT A DETAILED PROMPT ---
        # A good prompt is key to a good response.
        # We are giving the AI a role, context, the data, and instructions for the output format.
        prompt = f"""
 ROLE: You are an expert outreach assistant for a prestigious tech conclave. Your task is to generate two highly personalized paragraphs for an email invitation, based on the provided profile data.

CONTEXT: The email invites a distinguished professional to be a speaker at the "Sandstone Summit 5.0" at IIT Jodhpur.

Event Theme: "Innovate Today, Influence Tomorrow: Reimagining the Tech Landscape for a Sustainable Future."

Event Sub-themes: Ethical AI, Global Collaboration in Innovation, Data for Good, Green Tech Frontiers.

INSTRUCTIONS:

Analyze Input: Parse the provided unstructured profile_data. Extract the individual's key accomplishments, areas of expertise, and their current company name. Ignore any HTML tags or irrelevant text.

Generate Paragraph 1:

Craft a concise paragraph (under 100 words).

Directly address the recipient using pronouns like "you" and "your".

Specifically connect their expertise (e.g., in AI, sustainable tech, data-driven solutions) to the summit's main theme or one of its sub-themes. This connection is the core reason for the invitation.

Summarize their contributions in a generalized way that doesn't sound like a direct copy from their profile.

Generate Paragraph 2:

Use the following template exactly.

Identify the person's company from the profile_data and insert it into the {company_name} placeholder.

Template: "In this journey, your presence as a distinguished speaker would be invaluable. Your insights can inspire ideas, encourage dialogue, and leave a lasting impact on our audience while also strengthening the relationship between IIT Jodhpur and ____{company_name}."

CRITICAL OUTPUT RULES:

Your final output must consist of ONLY the two generated paragraphs with JUST SINGLE LINE SEPERATION BETWEEN THEM !!

Do NOT include any titles, labels (e.g., 'Paragraph 1'), introductory phrases (e.g., 'Here are the paragraphs'), or any other explanatory text.

The entire response must be formatted and ready for direct insertion into the email's {{PERSONALIZED_PARAGRAPH}} placeholder.

INPUT DATA: {profile_data}

        """

        # --- 4. GENERATE THE CONTENT ---
        response = model.generate_content(prompt)
        
        # --- 5. RETURN THE RESPONSE ---
        return response.text

    except Exception as e:
        return f"An unexpected error occurred: {e}"

# --- MAIN EXECUTION BLOCK ---
if __name__ == "__main__":
    # --- PASTE YOUR SCRAPED LINKEDIN PROFILE DATA HERE ---
    # This is an example. Replace the entire multi-line string with your data.
    linkedin_profile_data = """
   
    """

    print("Analyzing LinkedIn Profile... Please wait.")
    print("-" * 40)

    analysis_result = get_gemini_analysis(linkedin_profile_data, "Google")

    print(analysis_result)
    print("-" * 40)
