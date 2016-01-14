#BEGIN_HEADER
import os
import sys
import traceback
import json
import logging
from biokbase.workspace.client import Workspace as workspaceService


logging.basicConfig(format="[%(asctime)s %(levelname)s %(name)s] %(message)s",
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

#END_HEADER


class WholeGenomeAlignment:
    '''
    Module Name:
    WholeGenomeAlignment
    Module Description:

This module contains multiple assembly methods:

    run_mugsy

    '''

    ######## WARNING FOR GEVENT USERS #######
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    #########################################
    #BEGIN_CLASS_HEADER
    workspaceURL = None
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.workspaceURL = config['workspace-url']
        #END_CONSTRUCTOR
        pass

    def run_mugsy(self, ctx, params):
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN run_mugsy

        logger.info("params={}".format(json.dumps(params)))

        token = ctx["token"]
        ws = workspaceService(self.workspaceURL, token=token)

        if "input_genome_refs" in params and params["input_genome_refs"] is not None:
            for genome_ref in params["input_genome_refs"]:
                if genome_ref is not None:
                    genome_refs.append(genome_ref)
            log = self.log_line(log, "Final list of genome references: " + ", ".join(genome_refs))
        if len(genome_refs) < 2:
            raise ValueError("Number of genomes should be more than 1")

        returnVal = {"report_name": "tmp_name",
                     "report_ref": "tmp_ref"}

        #END run_mugsy

        # At some point might do deeper type checking...
        if not isinstance(returnVal, object):
            raise ValueError('Method count_contigs return value ' +
                             'returnVal is not type object as required.')
        # return the results
        return [returnVal]
