import connexion
import six

from swagger_server.models.city_data import CityData  # noqa: E501
from swagger_server.models.error import Error  # noqa: E501
from swagger_server import util
from swagger_server.__main__ import rj, Path

from qwikidata.sparql import return_sparql_query_results


def query_wikidata(sparql_query):
    """query_wikidata

    :param sparql_query: Sparql query
    :type sparql_query: str

    :rtype: list of objects of objects of type dict
    """
    res = return_sparql_query_results(sparql_query)
    obj_json = res['results']['bindings']
    return obj_json


def get_cities_data(name=None):  # noqa: E501
    """get_city_data

    Retrieve information about cities with a given name.
    If no cities with this name found, return empty list

    :param name: City name
    :type name: str

    :rtype: list of objects of type CityData
    """
    name = name.title()
    sparql_query = f'''
    SELECT DISTINCT ?name ?country ?population ?postal_code WHERE
    {{
        ?object wdt:P31/wdt:P279* wd:Q515;
                wdt:P1082 ?population;
                wdt:P17   ?country_obj;
                wdt:P281  ?postal_code.
        ?object rdfs:label|skos:altLabel "{name}"@en.
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en".
                                  ?object rdfs:label ?name.
                                  ?country_obj rdfs:label ?country.
                               }}
    }}
    '''

    cities_json = rj.jsonget(name)
    if not cities_json:
        cities_json = query_wikidata(sparql_query)
        rj.jsonset(name, Path('.'), cities_json)
        seconds = 60 * 60 * 24
        rj.expire(name, seconds)

    return cities_json if cities_json else \
        Error(code=404, message='City not found')
