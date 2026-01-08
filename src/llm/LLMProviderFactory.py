from .providers import CohereProvider
from .LLMEnums import LLMEnums


class LLMProviderFactory:

    def __init__(self, config: dict):

        self.config = config

    def get_llm(self, provider: str):

        if provider == LLMEnums.COHERE.value:
            return CohereProvider(
                api_key = self.config.COHERE_API_KEY, 
                default_generation_max_output_tokens = self.config.GENERATION_DAFAULT_MAX_TOKENS,
                default_generation_temperature = self.config.GENERATION_DAFAULT_TEMPERATURE,
                default_input_max_characters = self.config.INPUT_DAFAULT_MAX_CHARACTERS )
        
        else: 
            return None
            


