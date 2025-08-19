from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model_name='llama3-70b-8192'
)


def findStakeholder(problem_statement):
    
    prompt = ChatPromptTemplate.from_template("""
    ## Introduction:
    Imagine you are a **requirement analyst** working on defining stakeholders and end users for the given problem statement. Your goal is to identify all individuals or groups who interact with or are impacted by this system.

    ## Problem Statement:
    {problem_statement}

    To build this system efficiently, we need to first **identify key stakeholders and end users**.

    ## Task:
    - Identify and categorize **all relevant stakeholders** interacting with or impacted by the system.
    - Differentiate between **primary end users** (direct users) and **secondary stakeholders** (indirectly affected users).

    ## Instructions:
    1. **Classify stakeholders** into **primary (direct users)** and **secondary (indirect users)**.
    2. For each category, provide:
    - Their **role** in using or managing the system.
    - Their **expectations and concerns** about the system.
    3. Identify **any potential conflicts** between stakeholders and suggest how they can be resolved.
    4. Consider **external regulatory bodies** if applicable.

    ## Closing:
    Now that we have identified the key stakeholders and end users, the next step is to **apply elicitation techniques** such as **interviews, surveys, and observations** to gather detailed insights. This will help refine the system requirements and ensure it meets user needs effectively.
    """)


    prompt_template = prompt.format(problem_statement=problem_statement)


    example = f"""
    AI:
    {prompt_template}

    HUMAN:
    Give me a list of "stakeholders" and "endUsers" separately.

    AI:
    """


    stakeholders_response = llm.invoke(example).content


    print("\n===== Stakeholders & End Users =====\n")
    print(stakeholders_response)
    return stakeholders_response

def generateElicitationTechniques(Stakeholder):

    # Define a well-structured prompt for elicitation techniques
    prompt = ChatPromptTemplate.from_template(f"""
    ## **Introduction:**
    You are a **requirements analyst** tasked with selecting the best **elicitation techniques** for gathering system requirements from the identified **stakeholders and end users**.

    ## **Identified Stakeholders:**
    {Stakeholder}

    ## **Task:**
    1. Based on the **list of stakeholders**, recommend the most appropriate **elicitation technique(s)** for each stakeholder group.
    2. Provide a **justification** explaining why the chosen technique is the best fit for capturing their requirements.
    3. Present the results in a **structured table format** with:
    - **Stakeholder Name**
    - **Elicitation Techniques (e.g., interviews, surveys, observations, prototyping, focus groups, workshops, etc.)**
    - **Justification for Choosing the Technique**

    ## **Instructions:**
    1. Assign **at least one elicitation technique** per stakeholder group.
    2. Justify why the selected technique is **appropriate** based on their role, responsibilities, and influence over the system.
    3. Ensure recommendations cover **both functional and non-functional requirements**.

    ## **Closing:**
    Once the elicitation techniques are identified, the next step is to **apply them in real-world scenarios** to refine the system requirements and enhance user experience.
    """)

    # Format the prompt
    prompt_template = prompt.format()

    # Example user interaction
    example = f"""
    AI:
    {prompt_template}

    HUMAN:
    Generate a structured list of elicitation techniques for each stakeholder with justifications.

    AI:
    """

    # Get the AI response
    elicitation_techniques_response = llm.invoke(example).content

    # Print the output in a readable format
    print("\n===== Elicitation Techniques & Justifications =====\n")
    print(elicitation_techniques_response)
    return elicitation_techniques_response


