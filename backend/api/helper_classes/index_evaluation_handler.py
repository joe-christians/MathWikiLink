import os
import json

from ..formula_index_retrieval import employ_index


class IndexEvaluationHandler:

    def __init__(self, index_type):
        self.index_type = index_type
        if self.index_type == 'identifier':
            self.identifier_dict = self.read_index_file()
        elif self.index_type == 'formula':
            self.formula_index, self.qid_index = self.read_index_file()

    def read_index_file(self):
        """
        Read the file containing the identifier index.
        :return: The read file as a string.
        """
        if self.index_type == 'identifier':
            path = os.path.join('dataset', 'identifier_index.json')
            with open(path, 'r') as json_file:
                identifier_dict = json.load(json_file)
            return identifier_dict
        elif self.index_type == 'formula':
            # load formula index
            path = os.path.join('dataset/')
            with open(path + 'formula_string_index.json', 'r') as f:
                formula_index = json.load(f)
            # load qid index
            with open(path + 'formula_qid_index.json', 'r') as f:
                qid_index = json.load(f)
            return formula_index,qid_index

    def check_identifier_index(self, symbol, limit):
        results = {}

        symbol = symbol if symbol in self.identifier_dict else '\\{}'.format(symbol)
        if symbol in self.identifier_dict:
            identifier_dict_symbol = self.identifier_dict[symbol]

            for source_dict in identifier_dict_symbol:
                for source, entries in source_dict.items():

                    for positions in entries:
                        try:
                            positions.pop('value')
                        except:
                            pass

                        try:
                            positions.pop('item_description')
                        except:
                            pass

                    results[source] = entries[:limit]

        return results

    def check_formula_index(self, formula, limit):
        results = employ_index(formula, limit, self.formula_index, self.qid_index)

        for result in results['wikidata1Results']:
            result.pop('score')

        return results


