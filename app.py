import os

import aspose.words as aw
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
# from md2pdf.core import md2pdf



load_dotenv()

st.set_page_config(layout="wide", page_title="BoldProp", page_icon="📋")


@st.cache_data(show_spinner=False)
def get_output_from_ai(prompt):
    system_prompt = "You are an expert in crafting proposals that turn prospects into clients. With a deep understanding of persuasive writing, market trends, and a touch of psychological insight, Your goal is to create a proposal that not only meets the needs of the clients, but exceeds their expectations. Generate a proposal using the following information. If a particular section does not have any input from the user, make up the real content for it based on the context provided."

    client = OpenAI()
    c = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    )

    # print(c['choices'][0]['message']['content'])
    output = c.choices[0].message.content

    return output


def save_prop_pdf():
    doc = aw.Document("./proposal.md")

    # Save the document as PDF
    doc.save(f"./proposal.pdf")


# Title
st.title("Proposal Generator")
# st.write(st.session_state)

# Inputs
our_name = st.text_input("Company Name:")
our_values = st.text_area("Our Company Values")
client_name = st.text_input("Client Name:")
client_values = st.text_area("Client Values/Principles:")
problem_statement = st.text_area("Problem Statement:")
price = st.text_area("Enter you price")
start_date = st.date_input("Project Start Date:")
end_date = st.date_input("Project End Date:")
scope_of_work = st.multiselect(
    "Scope of Work:",
    ["UI/UX Design", "Full-stack Development", "Content Writing", "Other"],
)
payment_terms = st.radio("Payment Terms:", ["Upfront", "Milestones", "Upon Completion"])
contact_info = st.text_input("Your Contact Information:")
support_terms = st.radio(
    "Support and Maintenance Terms:", ["3 Months", "6 Months", "12 Months"]
)
tech_requirements = st.multiselect(
    "Technical Requirements:", ["Python", "React", "AWS", "Other"]
)
target_audience = st.text_input("Client's Target Audience:")
uploaded_file = st.file_uploader("Attach Documents (Optional):")
success_metrics = st.text_area("Success Metrics:")


generate_button = st.button("Generate Proposal")

# Generate Proposal Button
if generate_button or st.session_state.get("submit_key"):
    st.session_state["submit_key"] = True
    # Customized prompt for GPT
    gpt_prompt = f"""
    Here are the inputs given by the user.
    - Our Company Name: {our_name}
    - Our Company Values: {our_values}
    - Client Name: {client_name}
    - Client Values/Principles: {client_values}
    - Problem Statement: {problem_statement}
    - Quoted Price: {price}
    - Project Timeline: From {start_date} to {end_date}
    - Scope of Work: {', '.join(scope_of_work)}
    - Payment Terms: {payment_terms}
    - Contact Information: {contact_info}
    - Support and Maintenance Terms: {support_terms}
    - Technical Requirements: {', '.join(tech_requirements)}
    - Client's Target Audience: {target_audience}
    - Success Metrics: {success_metrics}  
    The proposal should be professional, comprehensive, and tailored to the client's needs. 
    Create a markdown file separately for the proposal, use tables wherever possible for better readability.
    The proposal should have these sections.
    - Title Page: 
        Agency Name, Proposal Title, Client's Name, Date
    - Objective:
        High-level objectives of the app development project.
    - User Personas:
        User personas to ensure an understanding of the end users.
    - Technical Specifications:
        Tech stack, frameworks, and libraries to be used.
    - Development Methodology:
        Explain your development process.
    - Proof of Work:
        Showcase past successful projects.
    - Why choose us? 
        Unique Selling Proposition (USP).
        Testimonials.
    - Features and Functionality:
        A detailed breakdown of the app's features and functionalities.
    - Maintenance and Support:
        Details on post-development support and maintenance.
    - Collaboration and Communication:
        Tools and platforms for collaboration.
    - Deliverables:
        A clear list of all project deliverables.
    - Pricing:
        Itemised pricing and possible additional costs.
    - Payment Terms:
        Milestones, invoicing, and payment schedules.
    - Next Steps:
        Clearly defined actions for the client to move forward.
    - Contact Information.

    
     Add a divider between each section.
    """
    # st.write("### GPT Prompt for Proposal Generation")
    # st.write(gpt_prompt)

    with st.spinner(text="Generating your proposal, Please Wait"):
        output = get_output_from_ai(prompt=gpt_prompt)

if "submit_key" in st.session_state and st.session_state["submit_key"]:
    st.header("Your Proposal")
    col1, col2 = st.columns([1, 2])
    editable_text = col1.text_area(label="Generated Proposal", value=output, height=700)
    col2.markdown(body=editable_text)

    editable_text_bytes = editable_text.encode(encoding="utf-8")

    with open("proposal.md", mode="wb") as f:
        f.write(editable_text_bytes)

    st.download_button(
        label="Download Proposal",
        data=editable_text_bytes,
        file_name="proposal.md",
        # on_click=save_prop_pdf,
    )

    css = """
    <style>
        [data-testid="stMarkdown"]{
            overflow: auto;
            height: 110vh;
        }
    </style>
    """

    st.markdown(css, unsafe_allow_html=True)
