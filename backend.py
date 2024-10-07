import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain


groq = st.secrets["Groq_API_Key"]


llm = ChatGroq(
    model="llama-3.1-70b-versatile",
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
   
    template = """As a project manager, provide detailed instructions for gathering initial requirements for this project:

        Project Description: {project_description}

        Your task:
        1. Analyze the project description
        2. Identify key stakeholders
        3. List 5-7 specific areas to focus on for requirements gathering
        4. Provide 3-5 targeted questions for each area
        5. Suggest any potential challenges or considerations

        Please provide a structured response with clear headings and bullet points."""
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
    
    template = """As a stakeholder interviewer, conduct simulated interviews based on these instructions and provide initial requirements:

        Instructions: {instructions}

        Your task:
        1. Simulate interviews with key stakeholders identified
        2. For each stakeholder:
            a. Introduce the stakeholder (role, perspective)
            b. List 5-7 key requirements they might have
            c. Provide any concerns or constraints they might mention
        3. Summarize common themes across all interviews
        4. Highlight any conflicting requirements between stakeholders

        Please provide a structured response with clear headings for each stakeholder and a summary section."""
        
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
    template = """As a requirements analyzer, refine and categorize these initial requirements:

        Initial Requirements: {initial_requirements}

        Your task:
        1. Categorize requirements into:
            a. Functional Requirements
            b. Non-Functional Requirements
            c. Technical Requirements
            d. User Interface Requirements
            e. Security Requirements
        2. For each category:
            a. List and number each requirement
            b. Prioritize requirements (High, Medium, Low)
            c. Identify any dependencies between requirements
        3. Highlight any ambiguous or conflicting requirements
        4. Suggest 3-5 additional requirements that might have been overlooked

        Please provide a structured response with clear headings for each category and a summary of key findings."""
        
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
    template = """As a documentation specialist, compile a final requirements document based on these refined requirements:

        Refined Requirements: {refined_requirements}

        Your task:
        1. Create an executive summary (2-3 paragraphs)
        2. Provide a table of contents
        3. For each category of requirements:
            a. Provide a brief introduction
            b. List all requirements in a numbered format
            c. Include priority and any dependencies for each requirement
        4. Create a glossary of technical terms used
        5. Add a section on assumptions and constraints
        6. Include a section on future considerations or potential enhancements

        Please format the document with clear headings, subheadings, and use bullet points or numbered lists where appropriate."""
        
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
