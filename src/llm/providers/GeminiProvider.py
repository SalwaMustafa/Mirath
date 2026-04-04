from ..LLMInterface import LLMInterface
from ..LLMEnums import DocumentTypeEnum, GeminiEnums
import logging
from typing import List
from google import genai
from google.genai import types



class GeminiProvider(LLMInterface):

    def __init__(self, api_key: str, default_generation_max_output_tokens: int=1000,
                                     default_generation_temperature: float=0.1,
                                     default_input_max_characters: int=1000):
        
        self.api_key = api_key
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature
        self.default_input_max_characters = default_input_max_characters

        self.generation_model = None
        self.embedding_model = None

        self.gemini_client = genai.Client(api_key = self.api_key)

        self.logger = logging.getLogger('uvicorn')


    def set_generation_model(self, model_id: str):

        self.generation_model = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model = model_id
        self.embedding_size = embedding_size


    def generate_text(self, prompt: str, chat_history: list=[], max_output_tokens: int=None,
                            temperature: float = None):
        
        if not self.gemini_client:
            self.logger.error("Gemini client was not set")
            return None

        if not self.generation_model:
            self.logger.error("Generation model for Gemini was not set")
            return None
        
        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_output_tokens
        temperature = temperature if temperature else  self.default_generation_temperature

        grounding_tool = types.Tool(google_search = types.GoogleSearch())

        config = types.GenerateContentConfig(temperature = temperature, tools = [grounding_tool])
        
        response = self.gemini_client.models.generate_content(
                   model = self.generation_model,
                   contents = prompt,
                   config = config
                   )
        
        if not response or not response.text:
            self.logger.error("The gemini generation response is empty")
            return None

        return response.text
    
    def embed_text(self, text: str, document_type: str = None):

        if not self.gemini_client:
            self.logger.error("Gemini client was not set")
            return None

        if not self.embedding_model:
            self.logger.error("Embedding model for Gemini was not set")
            return None
        
        input_type = GeminiEnums.DOCUMENT.value if document_type == DocumentTypeEnum.DOCUMENT.value else GeminiEnums.QUERY.value

        
        response = self.gemini_client.models.embed_content(
                   model = self.embedding_model,
                   contents = text,
                   config=types.EmbedContentConfig(task_type = input_type,
                                                   output_dimensionality = self.embedding_size)
                )
        
        if not response or not response.embeddings:
            self.logger.error("The gemini embedding response is empty")
            return None

        return response.embeddings
    

    def construct_prompt(self, prompt: str, role: str):
        
        pass
        