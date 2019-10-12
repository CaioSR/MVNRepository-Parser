import unittest
import MVNparser

class TestMVNParser(unittest.TestCase):

    def test_getSoup(self):
        soup = MVNparser.getSoup("https://www.google.com")
        self.assertIsInstance(soup, MVNparser.BeautifulSoup, 'Tipo de retorno incorreto')

    def test_getVersions(self):
        soup = MVNparser.getSoup("https://mvnrepository.com/artifact/org.apache.jclouds/jclouds-compute")
        versions = MVNparser.getVersions(soup)
        self.assertIsInstance(versions , list, 'Tipo de retorno incorreto')

    def test_searchDependency(self):
        soup = MVNparser.getSoup("https://mvnrepository.com/artifact/org.apache.jclouds/jclouds-compute/2.1.2")
        dependency = "com.google.auto/auto-common/0.3"
        result = MVNparser.searchDependency(soup, dependency)
        self.assertEqual(result, False, 'Incorrect result')

    def test_isVersion(self):
        link = "/artifact/com.google.auto/auto-common/0.3"
        result = MVNparser.isVersion(link)
        self.assertEqual(result, True, 'Incorrect result')

    def test_getDependencies(self):
        pass

    def test_getUsages(self):
        pass

if __name__ == '__main__':
    unittest.main()
