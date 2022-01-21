Beginning with version 1.1, all of the examples in the WDL specification represent test cases. They are of the form:

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

This naming convention enables the test harness to know the prefix to use for inputs and outputs. It also enables the implementation to filter out task tests if it does not support executing tasks.

The WDL code must be valid, runnable code. Note that an example can import another example using its file name.

The input and output JSON must be written with the workflow name as a prefix for all parameter names. Inputs to/outputs from `File`-type parameters must be given as file names/paths relative to the `data` directory.
