
package us.kbase.wholegenomealignment;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: MugsyParams</p>
 * <pre>
 * Run Mugsy.
 * workspace_name - the name of the workspace for input/output
 *         input_genome_refs - input list of references to genome objects
 *   output_alignment_name - the name of the output alignment
 *         minlength - minimum span of an aligned region in a colinear block (bp), default 30
 *         distance - maximum distance along a single sequence (bp) for chaining
 *    anchors into locally colinear blocks (LCBs), default 1000
 *         @optional minlength
 *         @optional distance
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_name",
    "input_genome_names",
    "minlength",
    "distance"
})
public class MugsyParams {

    @JsonProperty("workspace_name")
    private java.lang.String workspaceName;
    @JsonProperty("input_genome_names")
    private List<String> inputGenomeNames;
    @JsonProperty("minlength")
    private Long minlength;
    @JsonProperty("distance")
    private Long distance;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("workspace_name")
    public java.lang.String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(java.lang.String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public MugsyParams withWorkspaceName(java.lang.String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("input_genome_names")
    public List<String> getInputGenomeNames() {
        return inputGenomeNames;
    }

    @JsonProperty("input_genome_names")
    public void setInputGenomeNames(List<String> inputGenomeNames) {
        this.inputGenomeNames = inputGenomeNames;
    }

    public MugsyParams withInputGenomeNames(List<String> inputGenomeNames) {
        this.inputGenomeNames = inputGenomeNames;
        return this;
    }

    @JsonProperty("minlength")
    public Long getMinlength() {
        return minlength;
    }

    @JsonProperty("minlength")
    public void setMinlength(Long minlength) {
        this.minlength = minlength;
    }

    public MugsyParams withMinlength(Long minlength) {
        this.minlength = minlength;
        return this;
    }

    @JsonProperty("distance")
    public Long getDistance() {
        return distance;
    }

    @JsonProperty("distance")
    public void setDistance(Long distance) {
        this.distance = distance;
    }

    public MugsyParams withDistance(Long distance) {
        this.distance = distance;
        return this;
    }

    @JsonAnyGetter
    public Map<java.lang.String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(java.lang.String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public java.lang.String toString() {
        return ((((((((((("MugsyParams"+" [workspaceName=")+ workspaceName)+", inputGenomeNames=")+ inputGenomeNames)+", minlength=")+ minlength)+", distance=")+ distance)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
