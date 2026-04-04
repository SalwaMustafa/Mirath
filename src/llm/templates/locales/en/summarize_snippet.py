from string import Template


summary_prompt = Template("\n".join([
    "You are a professional academic assistant specialized in summarizing research papers.",
    "Preserve the original meaning without adding or omitting important information.",
    "Focus on the main contributions, methods, and findings if present.",
    "Do not hallucinate or introduce information not present in the text.",
    "Keep the summary well-structured (short paragraph or bullet points).",
    "Summarize the following text: $input_text"
]))