def justificationElicitationTechnique(ElicitationTechnique):

    # Define a refined prompt
    prompt = ChatPromptTemplate.from_template(f"""
    ## **Introduction:**
    You are a **requirements analyst** responsible for evaluating and explaining the **effectiveness** of the selected **elicitation techniques** used for gathering system requirements in the **NewYork Ticket Distributor System**.

    ## **Elicitation Techniques Mapping:**
    {ElicitationTechnique}

    ## **Task:**
    For each stakeholder, provide:
    1. A **clear justification** for why the chosen elicitation technique is the best fit.
    2. An explanation of **how this technique ensures effective requirement gathering**.
    3. If applicable, suggest any **alternative techniques** that might also be suitable.

    ## **Instructions:**
    1. Justify the **selected technique** for each stakeholder by explaining **why it is the most effective**.
    2. Describe **how this technique helps extract meaningful and actionable system requirements**.
    3. If applicable, recommend **alternative elicitation methods** that could enhance the requirement-gathering process.

    ## **Closing:**
    By using **the right elicitation techniques**, we ensure that **all stakeholder needs are accurately captured**. The next step is to **refine user stories and validate the gathered requirements** to align them with system goals.
    """)

    # Format the prompt
    prompt_template = prompt.format()

    # Example user interaction
    example = f"""
    AI:
    {prompt_template}

    HUMAN:
    Provide a detailed justification of why each elicitation technique is effective and how it helps in gathering requirements.

    AI:
    """

    # Get the AI response
    Elicitationjustification = llm.invoke(example).content  

    # Print the output in a readable format
    print("\n===== Justification for Elicitation Techniques =====\n")
    print(Elicitationjustification)
    return Elicitationjustification


def generateUserStories(Stakeholder):

    # Define the improved prompt
    prompt = ChatPromptTemplate.from_template(f"""
    ## **Introduction:**
    You are a **requirements analyst** responsible for defining the **functionalities** by creating **detailed user stories**. Each user story should clearly describe system interactions, covering both **successful operations and potential failure scenarios**.

    ## **Stakeholders & Users:**
    {Stakeholder}

    ## **Task:**
    For each type of user, generate **at least 15 user stories**, ensuring that every story includes:

    1. **A clear user story format** following the **Front & Back of the Card** approach.
    2. **Detailed success scenarios** covering all possible correct system behaviors.
    3. **Failure scenarios with display messages**, explicitly listing:
    - **System failures** (e.g., backend issues, transaction errors).
    - **User input errors** (e.g., incorrect card details, invalid selections).
    - **Hardware malfunctions** (e.g., printer errors, touchscreen unresponsive).
    - **Security concerns** (e.g., fraud detection, unauthorized access).

    ## **Instructions:**
    1. **Generate at least 15 user stories** for different users (Passengers, Metro Staff, Administrators, Maintenance Team).
    2. **Ensure success and failure cases are fully detailed** for each user story.
    3. **Each failure scenario must be explicitly listed with a clear user-friendly message**.
    4. **Avoid reusing previous failure lists—every user story must have its own detailed breakdown.**

    ## **Closing:**
    By defining these functionalities in **well-structured user stories**, we ensure a **clear understanding of system requirements**. The next step is to **validate and refine these stories before implementation**.
    """)

    # Format the prompt
    prompt_template = prompt.format()

    # Example user interaction
    example = f"""
    AI:
    {prompt_template}

    HUMAN:
    Generate a **list of 15 user stories** ensuring **detailed success and failure scenarios** with display messages for each failure case.

    AI:
    """

    # Get the AI response
    user_stories = llm.invoke(example).content

    # Print the output in a readable format
    print("\n===== User Stories for Ticket Distributor System =====\n")
    print(user_stories)
    return user_stories


