import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import re


groq = st.secrets["Groq_API_Key"]

def get_llm(temperature): 
    """
    Returns an instance of the ChatGroq LLM with the specified temperature.
    """
    return ChatGroq(
        model="llama-3.1-70b-versatile",
        groq_api_key=groq,
        temperature=temperature,
        max_tokens = 7000
        # other params...
    )

def check_for_rate_limit_error(response_content):
    """Checks if the response content contains a Groq rate limit error."""
    error_pattern = r"Rate limit reached.*in (\d+m\d+\.\d+s)"
    match = re.search(error_pattern, response_content)
    if match:
        wait_time = match.group(1)
        # Return an error message string instead of using st.error
        return f"This app uses free Groq API. API call Rate limit exceeded. Please try again in {wait_time}."
    return False

def project_manager_agent(project_description, temperature):
    """
    Acts as a project manager to provide instructions for gathering initial requirements.

    Args:
        project_description: A description of the project.
        temperature: Controls the creativity of the AI response.

    Returns:
        Instructions for gathering initial requirements.
    """
   
    template = """As a project manager, provide detailed instructions for gathering initial requirements for this project, keeping in mind the structure of a typical Functional Requirements Document (FRD):

        Project Description: {project_description}

        Your task:
        1. Analyze the project description.
        2. Identify key stakeholders (roles, departments, external entities).
        3.  Suggest appropriate methods for gathering requirements from each stakeholder (e.g., interviews, workshops, questionnaires, document analysis).
        4.  List 5-7 specific areas to focus on for requirements gathering, aligning with common FRD sections (e.g., User Interface, Functionality, Security, Performance, etc.).
        5. Provide 3-5 targeted questions for each area to elicit detailed requirements.
        6. Suggest any potential challenges or considerations for the requirements gathering process.

        Please provide a structured response with clear headings and bullet points."""
    llm = get_llm(temperature)
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm
    
    try:
        response = chain.invoke({"project_description": project_description})
        # Check for rate limit error in the response content
        error_message = check_for_rate_limit_error(response.content) 
        if error_message:
            return error_message # Return the error string
        else: 
            return response.content
    except Exception as e:
        error_message = check_for_rate_limit_error(str(e))
        if error_message:
            return error_message # Return the error string
        else: 
            return f"An error occurred: {e}"


def stakeholder_interview_agent(instructions, temperature):
    """
    Simulates stakeholder interviews to gather initial requirements.

    Args:
        instructions: Instructions from the project manager agent.
        temperature: Controls the creativity of the AI response.

    Returns:
        Initial requirements gathered from simulated stakeholder interviews.
    """
    
    template = """As a stakeholder interviewer, conduct simulated interviews based on these instructions and provide initial requirements, keeping in mind the structure of a typical FRD:

        Instructions: {instructions}

        Your task:
        1. Simulate interviews with the key stakeholders identified in the instructions.
        2. For each stakeholder:
            a. Introduce the stakeholder (role, perspective, concerns).
            b. Based on the areas and questions provided, generate realistic responses capturing their potential requirements.
            c. Include any constraints or specific needs they might mention.
        3. Summarize common themes and potential conflicts or misalignments in requirements across stakeholders.

        Please provide a structured response with clear headings for each stakeholder and a summary section."""
    llm = get_llm(temperature)    
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm
    
    try:
        response = chain.invoke({"instructions": instructions})
        # Check for rate limit error in the response content
        error_message = check_for_rate_limit_error(response.content) 
        if error_message:
            return error_message # Return the error string
        else: 
            return response.content
    except Exception as e:
        error_message = check_for_rate_limit_error(str(e))
        if error_message:
            return error_message # Return the error string
        else: 
            return f"An error occurred: {e}"


def requirements_analyzer_agent(initial_requirements, temperature):
    """
    Refines and categorizes initial requirements.

    Args:
        initial_requirements: Initial requirements gathered from stakeholder interviews.
        temperature: Controls the creativity of the AI response.

    Returns:
        Refined and categorized requirements.
    """
    template = """As a requirements analyst, refine and categorize these initial requirements into a structure suitable for an FRD:

        Initial Requirements: {initial_requirements}

        Your task:
        1.  Review the initial requirements gathered from stakeholder interviews.
        2.  Categorize requirements into standard FRD sections (e.g., Functional, Non-Functional, UI, Security, Performance, Data, etc.).
        3. For each category:
            a. List and number each requirement clearly and concisely.
            b. Prioritize requirements (High, Medium, Low) based on stakeholder input and project goals.
            c. Identify any dependencies between requirements.
        4. Highlight any ambiguous, conflicting, or incomplete requirements.
        5. Suggest 3-5 additional requirements that might have been overlooked.

        Please provide a structured response with clear headings for each category and a summary of key findings."""
    llm = get_llm(temperature)    
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm
    
    try:
        response = chain.invoke({"initial_requirements": initial_requirements})
        # Check for rate limit error in the response content
        error_message = check_for_rate_limit_error(response.content) 
        if error_message:
            return error_message # Return the error string
        else: 
            return response.content
    except Exception as e:
        error_message = check_for_rate_limit_error(str(e))
        if error_message:
            return error_message # Return the error string
        else: 
            return f"An error occurred: {e}"



