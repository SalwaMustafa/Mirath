from ..LLMInterface import LLMInterface
from ..LLMEnums import CohereEnums, DocumentTypeEnum
import cohere
import logging

class CohereProvider(LLMInterface):

    def __init__(self, api_key: str, default_generation_max_output_tokens: int=1000,
                                     default_generation_temperature: float=0.1,
                                     default_input_max_characters: int=1000):
        
        self.api_key = api_key
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature
        self.default_input_max_characters = default_input_max_characters

        self.generation_model = None
        self.embedding_model = None

        self.cohere_client = cohere.Client(api_key = self.api_key)

        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_id: str):

        self.generation_model = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int):

        self.embedding_model = model_id
        self.embedding_size = embedding_size

    def process_text(self, text: str):
        return text[:self.default_input_max_characters].strip()


    def generate_text(self, prompt: str, chat_history: list=[], max_output_tokens: int=None,
                            temperature: float = None):
        

        if not self.cohere_client:
            self.logger.error("CoHere client was not set")
            return None

        if not self.generation_model:
            self.logger.error("Generation model for CoHere was not set")
            return None
        
        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_output_tokens
        temperature = temperature if temperature else  self.default_generation_temperature

        response = self.cohere_client.chat(
                    model = self.generation_model,
                    message = self.process_text(prompt),
                    temperature = temperature,
                    max_tokens = max_output_tokens
        )

        if not response or not response.text:
            self.logger.error("The cohere generation response is empty")
            return None

        return response.text
    

    def embed_text(self, text: str, document_type: str = None):

        if not self.cohere_client:
            self.logger.error("CoHere client was not set")
            return None

        if not self.embedding_model:
            self.logger.error("Embedding model for CoHere was not set")
            return None

        input_type = CohereEnums.DOCUMENT.value if document_type == DocumentTypeEnum.DOCUMENT.value else CohereEnums.QUERY.value

        embedding_text = self.cohere_client.embed(
                         model = self.embedding_model,
                         input_type = input_type,
                         texts=[self.process_text(text)],
                         embedding_types=["float"])
        

        if not embedding_text or not  embedding_text.embeddings or not embedding_text.embeddings.float:

            self.logger.error("The cohere embedding response is empty")
            return None
        
        return embedding_text.embeddings.float[0]
    

    def construct_prompt(self, prompt: str, role: str):


        return {
            "role" : role,
            "message" : self.process_text(prompt)
        }