def checkInvestFramework(user_stories):

    prompt = ChatPromptTemplate.from_template(f"""
    ## **Introduction:**
    You are an **Agile Coach & Requirements Analyst**, responsible for **validating the user stories** using the **INVEST framework**. Your goal is to ensure that each user story meets agile best practices and is ready for development.

    ## **User Stories for Validation:**
    {user_stories}

    ## **Task:**
    For each user story, **apply the INVEST framework validation** and provide a **detailed breakdown** of strengths and weaknesses using the format below.

    ---

    ## **INVEST Validation Format:**

    ### **Front of the Card:**
    _As a [user role], I want to [goal] so that [benefit]._

    ### **Back of the Card:**
    1. **Validation Results:**
    - **Independent:** (Pass/Fail) + Justification
    - **Negotiable:** (Pass/Fail) + Justification
    - **Valuable:** (Pass/Fail) + Justification
    - **Estimable:** (Pass/Fail) + Justification
    - **Small:** (Pass/Fail) + Justification
    - **Testable:** (Pass/Fail) + Justification

    2. **Suggested Improvements (if needed):**
    - Provide **specific recommendations** if a criterion **fails**, ensuring the user story aligns with INVEST principles.

    ---

    ## **Instructions:**
    1. **Validate all user stories provided above** using the **INVEST framework**.
    2. **Clearly state Pass/Fail** for each criterion and provide justifications.
    3. **Suggest specific improvements** where necessary to align with agile best practices.
    4. **Put This **---** before all the userstories**.

    ## **Closing:**
    By validating these user stories against the **INVEST framework**, we ensure they are **clear, well-structured, and ready for agile development**. The next step is to refine any weak stories and move them into the development backlog.
    """)

    # Format the prompt
    prompt_template = prompt.format()

    # Example user interaction
    example = f"""
    AI:
    {prompt_template}

    HUMAN:
    Validate the following **user stories** using the **INVEST framework**, and provide detailed feedback. **Strictly do this task for all 15 user stories** also **follow front and back of the card format**.

    AI:
    """

    # Get the AI response
    invest_validations = llm.invoke(example).content

    # Print the output in a readable format
    print("\n===== INVEST Validation Results =====\n")
    print(invest_validations)
    return invest_validations


def Prioritize(final_validated_output):
    prompt = ChatPromptTemplate.from_template(f"""
    Introduction:
    Act as an Agile Coach & Requirements Analyst. Your task is to analyze and categorize the validated user stories using the MoSCoW prioritization method.

    ---

    Validated User Stories:
    {final_validated_output}

    ---

    Task:
    1. Review each validated user story and assign a priority level based on the MoSCoW method:
    - Must-have (M): Essential for core system functionality; required in the first release.
    - Should-have (S): Important but not immediately necessary; can be implemented in a later phase.
    - Could-have (C): Enhances user experience or efficiency; beneficial but not critical.
    - Won’t-have (W): Not required for this release; can be reconsidered in future updates.

    2. Justify each classification based on the following factors:
    - Business Value: How critical is this feature to end users and stakeholders?
    - Urgency: Does this feature need immediate implementation?
    - Feasibility: How complex is the technical implementation?
    - Security & Compliance: Does this impact data protection or legal regulations?
    - Performance & Usability: Will this affect system efficiency and user experience?
    - Dependencies: Does this feature rely on or enable other functionalities?

    3. Present the prioritized user stories in the following format:

    ---

    MoSCoW Prioritization Format:

    User Story:
    "As a [user role], I want to [goal] so that [benefit]."

    MoSCoW Classification:
    - **Priority:** Must-have (M) / Should-have (S) / Could-have (C) / Won’t-have (W)
    - **Justification:** Explain why this priority was assigned based on business value, urgency, feasibility, security, performance, and dependencies.

    ---

    Example Prioritization:

    User Story:
    "As a passenger, I want to log in with my credentials so that I can access my account securely."

    MoSCoW Classification:
    - **Priority:** Must-have (M)
    - **Justification:**
    - Business Value: Essential for authentication and security (5/5).
    - Urgency: Required before any other feature (5/5).
    - Feasibility: Well-established implementation methods (5/5).
    - Security & Compliance: High (5/5) due to user credential protection.
    - Performance & Usability: Low impact on system performance (4/5).
    - Dependencies: Required for all account-related features (5/5).

    ---

    Instructions:
    1. Apply MoSCoW prioritization to all validated user stories.
    2. Justify each priority level based on the factors listed above.
    3. Ensure security, compliance, and performance considerations are reflected.
    4. Structure the output clearly as shown in the example.

    ---

    Closing:
    By prioritizing user stories using the MoSCoW method, we ensure that essential functionalities are developed first while balancing business value, technical feasibility, and user needs. 

    """)

    # Generate formatted prompt
    prompt_template = prompt.format()
    example = f"""
    AI :
    {prompt_template}

    HUMAN :
    Using the MoSCoW method, prioritize the following validated user stories by considering business value, security, feasibility, urgency, and performance. **Strictly give me for all the user stories**

    AI :
    """

    # Get the AI response
    prioritize = llm.invoke(example).content
    print(prioritize)
    return prioritize


