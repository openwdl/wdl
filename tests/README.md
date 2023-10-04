Beginning with version 1.1.1, most of the examples in the WDL specification represent test cases. They are of the form:

```html
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

  Test config:

  ```json
  {config json}
  ```
  </p>
</details>
```

All examples are written as a single WDL file.

The file name is of the form `<target>.wdl`, where `target` is the name of the workflow or task within the example that should be executed by the test framework.

* If the file name is of the form `<target>_task.wdl` then it is assumed that `target` is a task, otherwise it is assumed to be a workflow (unless the `type` configuration parameter is specified).
* If the file name is of the form `<target>_fail.wdl` then it is assumed that the test is expected to fail (unless the `fail` configuration parameter is specified).
* If the file name is of the form `<target>_fail_task.wdl` then it is both `type: "task"` and `fail: true` are assumed unless the configuration parameters specify differently.
* If the file name ends with `_resource.wdl` then it not executed as a test. Such resource WDLs are intended only to be imported by other examples.

Examples must conform to the following rules:

* Example names must be globally unique.
* The WDL code must be valid, runnable code.
* The input and output JSON must be written according to the [standard input/output specification](../SPEC.md#input-and-output-formats), i.e., with the workflow/task name as a prefix for all parameter names.

The "Example input" is only required if the example has required inputs.

The "Example output" section is used to validate the outputs of the workflow/task executed with the example inputs. If an output should not be validated, it must be listed in the `exclude_outputs` configuration parameter.

An example can import another example using its file name.

<pre>
<details>
  <summary>
  Example: example1.wdl

  ```wdl
  task example1 {
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
  import "example1.wdl"

  workflow example2 {
    call example1.mytask { ... }
  }
  ```
  </summary>
  <p>...</p>
</details>
</pre>

Each example may specify a configuration for use by the testing framework in its "Test config" section. The "Test config" section is optional - if it is missing then all configuration parameters have their default values.

The following are the configuration parameters that must be supported by all test frameworks. Test frameworks may support additional parameters, and should ignore any unrecognized parameters.

* `id`: The unique identifier of the test case. Defaults to `target` (see below).
* `type`: One of "task", "workflow", or "resource". The default is "workflow", unless the example name ends with "_task" or "_resource". Must be set explicitly if the example does not contain a workflow, if the test framework should only execute a specific task (which should be specified using the `target` parameter), or if the example should not be executed at all and only contains definitions that should be available for import by other examples (`type: "resource"`).
* `target`: The name of the workflow or task the test framework should execute. Defaults to the example name (without the ".wdl" extension). Required if the target name is different from the test name, even if the test only contains a single workflow/task.
* `priority`: The priority of the test. Must be one of the following values. Defaults to "required".
    * "required": The test framework must execute the test. If the test fails, it must be reported as an error.
    * "optional": The test framework can choose whether to execute the test. If the test fails, it must be reported as a warning.
    * "ignore": The test framework must not execute the test.
* `fail`: Whether the test is expected to fail. If `true` then a failed execution is treated as a successful test, and a successful test is treated as a failure. and a Defaults to `false`.
* `exclude_output`: A name or array of names of output parameters that should be ignored when comparing the expected and actual outputs of the test.
* `return_code`: The expected return code of the task. If a task marked `fail: true` fails but with a different return code, then the test is treated as a failure. My either be an integer or an array of integers. The value "*" indicates that any return code is allowed. Defaults to `*`.
* `dependencies`: An array of the test's dependencies. If the test framework is unable to satisfy any dependency of a "required" test, then the test is instead treated as "optional". At a minimum, the test framework should recognize dependencies based on runtime attributes. For example, `dependencies: ["cpu", "memory"]` indicates that the task has CPU and/or memory requirements that the test framework might not be reasonably expected to provide, and thus if the test fails due to lack of CPU or memory resources it should be reported as a warning rather than an error.
* `tags`: Arbitrary string or array of string tags that can be used to filter tests. For example, a time-consuming test could have `tags: "long"`, and the test framework could be executed with `--exclude-tags "long"` to exclude running such tests.

For a workflow test, `return_code` and `dependencies` configuration parameters apply to any subworkflow or task called by the workflow, to any level of nesting. For example, if a workflow has `dependencies: ["gpu"]` and it calls a task that has `gpu: true` in its runtime section, and the test framework is not executing on a system that provides a GPU, then the test is treated as optional.

The following is an example of a task test that is optional and expected to fail with a return code of `1`:

<pre>
<details>
  <summary>
  Example: optional_fail_task.wdl

  ```wdl
  task optional_fail {
    command <<<
    exit 1
    >>>
  }
  ```
  </summary>
  <p>
  ...
  
  Test config:

  ```json
  {
    "type": "task",
    "priority": "optional",
    "fail": true,
    "return_code": 1
  }
  ```
  </p>
</details>
</pre>

These naming conventions and configuration are used with the intention that an automated testing framework can extract the examples from the specification and write them into the following directory structure. It also enables the implementation to filter out task tests if it does not support executing tasks.

```
tests
|_ data
|  |_ input1.txt
|  |_ output1.txt
|_ foo.wdl
|_ bar_task.wdl
|_ ...
|_ test_config.json
```

The `test_config.json` file contains a JSON array with one element for each test, where each element is an object with the test inputs, outputs, and configuration parameters. For example:

```json
[
  {
    "id": "foo",
    "path": "foo.wdl",
    "target": "foo",
    "type": "workflow",
    "priority": "required",
    "fail": false,
    "return_code": "*",
    "exclude_output": [],
    "dependencies": [],
    "input": {
      "foo.x": 1
    },
    "output": {
      "foo.y": true
    }
  },
  {
    "id": "bar",
    ...
  }
]
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
</pre>