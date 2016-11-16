import unittest
import os
import json
import time
import logging

from os import environ
from ConfigParser import ConfigParser
from pprint import pprint

from biokbase.workspace.client import Workspace as workspaceService
from WholeGenomeAlignment.WholeGenomeAlignmentImpl import WholeGenomeAlignment

logging.basicConfig(format="[%(asctime)s %(levelname)s %(name)s] %(message)s",
                    level=logging.INFO)
logger = logging.getLogger(__name__)


class WholeGenomeAlignmentTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        cls.ctx = {'token': token, 'provenance': [{'service': 'WholeGenomeAlignment',
            'method': 'please_never_use_it_in_production', 'method_params': []}],
            'authenticated': 1}
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('WholeGenomeAlignment'):
            cls.cfg[nameval[0]] = nameval[1]
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL, token=token)
        cls.serviceImpl = WholeGenomeAlignment(cls.cfg)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        if hasattr(self.__class__, 'wsName'):
            return self.__class__.wsName
        suffix = int(time.time() * 1000)
        wsName = "test_WholeGenomeAlignment_" + str(suffix)
        ret = self.getWsClient().create_workspace({'workspace': wsName})
        self.__class__.wsName = wsName
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx


    def getGenomeSetInfo(self):
        testFile = './params.json'
        if os.path.exists(testFile):
            logger.info("Reading input from {}".format(testFile))
            with open(testFile) as testInfoFile:
                return json.load(testInfoFile)

    def test_run_mugsy(self):
        params = self.getGenomeSetInfo()
        if not params.get('output_alignment_name'):
            params['output_alignment_name'] = 'output.alignment'

        logger.info(json.dumps(params))

        result = self.getImpl().run_mugsy(self.getContext(),params)
        logger.info(result)

    def test_run_mauve(self):
        params = self.getGenomeSetInfo()
        if not params.get('output_alignment_name'):
            params['output_alignment_name'] = 'output.alignment'

        logger.info(json.dumps(params))

        result = self.getImpl().run_mauve(self.getContext(),params)
        logger.info(result)
