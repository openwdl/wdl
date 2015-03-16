Workflow Description Language (WDL)
===================================

The Workflow Description Language is a domain specific language for describing tasks and workflows in a clear and concise syntax.

WDL was inspired by the [Common Workflow Language](https://github.com/common-workflow-language/common-workflow-language) but WDL aims to be written and read by humans while still maintaining easy machine parseability.

Here is an example of a tool for running `bwa mem`.  This was ported from [bwa mem in CWL](https://github.com/common-workflow-language/common-workflow-language/blob/master/examples/draft-2/bwa-mem-tool.cwl)

```
task bwa-mem {
  command {
    bwa mem \
    ${prefix='-t ' cpus?} \
    ${prefix='-I ' sep=',' type=array[int] min_std_max_min} \
    ${prefix='-m ' type=int minimum_seed_length} \
    ${type=file reference} \
    ${type=array[file] sep=' ' reads}
  }
  outputs {
    "output.bam" -> bam
    "${bam}.bai" -> bai
  }
  runtime {
    docker: "broadinstitute/bwa-mem:latest"
    memory: "5GB"
    stdout: "output.bam"
    cwd: "/job"
  }
}
```

Here the task is named, and has three sections: command, outputs, and runtime.

The 'command' section specifies the command line that this task runs with placeholders for parameters that the user must provide.  For example, `${type=array[uri] sep=' ' reads}` specifies that the user must provide a parameter called `reads` which is an array of URIs.

The 'outputs' section specifies which output files are important and which variables they should be stored as.

The 'runtime' section specifies any runtime needs for this task, like Docker containers, memory, CPU, standard in, standard out, etc.

Current Implementation
----------------------

`wdl2.hgr` is the grammar file for describing tasks, like the `bwa-mem` example above.

The `wdl.py` file will analyze a task and print out information about it:

```
$ python wdl.py analyze bwa-mem.wdl
Short Form:
['bwa', 'mem', <cpus>, <min_std_max_min>, <minimum_seed_length>, <reference>, <reads>]

Long Form:
(0) bwa
(1) mem
(2) [param name=cpus qualifier=? attrs={'type': string, 'prefix': '-t '}]
(3) [param name=min_std_max_min qualifier=None attrs={'type': array[int], 'prefix': '-I ', 'sep': ','}]
(4) [param name=minimum_seed_length qualifier=None attrs={'type': int, 'prefix': '-m '}]
(5) [param name=reference qualifier=None attrs={'type': uri}]
(6) [param name=reads qualifier=None attrs={'type': array[uri], 'sep': ' '}]
```

Also, providing an JSON file with mappings for the inputs, `wdl.py` will generate a command line:

```
$ python wdl.py run bwa-mem.wdl input.json
bwa mem -t 2 -I 1,2,3 -m 9 gs://bucket/object gs://bucket/read1 gs://bucket/read2
```

It also provides basic type checking... if an input specified in the JSON is incorrect:

```
$ python wdl.py run bwa-mem.wdl input.json
Parameter min_std_max_min requires type array[int], got: ['1', 2, 3]
```
