Workflow Description Language (WDL)
===================================

The Workflow Description Language is a domain specific language for describing tasks and workflows in a clear and concise syntax.

WDL was inspired by the [Common Workflow Language](https://github.com/common-workflow-language/common-workflow-language) but WDL aims to be written and read by humans while still maintaining easy machine parseability.

Here is an example of a tool for running `bwa mem`.  This was ported from [bwa mem in CWL](https://github.com/common-workflow-language/common-workflow-language/blob/master/examples/draft-2/bwa-mem-tool.cwl)

```
task bwa-mem {
  command {
    bwa mem \
    ${prefix='-t ' cores?} \
    ${prefix='-I ' sep=',' type=array[int] min_std_max_min} \
    ${prefix='-m ' type=int minimum_seed_length} \
    ${type=uri reference} \
    ${type=array[uri] sep=' ' reads}
  }
  outputs {
    "output.bam" -> bam
    "${bam}.bai" -> bai
  }
  runtime {
    docker: "broadinstitute/bwa-mem:latest"
    memory: "5GB"
    cores: ${cores}
  }
}
```

Here the task is named, and has three sections: command, outputs, and runtime.

The 'command' section specifies the command line that this task runs with placeholders for parameters that the user must provide.  For example, `${type=array[uri] sep=' ' reads}` specifies that the user must provide a parameter called `reads` which is an array of URIs.

The 'outputs' section specifies which output files are important and which variables they should be stored as.

The 'runtime' section specifies any runtime needs for this task, like Docker containers, memory, CPU, standard in, standard out, etc.
