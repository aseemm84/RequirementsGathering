# backend.py
from time import sleep

import cohere
import streamlit as st

co = cohere.Client(st.secrets["COHERE_API_KEY"])

def project_manager_agent(project_description, temperature, **kwargs):
    """
    Acts as a project manager to provide instructions for gathering initial requirements.

    Args:
        project_description: A description of the project.
        temperature: Controls the creativity of the AI response.
        **kwargs: Additional keyword arguments for refining the prompt.

    Returns:
        Instructions for gathering initial requirements.
    """
    try:
        prompt = f"""As a project manager, provide detailed instructions for gathering initial requirements for this project:

        Project Description: {project_description}

        Your task:
        1. Analyze the project description
        2. Identify key stakeholders
        3. List 5-7 specific areas to focus on for requirements gathering
        4. Provide 3-5 targeted questions for each area
        5. Suggest any potential challenges or considerations

        Please provide a structured response with clear headings and bullet points."""
        
        # Add any refinements to the prompt based on kwargs
        if kwargs:
            prompt += f"\n\nRefinement Instructions: {kwargs.get('refinement_instructions')}"

        response = co.chat(
            model="command-r-plus",
            message=prompt,
            temperature=temperature
        )
        return response.text
    except cohere.CohereError as e:
        st.error(f"Project Manager Agent Error: {e}")
        return "Error occurred during project manager agent processing."


def stakeholder_interview_agent(instructions, temperature, **kwargs):
    """
    Simulates stakeholder interviews to gather initial requirements.

    Args:
        instructions: Instructions from the project manager agent.
        temperature: Controls the creativity of the AI response.
        **kwargs: Additional keyword arguments for refining the prompt.

    Returns:
        Initial requirements gathered from simulated stakeholder interviews.
    """
    try:
        prompt = f"""As a stakeholder interviewer, conduct simulated interviews based on these instructions and provide initial requirements:

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
        
        # Add any refinements to the prompt based on kwargs
        if kwargs:
            prompt += f"\n\nRefinement Instructions: {kwargs.get('refinement_instructions')}"

        response = co.chat(
            model="command-r-plus",
            message=prompt,
            temperature=temperature
        )
        return response.text
    except cohere.CohereError as e:
        st.error(f"Stakeholder Interview Agent Error: {e}")
        return "Error occurred during stakeholder interview agent processing."


def requirements_analyzer_agent(initial_requirements, temperature, **kwargs):
    """
    Refines and categorizes initial requirements.

    Args:
        initial_requirements: Initial requirements gathered from stakeholder interviews.
        temperature: Controls the creativity of the AI response.
        **kwargs: Additional keyword arguments for refining the prompt.

    Returns:
        Refined and categorized requirements.
    """
    try:
        prompt = f"""As a requirements analyzer, refine and categorize these initial requirements:

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
        
        # Add any refinements to the prompt based on kwargs
        if kwargs:
            prompt += f"\n\nRefinement Instructions: {kwargs.get('refinement_instructions')}"

        response = co.chat(
            model="command-r-plus",
            message=prompt,
            temperature=temperature
        )
        return response.text
    except cohere.CohereError as e:
        st.error(f"Requirements Analyzer Agent Error: {e}")
        return "Error occurred during requirements analyzer agent processing."


def documentation_agent(refined_requirements, temperature, **kwargs):
    """
    Compiles a final requirements document.

    Args:
        refined_requirements: Refined and categorized requirements.
        temperature: Controls the creativity of the AI response.
        **kwargs: Additional keyword arguments for refining the prompt.

    Returns:
        A formatted requirements document.
    """
    try:
        prompt = f"""As a documentation specialist, compile a final requirements document based on these refined requirements:

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
        
        # Add any refinements to the prompt based on kwargs
        if kwargs:
            prompt += f"\n\nRefinement Instructions: {kwargs.get('refinement_instructions')}"

        response = co.chat(
            model="command-r-plus",
            message=prompt,
            temperature=temperature
        )
        return response.text
    except cohere.CohereError as e:
        st.error(f"Documentation Agent Error: {e}")
        return "Error occurred during documentation agent processing."
