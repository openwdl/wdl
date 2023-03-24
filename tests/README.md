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
* `<workflow_name>_fail.wdl` or `<task_name>_task_fail.wdl` if execution of the workflow/task is expected to fail.

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