from comp61542 import app
from comp61542.database import (database, mock_database)
import sys
import os

if len(sys.argv) == 1:
    dataset = "Mock"
    db = mock_database.MockDatabase()
else:
    data_file = sys.argv[1]
    path, dataset = os.path.split(data_file)
    print "Database: path=%s name=%s" % (path, dataset)
    db = database.Database()
    if db.read(data_file) == False:
        sys.exit(1)

app.config['DATASET'] = dataset
app.config['DATABASE'] = db

# create graph here
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
                    
                    
app.config['Graph'] = g

if "DEBUG" in os.environ:
    app.config['DEBUG'] = True

if "TESTING" in os.environ:
    app.config['TESTING'] = True

app.run(host='0.0.0.0', port=9292)
