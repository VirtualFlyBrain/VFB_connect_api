from flask_restplus import reqparse

get_term_info_arguments = reqparse.RequestParser()
get_term_info_arguments.add_argument('ID_list', type=str, action="append", required=True)
get_term_info_arguments.add_argument('Type', type=str, required=False)
get_term_info_arguments.add_argument('Filter', type=str, required=False)

get_subclasses_arguments = reqparse.RequestParser()
get_subclasses_arguments.add_argument('query', type=str, required=True)
get_subclasses_arguments.add_argument('Filter', type=str, required=False)

get_instances_arguments = reqparse.RequestParser()
get_instances_arguments.add_argument('query', type=str, required=True)
get_instances_arguments.add_argument('Filter', type=str, required=False)

get_term_xref_arguments = reqparse.RequestParser()
get_term_xref_arguments.add_argument('accession', type=str, action="append", required=True)
get_term_xref_arguments.add_argument('db', type=str, required=False)
get_term_xref_arguments.add_argument('Filter', type=str, required=False)

get_xrefs_arguments = reqparse.RequestParser()
get_xrefs_arguments.add_argument('ID_list', type=str, action="append", required=True)
get_xrefs_arguments.add_argument('db', type=str, required=False)

get_ids_arguments = reqparse.RequestParser()
get_ids_arguments.add_argument('acc_list', type=str, action="append", required=True)
get_ids_arguments.add_argument('db', type=str, required=False)
