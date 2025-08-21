"""
Part 3: LLM-based Program Synthesis - Test Cases and Examples
This file contains test cases and examples for LLM-based string transformation synthesis.
Students should examine these test cases and work on improving the LLM synthesis methods.
"""

import os
import unittest
from typing import List, Tuple
from llm_string_synthesizer import LLMPromptAndResponseLogger

from test_part2 import TestPart2Strings

class TestPart3LLM(TestPart2Strings):
    """Test cases for Part 3: LLM-based Program Synthesis"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.report_file_path = f"llm_synthesis_report.jsonl"
        if os.path.exists(self.report_file_path):
            os.remove(self.report_file_path)

    @classmethod
    def setUpClass(cls):
        """Set up test environment once for all tests"""
        print(f"\n{'='*60}")
        print("PART 3: LLM-BASED PROGRAM SYNTHESIS TESTS")
        print(f"{'='*60}")
        
        # Check for API key
        cls.api_key = os.getenv('GEMINI_API_KEY')
        
        if not cls.api_key:
            print("Warning: No Gemini API key found!")
            print("Set GEMINI_API_KEY environment variable to run LLM tests.")
            cls.llm_available = False
        else:
            # Import required modules
            try:
                from llm_string_synthesizer import LLMStringSynthesizer
                cls.LLMStringSynthesizer = LLMStringSynthesizer
                cls.llm_available = True
            except ImportError as e:
                print(f"Warning: Required modules not available: {e}")
                cls.llm_available = False
    
    def setUp(self):
        """Set up each individual test"""
        if not self.llm_available:
            self.fail("LLM synthesis not available (missing API key or modules)")
        
        self.logger = LLMPromptAndResponseLogger(file_path=self.report_file_path)
        self.synthesizer = self.LLMStringSynthesizer(api_key=self.api_key, logger=self.logger)
    
    def _test_string_synthesis(self, examples: List[Tuple[str, str]], test_name: str):
        """Helper method to test LLM synthesis capabilities"""
        try:
            print(f"Synthesizing {test_name}...")

            # Run LLM synthesis
            program = self.synthesizer.synthesize(examples, max_iterations=3)
            
            # Test that the synthesized program can interpret the examples
            for input_str, expected_output in examples:
                try:
                    actual_output = program.interpret(input_str)
                    # Note: We don't assert exact correctness here as LLM synthesis might not always succeed
                    # This is more of a smoke test to ensure the system works
                    self.assertIsInstance(actual_output, str)
                    self.assertEqual(actual_output, expected_output, f"Synthesized {test_name} program failed; program is {program}. Expected {expected_output} but got {actual_output}")
                except Exception as e:
                    # Interpretation might fail, which is acceptable for some complex cases
                    self.fail(f"Interpretation failed for {test_name}: {e}")

            print(f"Synthesized {test_name}: {program}")

        except Exception as e:
            # Synthesis might fail, which is acceptable for some complex cases
            self.fail(f"LLM synthesis failed for {test_name}: {e}")

    def test_smart_capitalization(self):
        examples = [
            ("quick brown fox", "Quick Brown Fox"),
            ("artificial intelligence research", "Artificial Intelligence Research"),
            ("machine learning algorithms", "Machine Learning Algorithms"),
            ("natural language processing", "Natural Language Processing"),
            ("computer vision applications", "Computer Vision Applications")
        ]
        self._test_string_synthesis(examples, "smart_capitalization")

    def test_intelligent_extraction(self):
        examples = [
            ("Temperature: 25°C", "25°C"),
            ("Speed: 60 mph", "60 mph"),
            ("Price: $29.99", "$29.99"),
            ("Weight: 150 lbs", "150 lbs"),
            ("Distance: 5.2 km", "5.2 km")
        ]
        self._test_string_synthesis(examples, "intelligent_extraction")

    def test_complex_name_formatting(self):
        examples = [
            ("john michael smith", "SMITH, J.M."),
            ("mary elizabeth johnson", "JOHNSON, M.E."),
            ("robert james wilson", "WILSON, R.J."),
            ("sarah anne brown", "BROWN, S.A."),
            ("david paul davis", "DAVIS, D.P.")
        ]
        self._test_string_synthesis(examples, "complex_name_formatting")

    def test_advanced_email_processing(self):
        examples = [
            ("john.smith@company.com", "JOHN.SMITH@COMPANY"),
            ("mary_johnson@university.edu", "MARY_JOHNSON@UNIVERSITY"),
            ("bob.wilson123@startup.io", "BOB.WILSON123@STARTUP"),
            ("alice.brown@research.org", "ALICE.BROWN@RESEARCH"),
            ("emma.davis@tech.net", "EMMA.DAVIS@TECH")
        ]
        self._test_string_synthesis(examples, "advanced_email_processing")

    def test_phone_number_masking(self):
        examples = [
            ("(555) 123-4567", "(555) ***-4567"),
            ("(408) 987-6543", "(408) ***-6543"),
            ("(212) 555-1234", "(212) ***-1234"),
            ("(650) 789-0123", "(650) ***-0123"),
            ("(415) 246-8135", "(415) ***-8135")
        ]
        self._test_string_synthesis(examples, "phone_number_masking")

    def test_repeated_pattern_generation(self):
        examples = [
            ("abc", "abc-abc-abc"),
            ("xyz", "xyz-xyz-xyz"),
            ("123", "123-123-123"),
            ("hi", "hi-hi-hi"),
            ("ok", "ok-ok-ok")
        ]
        self._test_string_synthesis(examples, "repeated_pattern_generation")

    def test_nested_extraction_and_formatting(self):
        examples = [
            ("user:john_doe|role:admin|dept:IT", "JOHN_DOE-ADMIN"),
            ("user:mary_smith|role:manager|dept:HR", "MARY_SMITH-MANAGER"),
            ("user:bob_wilson|role:developer|dept:ENG", "BOB_WILSON-DEVELOPER"),
            ("user:alice_brown|role:analyst|dept:FIN", "ALICE_BROWN-ANALYST"),
            ("user:emma_davis|role:designer|dept:UX", "EMMA_DAVIS-DESIGNER")
        ]
        self._test_string_synthesis(examples, "nested_extraction_and_formatting")

    def test_multi_level_path_processing(self):
        examples = [
            ("/home/users/john/documents/file.txt", "JOHN_FILE"),
            ("/var/log/system/error.log", "SYSTEM_ERROR"),
            ("/usr/local/bin/python", "BIN_PYTHON"),
            ("/opt/apps/myapp/config.json", "MYAPP_CONFIG"),
            ("/tmp/session/data.csv", "SESSION_DATA")
        ]
        self._test_string_synthesis(examples, "multi_level_path_processing")

    def test_complex_string_transformation(self):
        examples = [
            ("  Hello World! Welcome  ", "HEL_WOR_WEL"),
            ("  Python Programming Fun  ", "PYT_PRO_FUN"),
            ("  Data Science Rocks  ", "DAT_SCI_ROC"),
            ("  Machine Learning AI  ", "MAC_LEA_AI"),
            ("  Software Engineering  ", "SOF_ENG")
        ]
        self._test_string_synthesis(examples, "complex_string_transformation")

    def test_advanced_acronym_with_numbers(self):
        examples = [
            ("Version 2.0 Release Candidate", "V2RC"),
            ("Application Programming Interface 3.1", "API3"),
            ("Structured Query Language 5.0", "SQL5"),
            ("Hyper Text Transfer Protocol 2.0", "HTTP2"),
            ("Java Script Object Notation 1.1", "JSON1")
        ]
        self._test_string_synthesis(examples, "advanced_acronym_with_numbers")

    def test_interleaved_string_construction(self):
        examples = [
            ("abcdef", "a-b-c-d-e-f"),
            ("hello", "h-e-l-l-o"),
            ("world", "w-o-r-l-d"),
            ("python", "p-y-t-h-o-n"),
            ("code", "c-o-d-e")
        ]
        self._test_string_synthesis(examples, "interleaved_string_construction")

    def test_reverse_and_transform(self):
        examples = [
            ("first second third", "THIRD.SECOND.FIRST"),
            ("alpha beta gamma", "GAMMA.BETA.ALPHA"),
            ("one two three", "THREE.TWO.ONE"),
            ("red green blue", "BLUE.GREEN.RED"),
            ("start middle end", "END.MIDDLE.START")
        ]
        self._test_string_synthesis(examples, "reverse_and_transform")

    def test_nested_replacement_and_extraction(self):
        examples = [
            ("name=john&age=25&city=nyc", "JOHN_NYC"),
            ("user=mary&role=admin&team=hr", "MARY_HR"),
            ("id=123&type=premium&status=active", "123_ACTIVE"),
            ("code=abc&level=senior&dept=eng", "ABC_ENG"),
            ("ref=xyz&grade=a&subject=math", "XYZ_MATH")
        ]
        self._test_string_synthesis(examples, "nested_replacement_and_extraction")

    def test_multi_step_normalization(self):
        examples = [
            ("  HELLO-WORLD_TEST  ", "hello.world.test"),
            ("  DATA-SCIENCE_ROCKS  ", "data.science.rocks"),
            ("  MACHINE-LEARNING_AI  ", "machine.learning.ai"),
            ("  PYTHON-PROGRAMMING_FUN  ", "python.programming.fun"),
            ("  WEB-DEVELOPMENT_COOL  ", "web.development.cool")
        ]
        self._test_string_synthesis(examples, "multi_step_normalization")

    def test_pattern_based_extraction(self):
        examples = [
            ("2023-12-25T10:30:45", "2023_10_30"),
            ("2024-01-15T14:22:33", "2024_14_22"),
            ("2022-06-30T09:15:20", "2022_09_15"),
            ("2023-03-18T16:45:10", "2023_16_45"),
            ("2024-09-05T11:20:55", "2024_11_20")
        ]
        self._test_string_synthesis(examples, "pattern_based_extraction")

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPart3LLM)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    