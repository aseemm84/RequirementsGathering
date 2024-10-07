import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain


groq = st.secrets["Groq_API_Key"]

def get_llm(temperature): 
    """
    Returns an instance of the ChatGroq LLM with the specified temperature.
    """
    return ChatGroq(
        model="gemma-7b-it",
        groq_api_key=groq,
        temperature=temperature
        # other params...
    )



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
        return response.content
    except Exception as e:
        return f"Error: {str(e)}"


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
        return response.content
    except Exception as e:
        return f"Error: {str(e)}"


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
        return response.content
    except Exception as e:
        return f"Error: {str(e)}"



def documentation_agent(refined_requirements, temperature):
    """
    Compiles a final requirements document.

    Args:
        refined_requirements: Refined and categorized requirements.
        temperature: Controls the creativity of the AI response.

    Returns:
        A formatted requirements document.
    """
    template = """As a documentation specialist, compile a functional requirements document (FRD) based on these refined requirements:

        Refined Requirements: {refined_requirements}

        Your task:
        1. Create a concise and informative executive summary (2-3 paragraphs) highlighting the project's purpose and key features.
        2. Provide a comprehensive table of contents in a proper readable fromat. Ensure each item in the table of contents start in a new line.
        3. Structure the FRD with clear sections and headings, following industry best practices.
        4. Ensure the structure of the Functional Requirements Document should be a real world structure often prepared by the business analysts in big and professional organisations.
        5. For each section in the document:
            a. Provide a brief introduction to the section.
            b. Provide proper numbering, font size and other formatting requirements as per the industry best practices.
        6. Define all technical terms in a glossary.
        7. Clearly state any assumptions and constraints that may impact development or implementation.

        Please format the document professionally with clear headings, subheadings, and use bullet points or numbered lists where appropriate. Ensure the language is precise, unambiguous, and easy to understand for both technical and non-technical stakeholders."""
    llm = get_llm(temperature)    
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm
    
    try:
        response = chain.invoke({"refined_requirements": refined_requirements})
        return response.content
    except Exception as e:
        return f"Error: {str(e)}"

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
