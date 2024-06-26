import unittest
from main import read_resume, read_job_desc

class TestMain(unittest.TestCase):
    def test_read_resume(self):
        # Make sure non-existent files return None
        self.assertEqual(read_resume("abasdjfasdf"), None)
        # Make sure it reads nothing from an empty file
        self.assertEqual(read_resume("sample_resumes/empty.txt"), "")
        # Make sure it reads all the text from a file
        self.assertEqual(read_resume("sample_resumes/simple.txt"), "hi\nthere\nbud")
        

    def test_read_job_desc(self):
        # Make sure non-existent files return None
        self.assertEqual(read_job_desc("asgasdfasddf"), None)
        # Make sure it reads nothing from an empty file
        self.assertEqual(read_job_desc("sample_job_descriptions/empty.txt"), "")
        # Make sure it reads all the text from a file
        self.assertEqual(read_job_desc("sample_job_descriptions/simple.txt"), "hi\nthere\nbud")
