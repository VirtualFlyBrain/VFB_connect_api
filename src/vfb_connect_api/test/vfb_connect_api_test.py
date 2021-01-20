import unittest
import json
from vfb_connect_api.app import app
from flask import Flask, Blueprint
from vfb_connect_api.restplus import api
from vfb_connect_api.endpoints.vfb_connect_api import ns as api_namespace

app = Flask(__name__)

# config should be same with app.py
blueprint = Blueprint('vfb_connect_api', __name__, url_prefix='/vfb_connect_api')
api.init_app(blueprint)
api.add_namespace(api_namespace)
app.register_blueprint(blueprint)


class TermQueryApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_term_info_basic(self):
        response = self.app.get("""/vfb_connect_api/vfb/get_term_info?ID_list=['VFB_00010001']""")
        self.assertEqual(200, response.status_code)

        response_data = json.loads(response.get_data())
        print(response_data)
        self.assertEqual(1, len(response_data))
        self.assertEqual("2ea49d2", response_data[0]["version"])
        self.assertEqual("Get JSON for Individual:Anatomy", response_data[0]["query"])
        self.assertEqual("http://virtualflybrain.org/reports/VFB_00010001", response_data[0]["term"]["core"]["iri"])

    def test_get_term_info_not_found(self):
        response = self.app.get("""/vfb_connect_api/vfb/get_term_info?ID_list=['not_exists']""")
        self.assertEqual(200, response.status_code)

        response_data = json.loads(response.get_data())
        self.assertEqual(0, len(response_data))

    def test_get_term_info_multi_param(self):
        response = self.app.get("""/vfb_connect_api/vfb/get_term_info?ID_list=['VFB_00010001', 'VFB_00010002']""")
        self.assertEqual(200, response.status_code)

        response_data = json.loads(response.get_data())
        self.assertEqual(2, len(response_data))

    def test_get_term_info_missing_param(self):
        response = self.app.get("""/vfb_connect_api/vfb/get_term_info""")
        self.assertEqual(400, response.status_code)

        response_data = json.loads(response.get_data())
        print(response_data)
        self.assertEqual("Error: No ID_list field provided. Please specify an ID_list.", response_data["message"])

    def test_get_term_info_empty_param(self):
        response = self.app.get("""/vfb_connect_api/vfb/get_term_info?ID_list=""")
        self.assertEqual(200, response.status_code)

        response_data = json.loads(response.get_data())
        self.assertEqual(0, len(response_data))


class SubclassesApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_subclasses_basic(self):
        response = self.app.get("""/vfb_connect_api/vfb/get_subclasses?query='XXX'""")
        self.assertEqual(200, response.status_code)

        response_data = json.loads(response.get_data())
        print(response_data)
        self.assertEqual(1, len(response_data))
        self.assertEqual("2ea49d2", response_data[0]["version"])
        self.assertEqual("Get JSON for Individual:Anatomy", response_data[0]["query"])
        self.assertEqual("http://virtualflybrain.org/reports/VFB_00010001", response_data[0]["term"]["core"]["iri"])

    def test_get_subclasses_not_found(self):
        response = self.app.get("""/vfb_connect_api/vfb/get_term_info?ID_list=['not_exists']""")
        self.assertEqual(200, response.status_code)

        response_data = json.loads(response.get_data())
        self.assertEqual(0, len(response_data))

    def test_get_subclasses_missing_param(self):
        response = self.app.get("""/vfb_connect_api/vfb/get_term_info""")
        self.assertEqual(400, response.status_code)

        response_data = json.loads(response.get_data())
        print(response_data)
        self.assertEqual("The browser (or proxy) sent a request that this server could not understand.",
                         response_data["message"])

    def test_get_subclasses_empty_param(self):
        response = self.app.get("""/vfb_connect_api/vfb/get_term_info?ID_list=""")
        self.assertEqual(200, response.status_code)

        response_data = json.loads(response.get_data())
        self.assertEqual(0, len(response_data))


class InstancesApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_instances_basic(self):
        response = self.app.get("""/vfb_connect_api/vfb/get_instances?query='larval subesophageal """
                                """zone cypress neuron'""")
        self.assertEqual(200, response.status_code)

        response_data = json.loads(response.get_data())
        print(response_data)
        self.assertEqual(2, len(response_data))
        self.assertEqual("http://virtualflybrain.org/reports/VFB_00100184", response_data[0]["term"]["core"]["iri"])
        self.assertEqual("http://virtualflybrain.org/reports/VFB_00100173", response_data[1]["term"]["core"]["iri"])

    def test_get_instances_not_found(self):
        response = self.app.get("""/vfb_connect_api/vfb/get_instances?query='not_exists'""")
        self.assertEqual(400, response.status_code)

        response_data = json.loads(response.get_data())
        self.assertEqual("Query includes unknown term label: 'not_exists'", response_data["message"])

    def test_get_instances_missing_param(self):
        response = self.app.get("""/vfb_connect_api/vfb/get_instances""")
        self.assertEqual(400, response.status_code)

        response_data = json.loads(response.get_data())
        print(response_data)
        self.assertEqual("The browser (or proxy) sent a request that this server could not understand.",
                         response_data["message"])

    def test_get_instances_empty_param(self):
        response = self.app.get("""/vfb_connect_api/vfb/get_instances?query=""")
        self.assertEqual(400, response.status_code)

        response_data = json.loads(response.get_data())
        self.assertEqual("Error: query cannot be empty.", response_data["message"])


class DBsApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_dbs_basic(self):
        response = self.app.get("""/vfb_connect_api/vfb/get_dbs""")
        self.assertEqual(200, response.status_code)

        response_data = json.loads(response.get_data())
        print(response_data)
        self.assertTrue(len(response_data) > 10)
        self.assertTrue("FlyCircuit" in response_data)
        self.assertTrue("FlyBase" in response_data)
        self.assertTrue("FlyBrain_NDB" in response_data)


class TermXrefApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_term_xref_basic(self):
        response = self.app.get("""/vfb_connect_api/vfb/get_term_info_by_xref?accession=['17545695']""")
        self.assertEqual(200, response.status_code)

        response_data = json.loads(response.get_data())
        print(response_data)
        self.assertEqual(1, len(response_data))
        self.assertEqual("Get JSON for Individual:Anatomy", response_data[0]["query"])
        self.assertEqual("http://virtualflybrain.org/reports/VFB_00100184", response_data[0]["term"]["core"]["iri"])

    def test_get_term_xref_not_found(self):
        response = self.app.get("""/vfb_connect_api/vfb/get_term_info_by_xref?accession=['not_exists']""")
        self.assertEqual(200, response.status_code)

        response_data = json.loads(response.get_data())
        self.assertEqual(0, len(response_data))

    def test_get_term_xref_multi_param(self):
        response = self.app.get("""/vfb_connect_api/vfb/get_term_info_by_xref?accession=['17545695', '10958111']""")
        self.assertEqual(200, response.status_code)

        response_data = json.loads(response.get_data())
        self.assertEqual(2, len(response_data))
        self.assertEqual("http://virtualflybrain.org/reports/VFB_001001bs", response_data[0]["term"]["core"]["iri"])
        self.assertEqual("http://virtualflybrain.org/reports/VFB_00100184", response_data[1]["term"]["core"]["iri"])

    def test_get_term_xref_missing_param(self):
        response = self.app.get("""/vfb_connect_api/vfb/get_term_info_by_xref""")
        self.assertEqual(400, response.status_code)

        response_data = json.loads(response.get_data())
        print(response_data)
        self.assertEqual("Error: No accession field provided. Please specify accession.",
                         response_data["message"])
        # self.assertEqual("The browser (or proxy) sent a request that this server could not understand.",
        #                  response_data["message"])

    def test_get_term_xref_empty_param(self):
        response = self.app.get("""/vfb_connect_api/vfb/get_term_info_by_xref?accession=""")
        self.assertEqual(200, response.status_code)

        response_data = json.loads(response.get_data())
        self.assertEqual(0, len(response_data))

    def test_get_term_xref_db(self):
        response = self.app.get("""/vfb_connect_api/vfb/get_term_info_by_xref?accession=['17545695']&db=catmaid_l1em""")
        self.assertEqual(200, response.status_code)

        response_data = json.loads(response.get_data())
        print(response_data)
        self.assertEqual(1, len(response_data))
        self.assertEqual("Get JSON for Individual:Anatomy", response_data[0]["query"])
        self.assertEqual("http://virtualflybrain.org/reports/VFB_00100184", response_data[0]["term"]["core"]["iri"])

    def test_get_term_xref_wrongdb(self):
        response = self.app.get("""/vfb_connect_api/vfb/get_term_info_by_xref?accession=['17545695']&db=not_exist""")
        self.assertEqual(200, response.status_code)

        response_data = json.loads(response.get_data())
        print(response_data)
        self.assertEqual(0, len(response_data))


class XrefsApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_xrefs_basic(self):
        response = self.app.get("""/vfb_connect_api/vfb/get_xrefs?ID_list=['10958111']""")
        self.assertEqual(200, response.status_code)

        response_data = json.loads(response.get_data())
        response_val = response_data['10958111']
        self.assertEqual(1, len(response_val))
        self.assertEqual("catmaid_fafb", response_val[0]["db"])
        self.assertEqual("VFB_001001bs", response_val[0]["vfb_id"])

    def test_get_xrefs_not_found(self):
        response = self.app.get("""/vfb_connect_api/vfb/get_xrefs?ID_list=['not_exists']""")
        self.assertEqual(200, response.status_code)

        response_data = json.loads(response.get_data())
        self.assertEqual(0, len(response_data))

    def test_get_xrefs_multi_param(self):
        response = self.app.get("""/vfb_connect_api/vfb/get_xrefs?ID_list=['10958111', '8336193']""")
        self.assertEqual(200, response.status_code)

        response_data = json.loads(response.get_data())
        print(response_data)
        self.assertEqual(2, len(response_data))

        response_val = response_data['10958111']
        self.assertEqual(1, len(response_val))
        self.assertEqual("catmaid_fafb", response_val[0]["db"])
        self.assertEqual("VFB_001001bs", response_val[0]["vfb_id"])

        response_val2 = response_data['8336193']
        self.assertEqual(1, len(response_val2))
        self.assertEqual("catmaid_fafb", response_val2[0]["db"])
        self.assertEqual("VFB_001000n4", response_val2[0]["vfb_id"])

    def test_get_xrefs_missing_param(self):
        response = self.app.get("""/vfb_connect_api/vfb/get_xrefs""")
        self.assertEqual(400, response.status_code)

        response_data = json.loads(response.get_data())
        print(response_data)
        self.assertEqual("Error: No ID_list field provided. Please specify ID_list.", response_data["message"])

    def test_get_xrefs_empty_param(self):
        response = self.app.get("""/vfb_connect_api/vfb/get_xrefs?ID_list=""")
        self.assertEqual(200, response.status_code)

        response_data = json.loads(response.get_data())
        self.assertEqual(0, len(response_data))

    def test_get_xrefs_db(self):
        response = self.app.get("""/vfb_connect_api/vfb/get_xrefs?ID_list=['10958111', '8336193']&db=catmaid_fafb""")
        self.assertEqual(200, response.status_code)

        response_data = json.loads(response.get_data())
        print(response_data)
        self.assertEqual(2, len(response_data))

        response_val = response_data['10958111']
        self.assertEqual(1, len(response_val))
        self.assertEqual("catmaid_fafb", response_val[0]["db"])
        self.assertEqual("VFB_001001bs", response_val[0]["vfb_id"])

        response_val2 = response_data['8336193']
        self.assertEqual(1, len(response_val2))
        self.assertEqual("catmaid_fafb", response_val2[0]["db"])
        self.assertEqual("VFB_001000n4", response_val2[0]["vfb_id"])

    def test_get_xrefs_wrong_db(self):
        response = self.app.get("""/vfb_connect_api/vfb/get_xrefs?ID_list=['10958111', '8336193']&db=not_exist""")
        self.assertEqual(200, response.status_code)

        response_data = json.loads(response.get_data())
        print(response_data)
        self.assertEqual(0, len(response_data))


class IDsApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_ids_basic(self):
        response = self.app.get("""/vfb_connect_api/vfb/get_ids_by_xref?acc_list=['VFB_001000n4']""")
        self.assertEqual(200, response.status_code)

        response_data = json.loads(response.get_data())
        print(response_data)
        response_val = response_data['VFB_001000n4']
        self.assertEqual(1, len(response_val))
        self.assertEqual("catmaid_fafb", response_val[0]["db"])
        self.assertEqual("8336193", response_val[0]["acc"])

    def test_get_ids_not_found(self):
        response = self.app.get("""/vfb_connect_api/vfb/get_ids_by_xref?acc_list=['not_exists']""")
        self.assertEqual(200, response.status_code)

        response_data = json.loads(response.get_data())
        self.assertEqual(0, len(response_data))

    def test_get_ids_multi_param(self):
        response = self.app.get("""/vfb_connect_api/vfb/get_ids_by_xref?acc_list=['VFB_001001bs', 'VFB_001000n4']""")
        self.assertEqual(200, response.status_code)

        response_data = json.loads(response.get_data())
        self.assertEqual(2, len(response_data))

        response_val = response_data['VFB_001001bs']
        self.assertEqual(1, len(response_val))
        self.assertEqual("catmaid_fafb", response_val[0]["db"])
        self.assertEqual("10958111", response_val[0]["acc"])

        response_val2 = response_data['VFB_001000n4']
        self.assertEqual(1, len(response_val2))
        self.assertEqual("catmaid_fafb", response_val2[0]["db"])
        self.assertEqual("8336193", response_val2[0]["acc"])

    def test_get_ids_missing_param(self):
        response = self.app.get("""/vfb_connect_api/vfb/get_ids_by_xref""")
        self.assertEqual(400, response.status_code)

        response_data = json.loads(response.get_data())
        print(response_data)
        self.assertEqual("Error: No acc_list field provided. Please specify acc_list.", response_data["message"])

    def test_get_ids_empty_param(self):
        response = self.app.get("""/vfb_connect_api/vfb/get_ids_by_xref?acc_list=""")
        self.assertEqual(200, response.status_code)

        response_data = json.loads(response.get_data())
        self.assertEqual(0, len(response_data))

    def test_get_ids_db(self):
        response = self.app.get(
            """/vfb_connect_api/vfb/get_ids_by_xref?acc_list=['VFB_001001bs', 'VFB_001000n4']&db=catmaid_fafb""")
        self.assertEqual(200, response.status_code)

        response_data = json.loads(response.get_data())
        self.assertEqual(2, len(response_data))

        response_val = response_data['VFB_001001bs']
        self.assertEqual(1, len(response_val))
        self.assertEqual("catmaid_fafb", response_val[0]["db"])
        self.assertEqual("10958111", response_val[0]["acc"])

        response_val2 = response_data['VFB_001000n4']
        self.assertEqual(1, len(response_val2))
        self.assertEqual("catmaid_fafb", response_val2[0]["db"])
        self.assertEqual("8336193", response_val2[0]["acc"])

    def test_get_ids_wrong_db(self):
        response = self.app.get(
            """/vfb_connect_api/vfb/get_ids_by_xref?acc_list=['VFB_001001bs', 'VFB_001000n4']&db=not_exist""")
        self.assertEqual(200, response.status_code)

        response_data = json.loads(response.get_data())
        print(response_data)
        self.assertEqual(0, len(response_data))


if __name__ == '__main__':
    unittest.main()