def findEpicConflict(final_validated_output):
    prompt = ChatPromptTemplate.from_template(f"""

    ### Validated User Stories:
    {final_validated_output}

    ---

    ### Task:
    1. **Group related user stories into EPICs** based on broader functionalities.
    2. **Identify at least three EPICs** where conflicts exist between different user stories.
    3. **Analyze the nature of the conflict** within each EPIC, considering:
    - **Functional conflicts** (e.g., conflicting feature requirements)
    - **Non-functional conflicts** (e.g., security vs. usability)
    - **Resource conflicts** (e.g., system performance vs. cost)
    - **Stakeholder conflicts** (e.g., different priorities among user groups)
    4. **Propose a resolution strategy** that balances user needs, technical feasibility, and business priorities.
    5. **Present the findings in the following format:**

    ---

    ### EPIC Conflict Analysis Format:

    #### **EPIC Name: [Broad Functionality]**
    - **Conflicting User Stories:**
    - Story 1: _As a [user], I want to [goal] so that [benefit]._
    - Story 2: _As a [user], I want to [goal] so that [benefit]._
    - **Conflict Type:** [Functional / Non-functional / Resource / Stakeholder]
    - **Conflict Analysis:**
    - Describe the nature of the conflict and its impact on system design.
    - **Resolution Strategy:**
    - Provide a feasible solution that aligns with business objectives and technical constraints.

    ---

    ### Example Conflict Resolution

    #### **EPIC: Secure User Access**
    - **Conflicting User Stories:**
    - _As a passenger, I want to log in using biometric authentication so that I can access my account quickly._
    - _As an admin, I want strict two-factor authentication so that unauthorized users cannot access the system._
    - **Conflict Type:** Security vs. Usability
    - **Conflict Analysis:**
    - Biometric authentication improves user experience but may not meet regulatory security requirements.
    - Two-factor authentication enhances security but may cause friction for frequent passengers.
    - **Resolution Strategy:**
    - Implement **adaptive authentication**, where high-risk actions require 2FA while low-risk logins allow biometrics.

    ---

    ### Instructions:
    1. Identify **three EPICs** where conflicts exist.
    2. Clearly describe the **conflict type and analysis** of the problem.
    3. Propose **practical resolution strategies** to balance competing requirements.

    ---

    ### Closing:
    By resolving these requirement conflicts, we ensure that the System is designed to meet both **user needs and technical constraints**, resulting in a scalable and efficient solution.

    """)

    # Generate formatted prompt
    prompt_template = prompt.format()
    example = f"""
    AI :
    {prompt_template}

    HUMAN :
    Analyze the validated user stories and identify three EPICs (or collections of related user stories) where conflicts exist in the System. Provide a detailed analysis of each conflict and suggest resolution strategies. **Strictly the output must be complete and well structured**

    AI :
    """

    # Get the AI response
    epics = llm.invoke(example).content
    print(epics)
    return epics



def main():
    Stakeholder = findStakeholder("Create a system to build LLM?")
    ElicitationTechnique = generateElicitationTechniques(Stakeholder)
    ElicitationJustification = justificationElicitationTechnique(ElicitationTechnique)

    UserStories = generateUserStories(Stakeholder)
    InvestFramework = checkInvestFramework(UserStories)
    PrioritizeUS = Prioritize(InvestFramework)
    EpicsAndConflict = findEpicConflict(InvestFramework)


if __name__=='__main__':
    main()