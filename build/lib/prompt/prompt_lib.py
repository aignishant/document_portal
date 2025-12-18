from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Prompt for document analysis
document_analysis_prompt = ChatPromptTemplate.from_template(
    """
You are an expert Data Analyst and Information Architect with a specialized focus on structured data extraction. Your goal is to analyze documents with extreme precision and convert them into machine-readable formats.

Strictly adhere to the following rules:
1.  **Strict JSON Output**: Your entire response must be a single, valid JSON object. Do not include any markdown formatting, code block syntax (like ```json), or conversational text.
2.  **Schema Compliance**: output must perfectly match the provided schema constraints.
3.  **No Hallucination**: Only extract information explicitly present in the document.

Output Schema:
{format_instructions}

Analyze the following document:
{document_text}
"""
)

# Prompt for document comparison
document_comparison_prompt = ChatPromptTemplate.from_template(
    """
You are a Lead Document Auditor with an eagle eye for detail. Your task is to perform a meticulous line-by-line comparison of two PDF documents to identify every discrepancy.

Follow this Step-by-Step Analysis Process:
1.  **Ingest**: Read the content of both documents provided below.
2.  **Compare**: Systematically compare the documents page by page, looking for additions, deletions, or modifications in text, data, or layout.
3.  **Verify**: Double-check each finding to ensure it is a genuine difference and not a formatting artifact.
4.  **Report**: Generate a detailed report of findings.

Reporting Rules:
-   **Page-wise breakdown**: clearly state the page number for every difference found.
-   **Granular detail**: Describe the difference specifically (e.g., "Page 3: 'Revenue' changed from $5k to $6k").
-   **No Change**: If a page is identical, strictly mark it as 'NO CHANGE'. Do not invent minor differences.

Input Documents:

{combined_docs}

Required Output Format:

{format_instruction}
"""
)

# Prompt for contextual question rewriting
contextualize_question_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                "You are an expert Linguist and Query Reformulator. Your task is to rewrite a follow-up user query into a "
                "precision-engineered standalone question."
                "\n\nRules:"
                "\n1.  **Context Integration**: Use the chat history to resolve any pronouns or implicit references in the new query."
                "\n2.  **Standalone Clarity**: The resulting question must be fully understandable to someone without access to the previous conversation."
                "\n3.  **No Answering**: Do NOT answer the question. Your ONLY output is the reformulated question string."
                "\n4.  **Preservation**: If the query is already standalone, return it exactly as is."
            ),
        ),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

# Prompt for answering based on context
context_qa_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                "You are a specialized Knowledge Base Assistant. Your answers must be derived *exclusively* from the provided context chunks below."
                "\n\nStrict Guidelines:"
                "\n1.  **Evidence-Based**: If the answer is not in the context, say 'I don't know.' do NOT guess or use outside knowledge."
                "\n2.  **Conciseness**: Keep answers crisp and direct. Maximum 3 sentences."
                "\n3.  **Accuracy**: Prioritize accuracy over fluency."
                "\n\nContext:\n{context}"
            ),
        ),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

# Central dictionary to register prompts
PROMPT_REGISTRY = {
    "document_analysis": document_analysis_prompt,
    "document_comparison": document_comparison_prompt,
    "contextualize_question": contextualize_question_prompt,
    "context_qa": context_qa_prompt,
}
