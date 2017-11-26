import unittest
import substitution

class TestSubstitutionFunctions(unittest.TestCase):

    def test_replace(self):
        equivalents = {'boolean':'DB_BOOLEAN'}
        schema_fhir = '{"id":"Patient", "CML":[{"id": "boolean"}]}'
        schema_openehr = '{"id":"Patient", "CML":[{"id": "DB_BOOLEAN"}]}'
        self.assertEqual(substitution.replace(schema_fhir, equivalents), schema_openehr)

if __name__ == '__main__':
    unittest.main()