def documentation_agent(refined_requirements, temperature):
    """
    Compiles a final requirements document.

    Args:
        refined_requirements: Refined and categorized requirements.
        temperature: Controls the creativity of the AI response.

    Returns:
        A formatted requirements document.
    """
    template = """
    
    ou are an expert technical writer specializing in creating clear, concise, and comprehensive Functional Requirements Documents (FRDs).

**Your task is to generate an FRD based on the analyzed requirements {refined_requirements}.**


**Instructions:**

1. **Structure:** Adhere to a standard FRD structure, including:
    *   **Introduction:** Briefly describe the project and its purpose. Define the scope of the system and the intended audience for this document. Include any relevant definitions or acronyms.
    *   **Overall Description:** Provide context for the system, including its users, environment, and any assumptions or constraints.
    *   **Specific Requirements:**  Detail the functional and non-functional requirements, organized by category (e.g., Functionality, User Interface, Security, Performance, Data).
    *   **Other Requirements:**  Include any legal, regulatory, or operational requirements.

2. **Clarity:**  Ensure all requirements are:
    *   **Atomic:** Each requirement should express a single, specific need.
    *   **Concise:** Use clear and unambiguous language, avoiding jargon.
    *   **Testable:**  Formulate requirements so they can be objectively verified.
    *   **Traceable:**  Where possible, link requirements back to the original stakeholder input.

3. **Completeness:**
    *   Address all the requirements provided in the input.
    *   Resolve any identified ambiguities or conflicts. If unable to resolve, clearly highlight them in the FRD with proposed solutions or options.
    *   Incorporate any suggested additional requirements from the input, if deemed relevant.

4. **Formatting:**
    *   Use a professional and easy-to-read format.
    *   Number requirements for easy reference.
    *   Use tables, diagrams, or other visual aids where appropriate to enhance understanding.

**Example of how to present a requirement:**

**3.1 Functionality**

*   **FR-001 (High):** The system shall allow users to create new accounts with a unique username and password.
*   **FR-002 (Medium):** The system shall provide a "forgot password" functionality allowing users to reset their passwords via email.

**Deliverables:**

A complete and well-structured FRD document ready for review by stakeholders.
    
    """
    llm = get_llm(temperature)    
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm
    
    try:
        response = chain.invoke({"refined_requirements": refined_requirements})
        # Check for rate limit error in the response content
        error_message = check_for_rate_limit_error(response.content) 
        if error_message:
            return error_message # Return the error string
        else: 
            return response.content
    except Exception as e:
        error_message = check_for_rate_limit_error(str(e))
        if error_message:
            return error_message # Return the error string
        else: 
            return f"An error occurred: {e}"

def process_requirements(project_description, temperature, status_callback):
    """
    Orchestrates the entire requirements gathering process.

    Args:
        project_description: A description of the project.
        temperature: Controls the creativity of the AI responses.
        status_callback: A function to update the status of the process.

    Returns:
        A dictionary containing the results from each agent.
    """
      
    try:
        status_callback("Project Manager Agent: Generating instructions...")
        pm_instructions = project_manager_agent(project_description, temperature)

        status_callback("Stakeholder Interview Agent: Gathering initial requirements...")
        initial_requirements = stakeholder_interview_agent(pm_instructions, temperature)

        status_callback("Requirements Analyzer Agent: Refining and categorizing requirements...")
        refined_requirements = requirements_analyzer_agent(initial_requirements, temperature)

        status_callback("Documentation Agent: Compiling final document...")
        final_document = documentation_agent(refined_requirements, temperature)

        return {
            "pm_instructions": pm_instructions,
            "initial_requirements": initial_requirements,
            "refined_requirements": refined_requirements,
            "final_document": final_document
        }
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None
