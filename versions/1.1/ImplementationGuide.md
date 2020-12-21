
# WDL Implementation Guide

<details>
   <summary>
   ```wdl
   this is wdl
   ```
   </summary>
   
   <p>
   ```json
   {
     "input": 1
   }
   ```
   
   ```json
   {
      "expected output": 2
   }
   </p>
</details>

## Task Execution

The execution engine is responsible for implementing all the necessary logic to execute a task's command given a set of inputs. Task execution is performed in these logical stages, although an execution engine is free to implement these stages however it wishes, including combining or reording stages, so long as the contract of each stage is upheld:

1. WDL validation: The WDL document is validated as correct, meaning that:
    * it can be parsed according to the WDL grammar rules, and
    * all expressions will evaluate to the type expected by the declaration or call input parameter.
2. Input validation: Task inputs are validated to ensure that:
    * there are no duplicates,
    * each one matches a valid input parameter name,
    * the value can be deserialized to the declared type, and
    * there are no missing required inputs.
3. Declaration ordering: Any input and private declarations that are initialized with expressions and are not overridden by user-specified values have their expressions examined to determine their dependencies. Declarations are then ordered such that they can be evaluated unambiguously. For example, in the following task, the expressions need to be evaluated in the following order: `a`, `c`, `b`.
    ```wdl
    task out_of_order {
      input {
        File a
      }
      String b = "The input file is size: ${c} GB"
      Int c = size(a, "GB")
    }
    ```
4. Declaration evaluation: Input and private declarations are evaluated in order, with the values of all previously evaluated declarations being available to evaluate the next declaration's initialization expression.
5. Runtime evaluation:
    * The runtime attributes are evaluated in the context of all input and private declaration values.
    * An appropriate runtime instance type is determined from the resource requirements. If no instance type can satisfy all the requirements, task execution is terminated with an error.
    * The task may be executed in the current environment (where the evaluation is occurring) if that is acceptable, otherwise the runtime instance is provisioned and the task exection is "moved" to the runtime instance, where moving may involve a direct transfer of state or a relaunching of the task (starting over with stage 1).
6. Input localization: Each `File` typed value - including compound values with nested `File`s - that references a non-local resource is localized, which involves:
    * Creating a local file (or file-like object, such as a `fifo`), according to the [input localization](#task-input-localization) rules.
    * Making the contents of the remote resource readable from that file, either by downloading the remote resource or by streaming its contents.
    * Replacing the value of the `File` typed declaration with the path to the local file.
7. Command instantiation:
    * The command template is evaluated in the context of all the (localized) input and private declaration values, and all expression placeholders are replaced with their (stringified) values. 
    * The instantiated command is written to local disk and made executable.
8. Container resolution:
    * If alternative container images are specified, the ["best"](SPEC.md#container) one is selected.
    * The image is "pulled" to the local environment - this may involve a literal `docker pull`, downloading a tarball and calling `docker load` or `docker import`, or some other mechanism.
9. Command execution: The instantiated command is staged within the container (along with any other necessary volumes) and executed there. All outputs should be created relative to a staged output directory. If the command exits with any return code not specified in `runtime.returnCodes`, task execution exits with an error.
10. Output ordering: Any output declarations that are initialized with expressions have their expressions examined to determine their dependencies. Declarations are then ordered such that they can be evaluated unambiguously.
11. Output evaluation: Output declarations are evaluated in order, with the values of all previously evaluated declarations being available to evaluate the next declaration's initialization expression.
12. Output delocalization: The exection engine may choose to "delocalize" outputs - i.e. to move them from the execution environment to a permanent storage location. If so, the values of any `File` typed output parameters - including compound values with nested `File`s - are updated to replace the local path with the permanent storage location.
13. Cleanup: The execution engine performs any "cleanup" tasks, such as terminating the cloud worker instance.
