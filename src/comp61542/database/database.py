from comp61542.statistics import average
import itertools
import numpy as np
from xml.sax import handler, make_parser, SAXException
from comp61542 import priorityDictionary

PublicationType = [
    "Conference Paper", "Journal", "Book", "Book Chapter"]

class Publication:
    CONFERENCE_PAPER = 0
    JOURNAL = 1
    BOOK = 2
    BOOK_CHAPTER = 3

    def __init__(self, pub_type, title, year, authors):
        self.pub_type = pub_type
        self.title = title
        if year:
            self.year = int(year)
        else:
            self.year = -1
        self.authors = authors

class Author:
    def __init__(self, name):
        self.name = name

class Stat:
    STR = ["Mean", "Median", "Mode"]
    FUNC = [average.mean, average.median, average.mode]
    MEAN = 0
    MEDIAN = 1
    MODE = 2

class Database:
    def read(self, filename):
        self.publications = []
        self.authors = []
        self.author_idx = {}
        self.min_year = None
        self.max_year = None

        handler = DocumentHandler(self)
        parser = make_parser()
        parser.setContentHandler(handler)
        infile = open(filename, "r")
        valid = True
        try:
            parser.parse(infile)
        except SAXException as e:
            valid = False
            print "Error reading file (" + e.getMessage() + ")"
        infile.close()

        for p in self.publications:
            if self.min_year == None or p.year < self.min_year:
                self.min_year = p.year
            if self.max_year == None or p.year > self.max_year:
                self.max_year = p.year

        return valid

    def get_all_author_ids(self):
        return self.author_idx.values()

    def get_all_authors(self):
        return self.author_idx.keys()

    def get_coauthors(self, author):
        coauthors = []
        for p in self.publications:
            if author in p.authors:
                for a in p.authors:
                    if a != author and a not in coauthors:
                        coauthors.append(a)
        return coauthors

    def get_coauthor_data(self, start_year, end_year, pub_type):
        coauthors = {}
        for p in self.publications:
            if ((start_year == None or p.year >= start_year) and
                (end_year == None or p.year <= end_year) and
                (pub_type == 4 or pub_type == p.pub_type)):
                for a in p.authors:
                    for a2 in p.authors:
                        if a != a2:
                            try:
                                coauthors[a].add(a2)
                            except KeyError:
                                coauthors[a] = set([a2])
        def display(db, coauthors, author_id):
            return "%s (%d)" % (db.authors[author_id].name, len(coauthors[author_id]))

        header = ("Author", "Co-Authors")
        data = []
        for a in coauthors:
            data.append([ display(self, coauthors, a),
                ", ".join([
                    display(self, coauthors, ca) for ca in coauthors[a] ]) ])

        return (header, data)
    
    def search_authors_by_name(self, name):
        header = ("Name", "Number of conference papers", "Number of journals", 
        "Number of books", "Number of book chapters", "Times appeared first", 
        "Times appeared last", "Times sole author", "Times coauthored a paper", 
        "Total appearences")
        
        sAuthors = []
        
        ## Whole last name
        for i in range(0, len(self.authors)):
            strArray = self.authors[i].name.split(" ")
            lastName = strArray[len(strArray)-1]
            if name.lower() == lastName.lower():
                sAuthors.append(i)
        
        ## Start of last name
        for i in range(0, len(self.authors)):
            strArray = self.authors[i].name.split(" ")
            lastName = strArray[len(strArray)-1]
            lastName = " " + lastName
            if (" " + name.lower()) in lastName.lower() and i not in sAuthors:
                sAuthors.append(i)

        ## Whole first name
        for i in range(0, len(self.authors)):
            strArray = self.authors[i].name.split(" ")
            firstName = strArray[0]
            if name.lower() == firstName.lower() and i not in sAuthors:
                sAuthors.append(i)
                
        ## start of first name
        for i in range(0, len(self.authors)):
            strArray = self.authors[i].name.split(" ")
            firstName = " " + strArray[0]
            if (" " + name.lower()) in firstName.lower() and i not in sAuthors:
                sAuthors.append(i)
                
        ## end of last name
        for i in range(0, len(self.authors)):
            strArray = self.authors[i].name.split(" ")
            lastName = strArray[len(strArray)-1]
            lastName = lastName + " "
            if (name.lower() + " ") in lastName.lower() and i not in sAuthors:
                sAuthors.append(i)
                
        ## rest
        for i in range(0, len(self.authors)):
            if name.lower() in self.authors[i].name.lower() and i not in sAuthors:
                sAuthors.append(i)

        astats = [ [0, 0, 0, 0, 0, 0, 0, 0] for _ in range(len(self.authors)) ]
        for p in self.publications:
            author_count = len(p.authors)
            for a in p.authors:
                astats[a][p.pub_type] += 1
                # Sole author
                if (author_count == 1):
                    astats[a][6] += 1
                # first author
                elif a == p.authors[0]:
                    astats[a][4] += 1
                # last author
                elif a == p.authors[author_count - 1]:
                    astats[a][5] += 1
                if author_count > 1:
                    astats[a][7] += 1
 
        data = [ [self.authors[i].name] + astats[i] + [astats[i][0] + astats[i][1] + astats[i][2] + astats[i][3]]
            for i in sAuthors ]
            
        for entry in data:
            entry[0] = ", ".join(entry[0].rsplit(None, 1)[::-1])
            
        indexes = sAuthors
            
        return (header, data, indexes)    
        
    def get_author_stats(self, author_id):
        author_stats = {}
        
        author = self.authors[author_id]
        
        header = ("Overall", "Journal Articles", "Conference Papers", "Books", "Book Chapters")        
        author_stats["header"] = header
        
        times_coauthored = [0,0,0,0,0]
        
        ##### Publication statistics
        pubstats = [0,0,0,0,0]
        
        for p in self.publications:
            author_count = len(p.authors)
            for a in p.authors:
                if (a == author_id and author_count > 1):
                    if (p.pub_type == 0):
                        times_coauthored[0] +=1
                        times_coauthored[2] +=1
                    elif (p.pub_type == 1):
                        times_coauthored[0] +=1
                        times_coauthored[1] +=1
                    elif (p.pub_type == 2):
                        times_coauthored[0] +=1
                        times_coauthored[3] +=1
                    elif (p.pub_type == 3):
                        times_coauthored[0] +=1
                        times_coauthored[4] +=1
                        
        author_stats["coauthor_data"] = times_coauthored
        
        for p in self.publications:
            for a in p.authors:
                if (a == author_id):
                    # conf = 0
                    # journal = 1
                    # book = 2
                    # bookchapter = 3
                    if p.pub_type == 0:
                        pubstats[0] += 1
                        pubstats[2] += 1
                    elif p.pub_type == 1:
                        pubstats[0] += 1
                        pubstats[1] += 1
                    elif p.pub_type == 2:
                        pubstats[0] += 1
                        pubstats[3] += 1
                    elif p.pub_type == 3:
                        pubstats[0] += 1
                        pubstats[4] += 1
                    
        author_stats["publications_data"] = pubstats
        
        ##### First Author Statistics     
        first_author_stats = [0,0,0,0,0]
        
        for p in self.publications:
            author_count = len(p.authors)
            if (p.authors[0] == author_id and author_count > 1):
                # conf = 0
                # journal = 1
                # book = 2
                # bookchapter = 3
                if p.pub_type == 0:
                    first_author_stats[0] += 1
                    first_author_stats[2] += 1
                elif p.pub_type == 1:
                    first_author_stats[0] += 1
                    first_author_stats[1] += 1
                elif p.pub_type == 2:
                    first_author_stats[0] += 1
                    first_author_stats[3] += 1
                elif p.pub_type == 3:
                    first_author_stats[0] += 1
                    first_author_stats[4] += 1
                        
        author_stats["first_author_data"] = first_author_stats
        
        ##### Last Author Statistics    
        last_author_stats = [0,0,0,0,0]
        
        for p in self.publications:
            author_count = len(p.authors)
            if (p.authors[author_count-1] == author_id and author_count > 1):
                # conf = 0
                # journal = 1
                # book = 2
                # bookchapter = 3
                if p.pub_type == 0:
                    last_author_stats[0] += 1
                    last_author_stats[2] += 1
                elif p.pub_type == 1:
                    last_author_stats[0] += 1
                    last_author_stats[1] += 1
                elif p.pub_type == 2:
                    last_author_stats[0] += 1
                    last_author_stats[3] += 1
                elif p.pub_type == 3:
                    last_author_stats[0] += 1
                    last_author_stats[4] += 1
                        
        author_stats["last_author_data"] = last_author_stats
        
        ##### Sole Author Statistics    
        sole_author_stats = [0,0,0,0,0]
        
        for p in self.publications:
            author_count = len(p.authors)
            if (p.authors[0] == author_id and author_count == 1):
                # conf = 0
                # journal = 1
                # book = 2
                # bookchapter = 3
                if p.pub_type == 0:
                    sole_author_stats[0] += 1
                    sole_author_stats[2] += 1
                elif p.pub_type == 1:
                    sole_author_stats[0] += 1
                    sole_author_stats[1] += 1
                elif p.pub_type == 2:
                    sole_author_stats[0] += 1
                    sole_author_stats[3] += 1
                elif p.pub_type == 3:
                    sole_author_stats[0] += 1
                    sole_author_stats[4] += 1
                        
        author_stats["sole_author_data"] = sole_author_stats
        author_stats["times_coauthored"] = times_coauthored
                        
        print author_stats
        
        return (author.name, author_stats)  

    # dijkstras algorithm used
    def get_degrees_seperation(self, g, author1, author2):
        D = {} # dictionary for final distance
        P = {} # dictionary of predecessors
        Q = priorityDictionary.priorityDictionary()
        Q[author1] = 0
        
        for v in Q:
            D[v] = Q[v]
            if v == author2: break;

            for w in g[v]:
                vwLength = D[v] + 1
                if w in D:
                    if vwLength < D[w]:
                        raise ValueError, "Dijkstra: found better path to already final vertext"
                elif w not in Q or vwLength <Q[w]:
                    Q[w] = vwLength
                    P[w] = v
        
        if author2 not in D:
            return "x", []
        
        path = []
        end = author2
        start = author1
        
	while 1:
		path.append(end)
		if end == start: break
		end = P[end]
	path.reverse()
        
        """
        print path
        authors = []
        for author in path:
            authors.append(self.authors[author].name)
            
        print authors
        """
        
        return (len(path)-2), path

    def get_average_authors_per_publication(self, av):
        header = ("Conference Paper", "Journal", "Book", "Book Chapter", "All Publications")

        auth_per_pub = [[], [], [], []]

        for p in self.publications:
            auth_per_pub[p.pub_type].append(len(p.authors))

        func = Stat.FUNC[av]

        data = [ func(auth_per_pub[i]) for i in np.arange(4) ] + [ func(list(itertools.chain(*auth_per_pub))) ]
        return (header, data)

    def get_average_publications_per_author(self, av):
        header = ("Conference Paper", "Journal", "Book", "Book Chapter", "All Publications")

        pub_per_auth = np.zeros((len(self.authors), 4))

        for p in self.publications:
            for a in p.authors:
                pub_per_auth[a, p.pub_type] += 1

        func = Stat.FUNC[av]

        data = [ func(pub_per_auth[:, i]) for i in np.arange(4) ] + [ func(pub_per_auth.sum(axis=1)) ]
        return (header, data)

    def get_average_publications_in_a_year(self, av):
        header = ("Conference Paper",
            "Journal", "Book", "Book Chapter", "All Publications")

        ystats = np.zeros((int(self.max_year) - int(self.min_year) + 1, 4))

        for p in self.publications:
            ystats[p.year - self.min_year][p.pub_type] += 1

        func = Stat.FUNC[av]

        data = [ func(ystats[:, i]) for i in np.arange(4) ] + [ func(ystats.sum(axis=1)) ]
        return (header, data)

    def get_average_authors_in_a_year(self, av):
        header = ("Conference Paper",
            "Journal", "Book", "Book Chapter", "All Publications")

        yauth = [ [set(), set(), set(), set(), set()] for _ in range(int(self.min_year), int(self.max_year) + 1) ]

        for p in self.publications:
            for a in p.authors:
                yauth[p.year - self.min_year][p.pub_type].add(a)
                yauth[p.year - self.min_year][4].add(a)

        ystats = np.array([ [ len(S) for S in y ] for y in yauth ])

        func = Stat.FUNC[av]

        data = [ func(ystats[:, i]) for i in np.arange(5) ]
        return (header, data)

    def get_publication_summary_average(self, av):
        header = ("Details", "Conference Paper",
            "Journal", "Book", "Book Chapter", "All Publications")

        pub_per_auth = np.zeros((len(self.authors), 4))
        auth_per_pub = [[], [], [], []]

        for p in self.publications:
            auth_per_pub[p.pub_type].append(len(p.authors))
            for a in p.authors:
                pub_per_auth[a, p.pub_type] += 1

        name = Stat.STR[av]
        func = Stat.FUNC[av]

        data = [
            [name + " authors per publication"]
                + [ func(auth_per_pub[i]) for i in np.arange(4) ]
                + [ func(list(itertools.chain(*auth_per_pub))) ],
            [name + " publications per author"]
                + [ func(pub_per_auth[:, i]) for i in np.arange(4) ]
                + [ func(pub_per_auth.sum(axis=1)) ] ]
        return (header, data)

    def get_publication_summary(self):
        header = ("Details", "Conference Paper",
            "Journal", "Book", "Book Chapter", "Total")

        plist = [0, 0, 0, 0]
        alist = [set(), set(), set(), set()]

        for p in self.publications:
            plist[p.pub_type] += 1
            for a in p.authors:
                alist[p.pub_type].add(a)
        # create union of all authors
        ua = alist[0] | alist[1] | alist[2] | alist[3]

        data = [
            ["Number of publications"] + plist + [sum(plist)],
            ["Number of authors"] + [ len(a) for a in alist ] + [len(ua)] ]
        return (header, data)

    def get_average_authors_per_publication_by_author(self, av):
        header = ("Author", "Number of conference papers",
            "Number of journals", "Number of books",
            "Number of book chapers", "All publications")

        astats = [ [[], [], [], []] for _ in range(len(self.authors)) ]
        for p in self.publications:
            for a in p.authors:
                astats[a][p.pub_type].append(len(p.authors))

        func = Stat.FUNC[av]

        data = [ [self.authors[i].name]
            + [ func(L) for L in astats[i] ]
            + [ func(list(itertools.chain(*astats[i]))) ]
            for i in range(len(astats)) ]
        return (header, data)


    def get_publications_by_author(self):
        header = ("Name", "Number of conference papers", "Number of journals", 
        "Number of books", "Number of book chapters", "Times appeared first", 
        "Times appeared last", "Times sole author", "Times coauthored a paper", 
        "Total appearences")

        astats = [ [0, 0, 0, 0, 0, 0, 0, 0] for _ in range(len(self.authors)) ]
        for p in self.publications:
            author_count = len(p.authors)
            for a in p.authors:
                astats[a][p.pub_type] += 1
                # Sole author
                if (author_count == 1):
                    astats[a][6] += 1
                # first author
                elif a == p.authors[0]:
                    astats[a][4] += 1
                # last author
                elif a == p.authors[author_count - 1]:
                    astats[a][5] += 1
                if author_count > 1:
                    astats[a][7] += 1
                

        data = [ [self.authors[i].name] + astats[i] + [astats[i][0] + astats[i][1] + astats[i][2] + astats[i][3]]
            for i in range(len(astats)) ]
            
        for entry in data:
            entry[0] = ", ".join(entry[0].rsplit(None, 1)[::-1])
        
        indexes = range(len(self.authors))
        
        return (header, data, indexes)

    def get_average_authors_per_publication_by_year(self, av):
        header = ("Year", "Conference papers",
            "Journals", "Books",
            "Book chapers", "All publications")

        ystats = {}
        for p in self.publications:
            try:
                ystats[p.year][p.pub_type].append(len(p.authors))
            except KeyError:
                ystats[p.year] = [[], [], [], []]
                ystats[p.year][p.pub_type].append(len(p.authors))

        func = Stat.FUNC[av]

        data = [ [y]
            + [ func(L) for L in ystats[y] ]
            + [ func(list(itertools.chain(*ystats[y]))) ]
            for y in ystats ]
        return (header, data)

    def get_publications_by_year(self):
        header = ("Year", "Number of conference papers",
            "Number of journals", "Number of books",
            "Number of book chapers", "Total")

        ystats = {}
        for p in self.publications:
            try:
                ystats[p.year][p.pub_type] += 1
            except KeyError:
                ystats[p.year] = [0, 0, 0, 0]
                ystats[p.year][p.pub_type] += 1

        data = [ [y] + ystats[y] + [sum(ystats[y])] for y in ystats ]
        return (header, data)

    def get_average_publications_per_author_by_year(self, av):
        header = ("Year", "Conference papers",
            "Journals", "Books",
            "Book chapers", "All publications")

        ystats = {}
        for p in self.publications:
            try:
                s = ystats[p.year]
            except KeyError:
                s = np.zeros((len(self.authors), 4))
                ystats[p.year] = s
            for a in p.authors:
                s[a][p.pub_type] += 1

        func = Stat.FUNC[av]

        data = [ [y]
            + [ func(ystats[y][:, i]) for i in np.arange(4) ]
            + [ func(ystats[y].sum(axis=1)) ]
            for y in ystats ]
        return (header, data)

    def get_author_totals_by_year(self):
        header = ("Year", "Number of conference papers",
            "Number of journals", "Number of books",
            "Number of book chapers", "Total")

        ystats = {}
        for p in self.publications:
            try:
                s = ystats[p.year][p.pub_type]
            except KeyError:
                ystats[p.year] = [set(), set(), set(), set()]
                s = ystats[p.year][p.pub_type]
            for a in p.authors:
                s.add(a)
        data = [ [y] + [len(s) for s in ystats[y]] + [len(ystats[y][0] | ystats[y][1] | ystats[y][2] | ystats[y][3])]
            for y in ystats ]
        return (header, data)

    def add_publication(self, pub_type, title, year, authors):
        if year == None or len(authors) == 0:
            print "Warning: excluding publication due to missing information"
            print "    Publication type:", PublicationType[pub_type]
            print "    Title:", title
            print "    Year:", year
            print "    Authors:", ",".join(authors)
            return
        if title == None:
            print "Warning: adding publication with missing title [ %s %s (%s) ]" % (PublicationType[pub_type], year, ",".join(authors))
        idlist = []
        for a in authors:
            try:
                idlist.append(self.author_idx[a])
            except KeyError:
                a_id = len(self.authors)
                self.author_idx[a] = a_id
                idlist.append(a_id)
                self.authors.append(Author(a))
        self.publications.append(
            Publication(pub_type, title, year, idlist))
        if (len(self.publications) % 100000) == 0:
            print "Adding publication number %d (number of authors is %d)" % (len(self.publications), len(self.authors))

        if self.min_year == None or year < self.min_year:
            self.min_year = year
        if self.max_year == None or year > self.max_year:
            self.max_year = year

    def _get_collaborations(self, author_id, include_self):
        data = {}
        for p in self.publications:
            if author_id in p.authors:
                for a in p.authors:
                    try:
                        data[a] += 1
                    except KeyError:
                        data[a] = 1
        if not include_self:
            del data[author_id]
        return data

    def get_coauthor_details(self, name):
        author_id = self.author_idx[name]
        data = self._get_collaborations(author_id, True)
        return [ (self.authors[key].name, data[key])
            for key in data ]

    def get_network_data(self):
        na = len(self.authors)

        nodes = [ [self.authors[i].name, -1] for i in range(na) ]
        links = set()
        for a in range(na):
            collab = self._get_collaborations(a, False)
            nodes[a][1] = len(collab)
            for a2 in collab:
                if a < a2:
                    links.add((a, a2))
        return (nodes, links)

