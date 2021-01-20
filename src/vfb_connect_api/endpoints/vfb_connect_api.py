import ast

from flask import request
from flask_restplus import Resource, reqparse
from vfb_connect.cross_server_tools import VfbConnect
from vfb_connect_api.exception.api_exception import VfbApiException
from vfb_connect_api.restplus import api
from vfb_connect_api.endpoints.parser import get_term_info_arguments
from vfb_connect_api.endpoints.parser import get_subclasses_arguments
from vfb_connect_api.endpoints.parser import get_instances_arguments
from vfb_connect_api.endpoints.parser import get_term_xref_arguments
from vfb_connect_api.endpoints.parser import get_xrefs_arguments
from vfb_connect_api.endpoints.parser import get_ids_arguments

vc = VfbConnect()

ns = api.namespace('vfb', description='VFB Connect operations')


@ns.route('/get_term_info', methods=['GET'])
class TermInfoEndpoint(Resource):

    @api.expect(get_term_info_arguments, validate=True)
    def get(self):
        """
        Gets term information.

        Queries Neo4j  to retrieve term details.

        * Send list of term IDs (mandatory)

        ```
        ?ID_list=['FBbt_00003686', 'VFB_00010001']
        ```

        * Specify term type (optional)
        * Specify filter (optional)
        """

        id_list = []
        if 'ID_list' in request.args:
            if request.args['ID_list']:
                id_list = ast.literal_eval(request.args['ID_list'])
        else:
            raise VfbApiException("Error: No ID_list field provided. Please specify an ID_list.")

        return vc.neo_query_wrapper.get_TermInfo(id_list)


@ns.route('/get_subclasses', methods=['GET'])
class SubclassesEndpoint(Resource):

    @api.expect(get_subclasses_arguments, validate=True)
    def get(self):
        """
        Generates JSON report of all subclasses of the submitted term.

        Queries Neo4j  to retrieve term subclasses.

        * Term query (mandatory)
        ```
        ?query="larval subesophageal zone cypress neuron"
        ```

        * Specify filter (optional)

        """
        print("-"+request.args['query']+"-")
        print(type(request.args['query']))
        query = ""
        if 'query' in request.args:
            if request.args['query']:
                query = ast.literal_eval(request.args['query'])
        else:
            raise VfbApiException("Error: No query field provided. Please specify a query.")

        return vc.get_subclasses(query)


@ns.route('/get_instances', methods=['GET'])
class InstancesEndpoint(Resource):

    @api.expect(get_instances_arguments, validate=True)
    def get(self):
        """
        Generate JSON report of all images of the submitted type.

        Queries Neo4j  to retrieve term instances.

        * Term query (mandatory)

        * Specify filter (optional)

        """
        print("-"+request.args['query']+"-")
        print(type(request.args['query']))
        if 'query' in request.args:
            if request.args['query']:
                query = ast.literal_eval(request.args['query'])
            else:
                raise VfbApiException("Error: query cannot be empty.")
        else:
            raise VfbApiException("Error: No query field provided. Please specify a query.")

        return vc.get_images(query)


@ns.route('/get_dbs', methods=['GET'])
class DBsEndpoint(Resource):

    def get(self):
        """
        Lists all DBs in VFB.
        """

        return vc.neo_query_wrapper.get_dbs()


@ns.route('/get_term_info_by_xref', methods=['GET'])
class TermInfoXrefEndpoint(Resource):

    @api.expect(get_term_xref_arguments, validate=True)
    def get(self):
        """
        Gets term information by xref.

        Get terms in VFB corresponding to an accession

        * accession (mandatory): list of external DB IDs

        ```
        ?accession=['17545695']
        ```

        * db (optional): database identifier (short_form) in VFB

        ```
        db=catmaid_l1em
        ```

        * Specify filter (optional)
        """

        accession = []
        db = ""

        if "accession" in request.args:
            if request.args['accession']:
                accession = ast.literal_eval(request.args['accession'])
        else:
            raise VfbApiException("Error: No accession field provided. Please specify accession.")

        if 'db' in request.args:
            if request.args['db']:
                db = str(request.args['db'])

        return vc.neo_query_wrapper.get_terms_by_xref(accession, db)


@ns.route('/get_xrefs', methods=['GET'])
class XrefsEndpoint(Resource):

    @api.expect(get_xrefs_arguments, validate=True)
    def get(self):
        """
        Map an external ID (acc) to a VFB_id.

        Map an external ID (acc) to a VFB_id

        * ID_list (mandatory): list of external DB IDs

        ```
        ?ID_list=['17545695']
        ```

        * db (optional): database identifier (short_form) in VFB

        ```
        db=catmaid_l1em
        ```

        Return:

        ```
        { VFB_id : [{ db: <db> : acc : <acc> }]}
        ```
        """

        id_list = []
        db = ""

        if "ID_list" in request.args:
            if request.args['ID_list']:
                id_list = ast.literal_eval(request.args['ID_list'])
        else:
            raise VfbApiException("Error: No ID_list field provided. Please specify ID_list.")

        if 'db' in request.args:
            if request.args['db']:
                db = str(request.args['db'])

        return vc.neo_query_wrapper.xref_2_vfb_id(id_list, db)


@ns.route('/get_ids_by_xref', methods=['GET'])
class IDsEndpoint(Resource):

    @api.expect(get_ids_arguments, validate=True)
    def get(self):
        """
        Map a list of node short_form IDs in VFB to external DB IDs

        Map a list of node short_form IDs in VFB to external DB IDs

        * acc_list (mandatory): list of short_form IDs of nodes in the VFB KB

        ```
        ?acc_list=['17545695']
        ```

        * db (optional): database identifier (short_form) in VFB

        ```
        db=catmaid_l1em
        ```

        Return:

        ```
        { VFB_id : [{ db: <db> : acc : <acc> }]}
        ```
        """

        acc_list = []
        db = ""

        if "acc_list" in request.args:
            if request.args['acc_list']:
                acc_list = ast.literal_eval(request.args['acc_list'])
        else:
            raise VfbApiException("Error: No acc_list field provided. Please specify acc_list.")

        if 'db' in request.args:
            if request.args['db']:
                db = str(request.args['db'])

        return vc.neo_query_wrapper.vfb_id_2_xrefs(acc_list, db)
