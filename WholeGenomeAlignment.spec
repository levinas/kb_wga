/*
A KBase module: WholeGenomeAlignment
*/

module WholeGenomeAlignment {

	/*
		Run Mugsy.

		workspace_name - the name of the workspace for input/output
        input_genome_refs - input list of references to genome objects
  		output_alignment_name - the name of the output alignment

        minlength - minimum span of an aligned region in a colinear block (bp), default 30
        distance - maximum distance along a single sequence (bp) for chaining
                   anchors into locally colinear blocks (LCBs), default 1000

        @optional minlength
        @optional distance
    */
    typedef structure {
        string workspace_name;
        list<string> input_genome_names;

        int minlength;
        int distance;
    } MugsyParams;

	typedef structure {
		string report_name;
        string report_ref;
	} MugsyOutput;

    funcdef run_mugsy(MugsyParams params) returns (MugsyOutput output)
        authentication required;
};
