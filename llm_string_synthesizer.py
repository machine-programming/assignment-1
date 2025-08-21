"""
LLM-based Program Synthesis
This module uses Gemini 2.5 Pro to generate string operation programs
from input-output examples through carefully crafted prompts.
"""

import json
import os
from typing import List, Tuple, Optional
import google.generativeai as genai
from google.generativeai.types import GenerateContentResponse
from strings import *

class LLMPromptAndResponseLogger:
    """
    Logger for LLM prompt and response
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.prompt = ""
        self.response = ""
        self.program = None
        self.examples = []
        self.error = None

    def log_prompt(self, prompt: str, examples: List[Tuple[str, str]]):
        self.prompt = str(prompt)
        self.examples = str(examples)

    def log_response(self, response: GenerateContentResponse):
        self.response = str(response)

    def log_program(self, program: StringExpression):
        self.program = str(program)

    def log_error(self, error: Exception):
        self.error = str(error)

    def save(self):
        # dump into jsonl file as a single line
        with open(self.file_path, 'a') as f:
            f.write(json.dumps({'prompt': self.prompt, 'response': self.response, 'examples': self.examples, 'program': self.program, 'error': self.error}) + '\n')
            f.flush()

class LLMStringSynthesizer:
    """LLM-based synthesizer using Gemini 2.5 Pro"""
    
    def __init__(self, api_key: Optional[str] = None, logger: Optional[LLMPromptAndResponseLogger] = None):
        """
        Initialize the LLM synthesizer
        
        Args:
            api_key: Gemini API key. If None, will try to get from environment
        """
        if api_key is None:
            api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            raise ValueError("Gemini API key required. Set GEMINI_API_KEY environment variable or pass api_key parameter.")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro')
        self.logger = logger

    def synthesize(self, examples: List[Tuple[str, str]], max_iterations: int = 5) -> StringExpression:
        """
        Synthesize a string expression from input-output examples using LLM
        
        Args:
            examples: List of (input, output) string pairs
            max_iterations: Maximum number of growth iterations (unused in LLM approach)
            
        Returns:
            StringExpression that satisfies the examples
        """
        if not examples:
            raise ValueError("No examples provided")
        
        # Create the prompt template with DSL description and examples
        prompt = self.generate_prompt(examples)

        if self.logger:
            self.logger.log_prompt(prompt, examples)
        
        try:
            # Generate response from Gemini
            response = self.model.generate_content(prompt)
            if self.logger:
                self.logger.log_response(response)
            program_text = response.text.strip()
            
            # Extract and evaluate the program
            program = self.extract_program(program_text)
            if self.logger:
                self.logger.log_program(program)

            if self.logger:
                self.logger.save()

            # Validate the program against examples
            if self.validate_program(program, examples):
                return program
            else:
                raise ValueError(f"Generated program does not satisfy all examples: {program}")
                
        except Exception as e:
            if self.logger:
                self.logger.log_error(e)
                self.logger.save()

            raise ValueError(f"Failed to synthesize program: {str(e)}")
    
    def generate_prompt(self, examples: List[Tuple[str, str]]) -> str:
        """
        Create a comprehensive prompt template for the LLM including DSL description and examples
        """
        
        #####################################################################################################
        #                                                                                                   #
        # Part 3 (a): Creating a Prompt Template (`generate_prompt`)                                        #
        #                                                                                                   #
        # TODO: Add your implementation here.                                                               #
        #                                                                                                   #
        # NOTE: Below is a placeholder implementation that does not generate a prompt template. You need to #
        #       implement the actual prompt template generation logic here.                                 #
        #                                                                                                   #
        #####################################################################################################

        return "Please write a program"
    
    def extract_program(self, response_text: str) -> StringExpression:
        """
        Extract the program from LLM response and evaluate it to get StringExpression object
        """

        #####################################################################################################
        #                                                                                                   #
        # Part 3 (b): Extract the StringExpression from the LLM response (`extract_program`)                #
        #                                                                                                   #
        # TODO: Add your implementation here.                                                               # 
        #                                                                                                   #
        # NOTE: Below is a placeholder implementation that does not extract the StringExpression from the   #
        #       LLM response. You need to implement the actual extraction logic here.                       #
        #                                                                                                   #
        #####################################################################################################

        return StringLiteral("Dummy program")
    
    def validate_program(self, program: StringExpression, examples: List[Tuple[str, str]]) -> bool:
        """
        Validate that the generated program works correctly on all examples
        """
        try:
            for input_str, expected_output in examples:
                actual_output = program.interpret(input_str)
                if actual_output != expected_output:
                    return False
            return True
        except Exception:
            return False
