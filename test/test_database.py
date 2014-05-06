from os import path
import unittest

from comp61542.database import database

class TestDatabase(unittest.TestCase):

    def setUp(self):
        dir, _ = path.split(__file__)
        self.data_dir = path.join(dir, "..", "data")

    def test_read(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        self.assertEqual(len(db.publications), 2)

    def test_read_invalid_xml(self):
        db = database.Database()
        self.assertFalse(db.read(path.join(self.data_dir, "invalid_xml_file.xml")))

    def test_read_missing_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "missing_year.xml")))
        self.assertEqual(len(db.publications), 0)

    def test_read_missing_title(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "missing_title.xml")))
        # publications with missing titles should be added
        self.assertEqual(len(db.publications), 1)

    def test_get_average_authors_per_publication(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-1.xml")))
        _, data = db.get_average_authors_per_publication(database.Stat.MEAN)
        self.assertAlmostEqual(data[0], 2.3, places=1)
        _, data = db.get_average_authors_per_publication(database.Stat.MEDIAN)
        self.assertAlmostEqual(data[0], 2, places=1)
        _, data = db.get_average_authors_per_publication(database.Stat.MODE)
        self.assertEqual(data[0], [2])

    def test_get_average_publications_per_author(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-2.xml")))
        _, data = db.get_average_publications_per_author(database.Stat.MEAN)
        self.assertAlmostEqual(data[0], 1.5, places=1)
        _, data = db.get_average_publications_per_author(database.Stat.MEDIAN)
        self.assertAlmostEqual(data[0], 1.5, places=1)
        _, data = db.get_average_publications_per_author(database.Stat.MODE)
        self.assertEqual(data[0], [0, 1, 2, 3])

    def test_get_average_publications_in_a_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-3.xml")))
        _, data = db.get_average_publications_in_a_year(database.Stat.MEAN)
        self.assertAlmostEqual(data[0], 2.5, places=1)
        _, data = db.get_average_publications_in_a_year(database.Stat.MEDIAN)
        self.assertAlmostEqual(data[0], 3, places=1)
        _, data = db.get_average_publications_in_a_year(database.Stat.MODE)
        self.assertEqual(data[0], [3])

    def test_get_average_authors_in_a_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-4.xml")))
        _, data = db.get_average_authors_in_a_year(database.Stat.MEAN)
        self.assertAlmostEqual(data[0], 2.8, places=1)
        _, data = db.get_average_authors_in_a_year(database.Stat.MEDIAN)
        self.assertAlmostEqual(data[0], 3, places=1)
        _, data = db.get_average_authors_in_a_year(database.Stat.MODE)
        self.assertEqual(data[0], [0, 2, 4, 5])
        # additional test for union of authors
        self.assertEqual(data[-1], [0, 2, 4, 5])

    def test_get_publication_summary(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_publication_summary()
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data[0]), 6,
            "incorrect number of columns in data")
        self.assertEqual(len(data), 2,
            "incorrect number of rows in data")
        self.assertEqual(data[0][1], 2,
            "incorrect number of publications for conference papers")
        self.assertEqual(data[1][1], 4,
            "incorrect number of authors for conference papers")

    def test_get_average_authors_per_publication_by_author(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "three-authors-and-three-publications.xml")))
        header, data = db.get_average_authors_per_publication_by_author(database.Stat.MEAN)
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 3,
            "incorrect average of number of conference papers")
        self.assertEqual(data[0][1], 1.5,
            "incorrect mean journals for author1")
        self.assertEqual(data[1][1], 2,
            "incorrect mean journals for author2")
        self.assertEqual(data[2][1], 1,
            "incorrect mean journals for author3")

    def test_get_publications_by_author(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data, indexes = db.get_publications_by_author()
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 4,
            "incorrect number of authors")
        self.assertEqual(data[0][-1], 1,
            "incorrect total")

    def test_get_average_publications_per_author_by_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_average_publications_per_author_by_year(database.Stat.MEAN)
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 1,
            "incorrect number of rows")
        self.assertEqual(data[0][0], 9999,
            "incorrect year in result")

    def test_get_publications_by_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_publications_by_year()
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 1,
            "incorrect number of rows")
        self.assertEqual(data[0][0], 9999,
            "incorrect year in result")

    def test_get_average_authors_per_publication_by_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_author_totals_by_year()
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 1,
            "incorrect number of rows")
        self.assertEqual(data[0][0], 9999,
            "incorrect year in result")
        self.assertEqual(data[0][1], 4,
            "incorrect number of authors in result")

    def test_get_author_totals_by_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_author_totals_by_year()
        print data
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 1,
            "incorrect number of rows")
        self.assertEqual(data[0][0], 9999,
            "incorrect year in result")
            
        string = "data[0][1]: "
        string += str(data[0][1])
        print string
        self.assertEqual(data[0][1], 4,
            "incorrect number of authors in result")
            
    def test_search_results_count(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "dblp_curated_sample.xml")))
        header, data, indexes = db.search_authors_by_name("Stefano Ceri")
        self.assertEqual(len(data), 1, "Incorrect number of search results")
        header, data, indexes = db.search_authors_by_name("STEFANO CERI")
        self.assertEqual(len(data), 1, "Incorrect number of search results")
        header, data, indexes = db.search_authors_by_name("NONAME")
        self.assertEqual(len(data), 0, "Incorrect number of search results")
        header, data, indexes = db.search_authors_by_name("")
        self.assertEqual(len(data),1139, "Incorrect number of search results")
        header, data, indexes = db.search_authors_by_name("*")
        self.assertEqual(len(data), 0, "Incorrect number of search results")
        
    def test_search_results_results(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "dblp_curated_sample.xml")))
        header, data, indexes = db.search_authors_by_name("Stefano Ceri")
        self.assertEqual(data[0][9], 218, "Incorrect results: Ceri")
        header, data, indexes = db.search_authors_by_name("McNab")
        self.assertEqual(data[0][6], 0, "Incorrect results: McNab")
        header, data, indexes = db.search_authors_by_name("Goble")
        self.assertEqual(data[0][1],115, "Incorrect results: Goble")
        header, data, indexes = db.search_authors_by_name("Stefano Ceri")
        # test First appearences
        self.assertEqual(data[0][5], 78, "Incorrect results for First Appearences")
        # test last appearences
        self.assertEqual(data[0][6], 25, "Incorrect results for Last Appearences")
        # test Sole appearences
        self.assertEqual(data[0][7], 8, "Incorrect results for Sole Appearences")
        
    def test_search_results_precendence(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "searchPrecedence.xml")))
        header, data, indexes = db.search_authors_by_name("Sam")
        names = ["Sam, Alice", "Sam, Brian", "Sammer, Alice", "Sammer, Brian", "Samming, Alice", "Samming, Brian", "Alice, Sam", "Brian, Sam", "Alice, Samuel", "Brian, Samuel", "Esam, Alice", "Esam, Brian"]
        searchResults = []
        for data_entry in data:
            searchResults.append(data_entry[0])
        self.assertEqual(names, searchResults, "search results precedence incorrect")
        
        
    def test_author_page_stats(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "dblp_curated_sample.xml")))
        name, data = db.get_author_stats(0)    
        self.assertEqual(name, "Stefano Ceri", "incorrect name found")
        self.assertEqual(data["publications_data"][0], 218, "incorrect overall publications value for stefano ceri")
        self.assertEqual(data["publications_data"][3], 6, "incorrect overall books value for stefano ceri")
        self.assertEqual(data["sole_author_data"][0], 8, "incorrect overall sole appearences value for stefano ceri")
        self.assertEqual(data["coauthor_data"][0], 210, "incorrect coauthor value for stefano ceri")
        
        # overall appearences
        overallPublications = data["publications_data"][0]
        sumOfPublications = 0
        for i in range(1,5):
            print i
            sumOfPublications += data["publications_data"][i]
            
        print "publications_data: " + str(overallPublications)
        self.assertEqual(overallPublications, sumOfPublications, "overall column does not equal sum of all columns")
        
        # first appearences
        overallPublications = data["first_author_data"][0]
        sumOfPublications = 0
        for i in range(1,5):
            print i
            sumOfPublications += data["first_author_data"][i]
        
        print "first_author_data: " + str(overallPublications)
        self.assertEqual(overallPublications, sumOfPublications, "overall column does not equal sum of all columns")
        
        # last appearences
        overallPublications = data["last_author_data"][0]
        sumOfPublications = 0
        for i in range(1,5):
            print i
            sumOfPublications += data["last_author_data"][i]
        
        print "last_author_data: " + str(overallPublications)
        self.assertEqual(overallPublications, sumOfPublications, "overall column does not equal sum of all columns")
        
        # sole appearences
        overallPublications = data["sole_author_data"][0]
        sumOfPublications = 0
        for i in range(1,5):
            print i
            sumOfPublications += data["sole_author_data"][i]
        
        print "sole_author_data: " + str(overallPublications)
        self.assertEqual(overallPublications, sumOfPublications, "overall column does not equal sum of all columns")

    def test_degrees_separation(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "DegreesSample.xml")))
        
        g = {}
        authors = db.authors
        publications = db.publications
        for index, author in enumerate(authors):
            g[index] = []
        for publication in publications:
            for author in publication.authors:
                for authorToAdd in publication.authors:
                    if (authorToAdd != author):
                        if authorToAdd not in g[author]:
                            g[author].append(authorToAdd)
                        #print authorToAdd
                        #print author
                        if author not in g[authorToAdd]:
                            g[authorToAdd].append(author)
        
        # Author A - 0
        # Author B - 1
        # Author C - 4
        # Author D - 2
        # Author E - 3
        # Author F - 5
        
        # C <--> D
        degrees, author_path = db.get_degrees_seperation(g, 4,2)
        self.assertEqual(degrees, 1, "Author C and D not correct distance")
        
        # A <--> B
        degrees, author_path = db.get_degrees_seperation(g, 0,1)
        self.assertEqual(degrees, 0, "Author A and B not correct distance")
        
        # E <--> C
        degrees, author_path = db.get_degrees_seperation(g, 3,4)
        self.assertEqual(degrees, 2, "Author A and B not correct distance")
        
        # A <--> F
        degrees, author_path = db.get_degrees_seperation(g, 0,5)
        self.assertEqual(degrees, "x", "Author A and B not correct distance")
        
    def test_get_coauthors(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "dblp_curated_sample.xml")))
        
        author = 667 # A. McNab
        coauthors = db.get_coauthors(author)
        self.assertEqual(len(coauthors), 7, "Incorrect number of coauthors")
        
        # Coauthors
        # Jay Chin 224
        # Aleksandra nenadic 293
        # Alan 80
        # Qi Shi 342
        # Li Yao 666
        # Ning Zhang 223
        # Carole A. Gobole 31
        
        self.assertTrue (224 in coauthors, "Jay chin not present")
        self.assertTrue (293 in coauthors, "JAleksandra nenadic not present")
        self.assertTrue (80 in coauthors, "Alan not present")
        self.assertTrue (342 in coauthors, "Qi Shi not present")
        self.assertTrue (666 in coauthors, "Li yao not present")
        self.assertTrue (223 in coauthors, "Ning zhang not present")
        self.assertTrue (31 in coauthors, "Carole a. gobole not present")
        
        self.assertTrue (0 not in coauthors, "Stefano ceri wrongly present")
        

if __name__ == '__main__':
    unittest.main()