class DocumentHandler(handler.ContentHandler):
    TITLE_TAGS = [ "sub", "sup", "i", "tt", "ref" ]
    PUB_TYPE = {
        "inproceedings":Publication.CONFERENCE_PAPER,
        "article":Publication.JOURNAL,
        "book":Publication.BOOK,
        "incollection":Publication.BOOK_CHAPTER }

    def __init__(self, db):
        self.tag = None
        self.chrs = ""
        self.clearData()
        self.db = db

    def clearData(self):
        self.pub_type = None
        self.authors = []
        self.year = None
        self.title = None

    def startDocument(self):
        pass

    def endDocument(self):
        pass

    def startElement(self, name, attrs):
        if name in self.TITLE_TAGS:
            return
        if name in DocumentHandler.PUB_TYPE.keys():
            self.pub_type = DocumentHandler.PUB_TYPE[name]
        self.tag = name
        self.chrs = ""

    def endElement(self, name):
        if self.pub_type == None:
            return
        if name in self.TITLE_TAGS:
            return
        d = self.chrs.strip()
        if self.tag == "author":
            self.authors.append(d)
        elif self.tag == "title":
            self.title = d
        elif self.tag == "year":
            self.year = int(d)
        elif name in DocumentHandler.PUB_TYPE.keys():
            self.db.add_publication(
                self.pub_type,
                self.title,
                self.year,
                self.authors)
            self.clearData()
        self.tag = None
        self.chrs = ""

    def characters(self, chrs):
        if self.pub_type != None:
            self.chrs += chrs
