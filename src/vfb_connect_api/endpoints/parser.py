from flask_restplus import reqparse

get_term_info_arguments = reqparse.RequestParser()
get_term_info_arguments.add_argument('ID_list', type=str, action="append", required=True, help="List of term IDs")
get_term_info_arguments.add_argument('Type', type=str, required=False)
get_term_info_arguments.add_argument('Filter', type=str, required=False)

get_subclasses_arguments = reqparse.RequestParser()
get_subclasses_arguments.add_argument('query', type=str, required=True, help="Term to get subclasses")
get_subclasses_arguments.add_argument('summary', type=bool, required=False, default=False,
                                      help="""'true' to get results in a summary format""")

get_instances_arguments = reqparse.RequestParser()
get_instances_arguments.add_argument('query', type=str, required=True, help="Term to get instances")
get_instances_arguments.add_argument('summary', type=bool, required=False, default=False,
                                     help="""'true' to get results in a summary format""")

get_term_xref_arguments = reqparse.RequestParser()
get_term_xref_arguments.add_argument('accession', type=str, action="append", required=True,
                                     help="List of external DB IDs")
get_term_xref_arguments.add_argument('db', type=str, required=False, help="Database identifier (short_form) in VFB")
get_term_xref_arguments.add_argument('Filter', type=str, required=False)

get_xrefs_arguments = reqparse.RequestParser()
get_xrefs_arguments.add_argument('ID_list', type=str, action="append", required=True, help="List of external DB IDs")
get_xrefs_arguments.add_argument('db', type=str, required=False, help="Database identifier (short_form) in VFB")

get_ids_arguments = reqparse.RequestParser()
get_ids_arguments.add_argument('acc_list', type=str, action="append", required=True,
                               help="List of short_form IDs of nodes in the VFB KB")
get_ids_arguments.add_argument('db', type=str, required=False, help="Database identifier (short_form) in VFB")
