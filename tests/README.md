Beginning with version 1.1.1, all of the examples in the WDL specification represent test cases. They are of the form:

<pre>
<details>
  <summary>
  Example: {file name}

  ```wdl
  {WDL code}
  ```
  </summary>
  <p>
  Example input:

  ```json
  {input json}
  ```

  Example output:

  ```json
  {output json}
  ``` 
  </p>
</details>
</pre>

All examples are written as a single WDL file. The file name is of the form:

* `<workflow_name>.wdl` if the example contains a workflow.
* `<task_name>_task.wdl` if the example only contains a task.

Examples must conform to the following rules:

* Workflow and task names must be globally unique.
* Workflow names must not end with `_task`.
* The WDL code must be valid, runnable code.
* The input and output JSON must be written with the workflow name as a prefix for all parameter names.

An example can import another example using its file name.

<pre>
<details>
  <summary>
  Example: example1_task.wdl

  ```wdl
  task1 {
    ...
  }
  ```
  </summary>
  <p>...</p>
</details>
<details>
  <summary>
  Example: example2.wdl

  ```wdl
  import "example1_task.wdl"

  workflow example2 {
    ...
  }
  ```
  </summary>
  <p>...</p>
</details>
</pre>

The `meta` section of the `task` or `workflow` can be used to specify test metadata using the `test_config` attribute. This attribute accepts either a directive or an array of directives, where each directive is one of the following string values.

* Necessity: these directives are mutually exclusive, in increasing order of precedence:
    * "required": The test harness must run the test. (default)
    * "optional": The test harness may choose whether or not to run the test. If the test harness does run the test and it is unsuccessful, it should be reported as a warning rather than an error.
    * "ignore": The test harness must not run the test.
* Expected result: these directives are mutually exclusive, in increasing order of precedence:
    * "succeed": The test is expected to succeed. (default)
    * "fail": The test is expected to fail.

<pre>
<details>
  <summary>
  Example: optional_fail_task.wdl

  ```wdl
  optional_fail_task {
    ...

    meta {
      # This test is optional. If the test harness does run it, then it's expected to fail.
      test_config: ["optional", "fail"]
    }
  }
  ```
  </summary>
  <p>...</p>
</details>
</pre>

These naming conventions are used with the intention that an automated testing framework can extract the examples from the specification and write them into the following directory structure. It also enables the implementation to filter out task tests if it does not support executing tasks.

```
tests
|_ data
|  |_ input1.txt
|  |_ output1.txt
|_ foo.wdl
|_ foo_inputs.json
|_ foo_outputs.json
|_ bar_task.wdl
|_ bar_task_inputs.wdl
|_ bar_task_outputs.wdl
|_ ...
```

The `data` directory contains files that may be referenced by test cases. The data files do not need to follow any special naming conventions. Inputs to/outputs from `File`-type parameters must be given as file names/paths relative to the `data` directory.

<pre>
<details>
  <summary>
  Example: example1.wdl

  ```wdl
  workflow example1 {
    input {
      File infile
    }

    ...

    output {
      File outfile
    }
  }
  ```
  </summary>
  <p>
  Example input:

  ```json
  {
    "example1.infile": "input1.txt"
  }
  ```

  Example output:

  ```json
  {
    "example1.outfile": "output1.txt"
  }
  ``` 
  </p>
</details>