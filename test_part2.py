"""
Part 2: String Operations DSL - Synthesis Test Cases
This file contains synthesis test cases for students to solve using the string transformation DSL.
Students should examine these test cases to understand the expected behavior and implement the DSL.
"""

import unittest
from typing import List, Tuple

class TestPart2Strings(unittest.TestCase):
    """Test cases for Part 2: String Operations DSL"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment once for all tests"""
        print(f"\n{'='*60}")
        print("PART 2: STRING OPERATIONS DSL TESTS")
        print(f"{'='*60}")
        
        # Import required modules
        try:
            from string_synthesizer import StringSynthesizer
            cls.StringSynthesizer = StringSynthesizer
            cls.strings_available = True
        except ImportError as e:
            print(f"Warning: Required modules not available: {e}")
            cls.strings_available = False
    
    def setUp(self):
        """Set up each individual test"""
        if not self.strings_available:
            self.fail("Required modules not available")
        
        self.synthesizer = self.StringSynthesizer()

    def _test_string_synthesis(self, examples: List[Tuple[str, str]], test_name: str):
        """Helper method to test string synthesis capabilities"""
        try:
            print(f"Synthesizing {test_name}...")
            program = self.synthesizer.synthesize(examples, max_iterations=5)
            for input_str, expected_output in examples:
                try:
                    actual_output = program.interpret(input_str)
                    self.assertIsInstance(actual_output, str)
                    self.assertEqual(actual_output, expected_output)
                except Exception as e:
                    self.fail(f"Interpretation failed for {test_name}: {e}")
                    
            print(f"Synthesized {test_name}: {program}")
        except Exception as e:
            self.fail(f"Synthesis failed for {test_name}: {e}")

    def test_formal_greeting(self):
        examples = [
            ("hello", "HELLO"),
            ("world", "WORLD"), 
            ("python", "PYTHON"),
            ("synthesis", "SYNTHESIS"),
            ("programming", "PROGRAMMING")
        ]
        self._test_string_synthesis(examples, "formal_greeting")

    def test_casual_style(self):
        examples = [
            ("HELLO", "hello"),
            ("WORLD", "world"),
            ("PYTHON", "python"), 
            ("SYNTHESIS", "synthesis"),
            ("PROGRAMMING", "programming")
        ]
        self._test_string_synthesis(examples, "casual_style")

    def test_get_first_name(self):
        examples = [
            ("John Smith", "John"),
            ("Mary Johnson", "Mary"),
            ("Alice Brown", "Alice"),
            ("Bob Wilson", "Bob"),
            ("Emma Davis", "Emma")
        ]
        self._test_string_synthesis(examples, "get_first_name")

    def test_get_last_name(self):
        examples = [
            ("John Smith", "Smith"),
            ("Mary Johnson", "Johnson"),
            ("Alice Brown Wilson", "Wilson"),
            ("Bob Davis", "Davis"),
            ("Emma Thompson", "Thompson")
        ]
        self._test_string_synthesis(examples, "get_last_name")

    def test_get_middle_initial(self):
        examples = [
            ("John Michael Smith", "M"),
            ("Mary Elizabeth Johnson", "E"),
            ("Alice Rose Brown", "R"),
            ("Bob James Wilson", "J"),
            ("Emma Grace Davis", "G")
        ]
        self._test_string_synthesis(examples, "get_middle_initial")

    def test_clean_user_input(self):
        examples = [
            ("  hello  ", "hello"),
            ("\tworld\t", "world"),
            ("  python programming  ", "python programming"),
            (" \n synthesis \n ", "synthesis"),
            ("   clean input   ", "clean input")
        ]
        self._test_string_synthesis(examples, "clean_user_input")

    def test_get_file_extension(self):
        examples = [
            ("document.txt", "txt"),
            ("image.jpg", "jpg"),
            ("script.py", "py"),
            ("data.csv", "csv"),
            ("config.xml", "xml")
        ]
        self._test_string_synthesis(examples, "get_file_extension")

    def test_get_first_name_initial(self):
        examples = [
            ("John", "J"),
            ("mary", "M"),
            ("Alice", "A"),
            ("bob", "B"),
            ("Emma", "E")
        ]
        self._test_string_synthesis(examples, "get_first_name_initial")

    def test_create_emphasis(self):
        examples = [
            ("!", "!!!"),
            ("?", "???"),
            ("*", "***"),
            ("-", "---"),
            (".", "...")
        ]
        self._test_string_synthesis(examples, "create_emphasis")

    def test_phone_area_code(self):
        examples = [
            ("(555) 123-4567", "555"),
            ("(123) 456-7890", "123"),
            ("(999) 888-7777", "999"),
            ("(444) 333-2222", "444"),
            ("(777) 666-5555", "777")
        ]
        self._test_string_synthesis(examples, "phone_area_code")

    def test_professional_email_signature(self):    
        examples = [
            ("john smith", "JOHN smith"),
            ("mary johnson", "MARY johnson"),
            ("alice brown wilson", "ALICE wilson"),
            ("bob davis", "BOB davis"),
            ("emma thompson", "EMMA thompson")
        ]
        self._test_string_synthesis(examples, "professional_email_signature")

    def test_create_hashtag(self):
        examples = [
            ("Machine Learning", "#machinelearning"),
            ("Data Science", "#datascience"),
            ("Python Programming", "#pythonprogramming"),
            ("Web Development", "#webdevelopment"),
            ("Artificial Intelligence", "#artificialintelligence")
        ]
        self._test_string_synthesis(examples, "create_hashtag")

    @unittest.skip("Skipping format_phone_number test case")
    def test_format_phone_number(self):
        examples = [
            ("5551234567", "555-123-4567"),
            ("1234567890", "123-456-7890"),
            ("9998887777", "999-888-7777"),
            ("4443332222", "444-333-2222"),
            ("7776665555", "777-666-5555")
        ]
        self._test_string_synthesis(examples, "format_phone_number")

    def test_generate_password_hint(self):
        examples = [
            ("password", "Pas***"),
            ("secret", "Sec***"),
            ("mykey", "Myk***"),
            ("login", "Log***"),
            ("access", "Acc***")
        ]
        self._test_string_synthesis(examples, "generate_password_hint")

    def test_format_title(self):
        examples = [
            ("  user_guide  ", "USER GUIDE"),
            (" technical_documentation ", "TECHNICAL DOCUMENTATION"),
            ("  project_report  ", "PROJECT REPORT"),
            (" system_manual ", "SYSTEM MANUAL"),
            ("  installation_notes  ", "INSTALLATION NOTES")
        ]
        self._test_string_synthesis(examples, "format_title")

    def test_extract_domain(self):
        examples = [
            ("user@gmail.com", "gmail.com"),
            ("admin@company.org", "company.org"),
            ("student@university.edu", "university.edu"),
            ("support@service.net", "service.net"),
            ("info@domain.io", "domain.io")
        ]
        self._test_string_synthesis(examples, "extract_domain")

    def test_format_currency(self):
        examples = [
            ("100", "$100.00"),
            ("25", "$25.00"),
            ("999", "$999.00"),
            ("1", "$1.00"),
            ("50", "$50.00")
        ]
        self._test_string_synthesis(examples, "format_currency")

    def test_create_slug(self):
        examples = [
            ("  My Blog Post  ", "my-blog-post"),
            (" Product Review ", "product-review"),
            ("  News Article  ", "news-article"),
            (" User Guide ", "user-guide"),
            ("  Tutorial Series  ", "tutorial-series")
        ]
        self._test_string_synthesis(examples, "create_slug")

    def test_extract_major_version(self):
        examples = [
            ("v1.2.3", "1"),
            ("v2.0.1", "2"),
            ("v3.1.4", "3"),
            ("v0.9.8", "0"),
            ("v4.5.2", "4")
        ]
        self._test_string_synthesis(examples, "extract_major_version")

    def test_clean_and_capitalize(self):
        examples = [
            ("  hello world  ", "HELLO WORLD"),
            ("\tpython programming\t", "PYTHON PROGRAMMING"),
            ("  data science  ", "DATA SCIENCE"),
            (" \n machine learning \n ", "MACHINE LEARNING"),
            ("   web development   ", "WEB DEVELOPMENT")
        ]
        self._test_string_synthesis(examples, "clean_and_capitalize")

    def test_reverse_name_format(self):
        examples = [
            ("John Smith", "Smith, John"),
            ("Mary Johnson", "Johnson, Mary"),
            ("Alice Brown Wilson", "Wilson, Alice"),
            ("Bob Davis", "Davis, Bob"),
            ("Emma Thompson", "Thompson, Emma")
        ]
        self._test_string_synthesis(examples, "reverse_name_format")

    def test_extract_filename_from_path(self):
        examples = [
            ("/home/user/document.txt", "document"),
            ("/var/log/system.log", "system"),
            ("/tmp/data.csv", "data"),
            ("/usr/bin/program.exe", "program"),
            ("/etc/config.xml", "config")
        ]
        self._test_string_synthesis(examples, "extract_filename_from_path")

    def test_extract_file_extension(self):
        examples = [
            ("/home/user/document.txt", "txt"),
            ("/var/log/system.log", "log"),
            ("/tmp/data.csv", "csv"),
            ("/usr/bin/script.py", "py"),
            ("/etc/config.json", "json")
        ]
        self._test_string_synthesis(examples, "extract_file_extension")

    def test_get_parent_directory(self):
        examples = [
            ("/home/user/documents/file.txt", "documents"),
            ("/var/log/apache/access.log", "apache"),
            ("/tmp/downloads/data.csv", "downloads"),
            ("/usr/local/bin/script.py", "bin"),
            ("/etc/nginx/sites/config.conf", "sites")
        ]
        self._test_string_synthesis(examples, "get_parent_directory")

    def test_extract_directory_path(self):
        examples = [
            ("/home/user/file.txt", "/home"),
            ("/var/log/system.log", "/var"),
            ("/tmp/data.csv", "/tmp"),
            ("/usr/bin/script.py", "/usr"),
            ("/etc/config.xml", "/etc")
        ]
        self._test_string_synthesis(examples, "extract_directory_path")

    def test_normalize_path_separators(self):
        examples = [
            ("C:\\Users\\Documents\\file.txt", "C:/Users/Documents/file.txt"),
            ("D:/Projects/code/script.py", "D:/Projects/code/script.py"),
            ("E:\\Data\\backup\\archive.zip", "E:/Data/backup/archive.zip"),
            ("F:/Temp\\logs\\error.log", "F:/Temp/logs/error.log"),
            ("G:\\Music\\albums\\song.mp3", "G:/Music/albums/song.mp3")
        ]
        self._test_string_synthesis(examples, "normalize_path_separators")

    @unittest.skip("Skipping format_initials test case")
    def test_format_initials(self):
        examples = [
            ("john smith", "J.S."),
            ("mary elizabeth johnson", "M.J."),
            ("alice brown", "A.B."),
            ("bob wilson", "B.W."),
            ("emma grace davis", "E.D.")
        ]
        self._test_string_synthesis(examples, "format_initials")

    @unittest.skip("Skipping create_acronym test case")
    def test_create_acronym(self):
        examples = [
            ("machine learning", "ML"),
            ("artificial intelligence", "AI"),
            ("data science", "DS"),
            ("programming languages", "PL"),
            ("software engineering", "SE")
        ]
        self._test_string_synthesis(examples, "create_acronym")

if __name__ == "__main__":
    unittest.main()