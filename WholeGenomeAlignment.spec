/*
A KBase module: WholeGenomeAlignment
*/

module WholeGenomeAlignment {

    /*
        Run Mugsy.

        workspace_name - the name of the workspace for input/output
        input_genomeset_ref - optional input reference to genome set
        input_genome_refs - optional input list of references to genome objects
        output_alignment_name - the name of the output alignment

        minlength - minimum span of an aligned region in a colinear block (bp), default 30
        distance - maximum distance along a single sequence (bp) for chaining
                   anchors into locally colinear blocks (LCBs), default 1000

        @optional input_genomeset
        @optional input_genome_names
        @optional minlength
        @optional distance
    */
    typedef structure {
        string workspace_name;
        string input_genomeset;
        list<string> input_genome_names;
        string output_alignment_name;

        int minlength;
        int distance;
        float max_breakpoint_distance_scale;
		float conservation_distance_scale;
		float hmm_identity;
    } MugsyParams;

    typedef structure {
        string report_name;
        string report_ref;
    } WGAOutput;

    typedef MugsyParams MauveParams;

    funcdef run_mugsy(MugsyParams params) returns (WGAOutput output)
        authentication required;

    funcdef run_mauve(MauveParams params) returns (WGAOutput output)
        authentication required;
};
