from comp61542 import app
from database import database
from flask import (render_template, request)

def format_data(data):
    fmt = "%.2f"
    result = []
    for item in data:
        if type(item) is list:
            result.append(", ".join([ (fmt % i).rstrip('0').rstrip('.') for i in item ]))
        else:
            result.append((fmt % item).rstrip('0').rstrip('.'))
    return result

@app.route("/search")
def showSearch():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":"search"}
    args['title'] = "Search"
    return render_template("search.html", args=args)

@app.route("/search/authors")
def authorSearch():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":"search results"}
    args['title'] = "Search Results"
    args['tableID'] = "searchRes"
    name = "bob"
    
    if "name" in request.args:
        name = request.args.get("name")
    
    data = db.search_authors_by_name(name)
    if len(data[2]) == 1:
        args = {"dataset":dataset, "id":"search results"}
        author_name, args["data"] = db.get_author_stats(data[2][0])
        args['title'] = "Author Information: " + author_name
        return render_template('author.html', args=args)
    else:
        args['links'] = 1
        args["data"] = data
        return render_template("statistics_details.html", args=args)
    
@app.route("/author/<id>")
def showAuthorStats(id):
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":"search results"}

    author_name, args['data'] = db.get_author_stats(int(id))
    
    args['title'] = "Author Information: " + author_name
    
    return render_template('author.html', args=args)

@app.route("/degrees_of_separation")
def showDegreeOfSeperationSelector():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":"degrees of seperation"}
    args['title'] = "Degrees of Seperation"
    
    # get list of names
    authors = db.authors
    names = []
    for author in authors:
        names.append(author.name)
    
    # get ids, sort names, reorder ids
    ids = {}
    for index, name in enumerate(names):
        names[index] = ", ".join(name.rsplit(None, 1)[::-1])
        ids[names[index]] = index
    names.sort()
    newIds = []
    for name in names:
        newIds.append(ids[name])
    
    ## send arguments to args
    args['names'] = names
    args['ids'] = newIds
    
    return render_template('degreesSelector.html', args=args)

@app.route("/degrees_of_separation/results")
def showDegreeOfSeperationResults():
    dataset = app.config['DATASET']
    args = {"dataset":dataset}
    db = app.config['DATABASE']
    args['title'] = "Degrees of Seperation: results"
    
    author1 = 0
    author2 = 0
    if "author1" in request.args:
        author1 = request.args.get("author1")
    if "author2" in request.args:
        author2 = request.args.get("author2")
        
    g = app.config['Graph']
    degrees, path = db.get_degrees_seperation(g, int(author1), int(author2))
    
    path_names= []
    
    for author in path:
        path_names.append(db.authors[author].name)
    
        
    args['path'] = path_names
    if degrees == -1:
        degrees = 0
    args['degrees'] = degrees
    args['author1'] = db.authors[int(author1)].name
    args['author2'] = db.authors[int(author2)].name
    
    
    # get list of names
    authors = db.authors
    names = []
    for author in authors:
        names.append(author.name)
    
    # get ids, sort names, reorder ids
    ids = {}
    for index, name in enumerate(names):
        names[index] = ", ".join(name.rsplit(None, 1)[::-1])
        ids[names[index]] = index
    names.sort()
    newIds = []
    for name in names:
        newIds.append(ids[name])
    
    ## send arguments to args
    args['names'] = names
    args['ids'] = newIds

    return render_template('degreesResults.html', args=args)

@app.route("/coauthor_network")
def showCoauthorNetwork():
    dataset = app.config['DATASET']
    args = {"dataset":dataset}
    db = app.config['DATABASE']
    args['title'] = "Coauthor Network"
    
    author = 0
    
    if "author" in request.args:
        author = int(request.args.get("author"))
    coauthors = db.get_coauthors(author)
    
    coauthor_names = []
    
    for a in coauthors:
        coauthor_names.append(db.authors[int(a)].name)
    
    args['author_id'] = author
    args['author_name'] = db.authors[author].name
    args['coauthor_ids'] = coauthors
    args['coauthor_names'] = coauthor_names
    
    return render_template("coauthor_network.html", args=args)

@app.route("/averages")
def showAverages():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":"averages"}
    args['title'] = "Averaged Data"
    tables = []
    headers = ["Average", "Conference Paper", "Journal", "Book", "Book Chapter", "All Publications"]
    averages = [ database.Stat.MEAN, database.Stat.MEDIAN, database.Stat.MODE ]
    tables.append({
        "id":1,
        "title":"Average Authors per Publication",
        "header":headers,
        "rows":[
                [ database.Stat.STR[i] ]
                + format_data(db.get_average_authors_per_publication(i)[1])
                for i in averages ] })
    tables.append({
        "id":2,
        "title":"Average Publications per Author",
        "header":headers,
        "rows":[
                [ database.Stat.STR[i] ]
                + format_data(db.get_average_publications_per_author(i)[1])
                for i in averages ] })
    tables.append({
        "id":3,
        "title":"Average Publications in a Year",
        "header":headers,
        "rows":[
                [ database.Stat.STR[i] ]
                + format_data(db.get_average_publications_in_a_year(i)[1])
                for i in averages ] })
    tables.append({
        "id":4,
        "title":"Average Authors in a Year",
        "header":headers,
        "rows":[
                [ database.Stat.STR[i] ]
                + format_data(db.get_average_authors_in_a_year(i)[1])
                for i in averages ] })

    args['tables'] = tables
    return render_template("averages.html", args=args)

@app.route("/coauthors")
def showCoAuthors():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    PUB_TYPES = ["Conference Papers", "Journals", "Books", "Book Chapters", "All Publications"]
    args = {"dataset":dataset, "id":"coauthors"}
    args["title"] = "Co-Authors"

    start_year = db.min_year
    if "start_year" in request.args:
        start_year = int(request.args.get("start_year"))

    end_year = db.max_year
    if "end_year" in request.args:
        end_year = int(request.args.get("end_year"))

    pub_type = 4
    if "pub_type" in request.args:
        pub_type = int(request.args.get("pub_type"))

    args["data"] = db.get_coauthor_data(start_year, end_year, pub_type)
    args["start_year"] = start_year
    args["end_year"] = end_year
    args["pub_type"] = pub_type
    args["min_year"] = db.min_year
    args["max_year"] = db.max_year
    args["start_year"] = start_year
    args["end_year"] = end_year
    args["pub_str"] = PUB_TYPES[pub_type]
    return render_template("coauthors.html", args=args)

@app.route("/")
def showStatisticsMenu():
    dataset = app.config['DATASET']
    args = {"dataset":dataset}
    return render_template('statistics.html', args=args)

@app.route("/statisticsdetails/<status>")
def showPublicationSummary(status):
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":status}

    if (status == "publication_summary"):
        args["title"] = "Publication Summary"
        args["data"] = db.get_publication_summary()
        args['tableID'] = "pubSummary"

    if (status == "publication_author"):
        args["title"] = "Author Publication"
        args["data"] = db.get_publications_by_author()
        args['tableID'] = "authPub"
        args['links'] = 1

    if (status == "publication_year"):
        args["title"] = "Publication by Year"
        args["data"] = db.get_publications_by_year()
        args['tableID'] = "pubYear"

    if (status == "author_year"):
        args["title"] = "Author by Year"
        args["data"] = db.get_author_totals_by_year()
        args['tableID'] = "authYear"

    return render_template('statistics_details.html', args=args)
