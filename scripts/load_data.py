# -*- coding: utf-8 -*-

__author__ = "Toto <toto@toto.ch>"
__version__ = "0.0.0"
__copyright__ = "Copyright (c) 2009 Rero, Johnny Mariethoz"
__license__ = "Internal Use Only"

# import of standard modules
import sys
import os
from optparse import OptionParser
import pyelasticsearch


if __name__ == '__main__':

    usage = "usage: %prog [options]"

    parser = OptionParser(usage)

    parser.set_description ("Change It")



    parser.add_option ("-v", "--verbose", dest="verbose",
                       help="Verbose mode",
                       action="store_true", default=False)

    (options,args) = parser.parse_args ()

    if len(args) != 1:
        parser.error("Error: incorrect number of arguments, try --help")

    s = pyelasticsearch.ElasticSearch("http://localhost:9200")

    try:
        s.delete_index("test")
    except:
        pass

    s.create_index("test")
    mapping = {
        "doc" : {
            "properties" : {
                "my_id" : {
                    "type": "integer"
                },
                "title" : {
                    "type": "string",
                    "analyzer": "french"
                },
                "author" : {
                    "type": "multi_field",
                    "fields": {
                        "author": { "type": "string" },
                        "facet_author":   { "type": "string", "index": "not_analyzed" }
                    }
                }
            }
        }
    }

    print s.put_mapping(index="test", doc_type="doc", mapping=mapping)

    data_file = file(args[0])
    n = 0
    for line in data_file:
        line = line.replace("\n","").split(";")
        data = {
            "my_id": n,
            "author": line[0],
            "title": line[1],
            "director": line[2],
            "year": line[-1]
        }
        n += 1

        print s.index(index="test", doc_type="doc", doc=data, id=data["my_id"])
     
