SERVICE_CONFIG = {
    "explain": {
        "key": "explain_prompt",
        "vars": lambda input_text, target_language: {
            "input_text": input_text
        }
    },
    "summarize_snippet": {
        "key": "summary_prompt",
        "vars": lambda input_text, target_language: {
            "input_text": input_text
        }
    },
    "translate": {
        "key": "translate_prompt",
        "vars": lambda input_text, target_language: {
            "input_text": input_text,
            "target_language": target_language
        }
    },
    "generate_title": {
        "key": "title_prompt",
        "vars": lambda input_text, target_language: {
            "input_text": input_text
        }
    }
}