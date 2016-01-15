#BEGIN_HEADER
import os
import sys
import traceback
import json
import logging
import subprocess
import tempfile
import uuid

from datetime import datetime

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

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
    A KBase module: WholeGenomeAlignment
    '''

    ######## WARNING FOR GEVENT USERS #######
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    #########################################
    #BEGIN_CLASS_HEADER
    workspaceURL = None

    # target is a list for collecting log messages
    def log(self, target, message):
        # we should do something better here...
        if target is not None:
            target.append(message)
        logger.info(message)

    def contigset_to_fasta(self, contigset, fasta_file):
        records = []
        for contig in contigset['contigs']:
            record = SeqRecord(Seq(contig['sequence']), id=contig['id'], description='')
            records.append(record)
        SeqIO.write(records, fasta_file, "fasta")

    def create_temp_json(self, attrs):
        f = tempfile.NamedTemporaryFile(delete=False)
        outjson = f.name
        f.write(json.dumps(attrs))
        f.close()
        return outjson
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.workspaceURL = config['workspace-url']
        self.scratch = os.path.abspath(config['scratch'])
        if not os.path.exists(self.scratch):
            os.makedirs(self.scratch)
        #END_CONSTRUCTOR
        pass

    def run_mugsy(self, ctx, params):
        # ctx is the context object
        # return variables are: output
        #BEGIN run_mugsy

        logger.info("params={}".format(json.dumps(params)))

        token = ctx["token"]
        ws = workspaceService(self.workspaceURL, token=token)
        wsid = None

        genomeset = None
        if "input_genomeset_ref" in params and params["input_genomeset_ref"] is not None:
            logger.info("Loading GenomeSet object from workspace")
            objects = ws.get_objects([{"ref": params["input_genomeset_ref"]}])
            genomes = objects[0]["data"]
            wsid = objects[0]['info'][6]

        genome_refs = []
        if genomeset is not None:
            for param_key in genomeset["elements"]:
                genome_refs.append(genomeset["elements"][param_key]["ref"])
            logger.info("Genome references from genome set: {}".format(genome_refs))

        if "input_genome_refs" in params and params["input_genome_refs"] is not None:
            for genome_ref in params["input_genome_refs"]:
                if genome_ref is not None:
                    genome_refs.append(genome_ref)

        logger.info("Final list of genome references: {}".format(genome_refs))
        if len(genome_refs) < 2:
            raise ValueError("Number of genomes should be more than 1")
        if len(genome_refs) > 10:
            raise ValueError("Number of genomes exceeds 10, which is too many for mugsy")

        timestamp = int((datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds()*1000)
        output_dir = os.path.join(self.scratch, 'output.'+str(timestamp))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        fasta_files = []
        for pos, ref in enumerate(genome_refs):
            logger.info("Loading Genome object from workspace for ref: ".format(ref))

            obj = ws.get_objects([{"ref": ref}])[0]
            data = obj["data"]
            info = obj["info"]
            wsid = wsid or info[6]
            type_name = info[2].split('.')[1].split('-')[0]
            logger.info("type_name = {}".format(type_name))

            # if KBaseGenomes.ContigSet
            if type_name == 'Genome':
                contigset_ref = data["contigset_ref"]
                obj = ws.get_objects([{"ref": contigset_ref}])[0]
                data = obj["data"]
                info = obj["info"]
                # logger.info("data = {}".format(json.dumps(data)))

            fasta_name = os.path.join(output_dir, "{}.fa".format(pos+1))
            self.contigset_to_fasta(data, fasta_name)
            fasta_files.append(fasta_name)

            # data_ref = str(info[6]) + "/" + str(info[0]) + "/" + str(info[4])

            # logger.info("info = {}".format(json.dumps(info)))
            # logger.info("data = <<<<<<{}>>>>>>".format(json.dumps(data)))

        logger.info("fasta_files = {}".format(fasta_files))

        logger.info("Run Mugsy:")

        cmd = ['mugsy', '-p', 'out', '--directory', output_dir ]
        cmd += fasta_files

        logger.info("CMD: {}".format(' '.join(cmd)))
        p = subprocess.Popen(cmd,
                             cwd = self.scratch,
                             stdout = subprocess.PIPE,
                             stderr = subprocess.STDOUT, shell = False)

        console = []
        while True:
            line = p.stdout.readline()
            if not line: break
            self.log(console, line.replace('\n', ''))

        p.stdout.close()
        p.wait()
        logger.debug('return code: {}'.format(p.returncode))
        if p.returncode != 0:
            raise ValueError('Error running mugsy, return code: {}\n\n{}'.format(p.returncode, '\n'.join(console)))


        report = 'Genomes/ContigSets aligned with Mugsy:\n'
        for pos, ref in enumerate(genome_refs):
            name = ref.split('/')[1]
            report += '  {}: {}\n'.format(pos+1, name)

        report += '\n\n============= MAF output =============\n\n'
        maf_file = os.path.join(output_dir, 'out.maf')
        with open(maf_file, 'r') as f:
            maf = f.read()
            report += maf

        print(report)

        aln_fata = os.path.join(output_dir, 'aln.fasta')
        cmdstr = 'maf2fasta.pl < {} > {}'.format(maf_file, aln_fasta)
        logger.debug('CMD: {}'.format(cmdstr))
        subprocess.check_call(cmdstr, shell=True)

        # Warning: this reads everything into memory!  Will not work if
        # the contigset is very large!
        contigset_data = {
            'id': 'mugsy.aln',
            'source': 'User assembled contigs from reads in KBase',
            'source_id':'none',
            'md5': 'md5 of what? concat seq? concat md5s?',
            'contigs':[]
        }

        lengths = []
        for seq_record in SeqIO.parse(aln_fasta, 'fasta'):
            contig = {
                'id': seq_record.id,
                'name': seq_record.name,
                'description': seq_record.description,
                'length': len(seq_record.seq),
                'sequence': str(seq_record.seq),
                'md5': hashlib.md5(str(seq_record.seq)).hexdigest()
            }
            lengths.append(contig['length'])
            contigset_data['contigs'].append(contig)


        # provenance
        input_ws_objects = []
        if "input_genomeset_ref" in params and params["input_genomeset_ref"] is not None:
            input_ws_objects.append(params["input_genomeset_ref"])
        if "input_genome_refs" in params and params["input_genome_refs"] is not None:
            for genome_ref in params["input_genome_refs"]:
                if genome_ref is not None:
                    input_ws_objects.append(genome_ref)

        provenance = None
        if "provenance" in ctx:
            provenance = ctx["provenance"]
        else:
            logger.info("Creating provenance data")
            provenance = [{"service": "WholeGenomeAlignment",
                           "method": "run_mugsy",
                           "method_params": [params]}]

        provenance[0]["input_ws_objects"] = input_ws_objects
        provenance[0]["description"] = "whole genome alignment using mugsy"


        reportObj = {
            # FIXME: change ref to FASTA alignment
            # 'objects_created':[{'ref':params['workspace_name']+'/'+params['output_contigset_name'], 'description':'Assembled contigs'}],
            'objects_created':[{'ref':input_ws_objects[0], 'description':'Mugsy report'}],
            'text_message': report
        }

        reportName = '{}.report.{}'.format('run_mugsy', hex(uuid.getnode()))
        report_obj_info = ws.save_objects({
                # 'workspace': params["workspace_name"],
            'id': wsid,
            'objects': [
                {
                    'type': 'KBaseReport.Report',
                    'data': reportObj,
                    'name': reportName,
                    'meta': {},
                    'hidden': 1,
                    'provenance': provenance
                }
            ]})[0]


        # shutil.rmtree(output_dir)

        output = {"report_name": reportName, 'report_ref': str(report_obj_info[6]) + '/' + str(report_obj_info[0]) + '/' + str(report_obj_info[4]) }

        #END run_mugsy

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_mugsy return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
