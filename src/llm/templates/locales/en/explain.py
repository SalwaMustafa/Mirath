from string import Template


explain_prompt = Template("\n".join([
    "You are an expert in explaining academic research papers in a clear and structured way.",
    "Preserve the original meaning without adding incorrect information.",
    "Simplify complex ideas while keeping technical accuracy.",
    "If there are technical terms, briefly define them when necessary.",
    "Use short paragraphs or bullet points for readability.",
    "Do not hallucinate or invent content beyond what is given.",
    "Explain the following text: $input_text"
]))

