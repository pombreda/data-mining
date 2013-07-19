from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("""
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
SELECT DISTINCT ?club ?stadium ?label ?abstract ?ground ?long ?lat {
?s foaf:page ?club .
?s rdf:type <http://dbpedia.org/class/yago/LaLigaClubs> .
?s dbpedia-owl:ground ?ground .
?ground foaf:page ?stadium .
?ground rdfs:label ?label .
?ground dbpedia-owl:abstract ?abstract .
?ground rdf:type <http://dbpedia.org/ontology/Stadium> .
OPTIONAL { ?ground geo:long ?long } .
OPTIONAL { ?ground geo:lat ?lat } .
FILTER (lang(?label) = "" || langMatches(lang(?label), "ES")) .
FILTER (lang(?abstract) = "" || langMatches(lang(?abstract), "ES")) .
}
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print result