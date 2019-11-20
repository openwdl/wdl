version development

import "other-workflow.wdl" as other

task foo {
	input {
		String inp
	}

	String otherMessage = if inp == "even" then inp else "odd"

	command <<<
		echo ~{inp} ~{otherMessage}
	>>>

	runtime {
		container: "ubuntu"
		cpu: 1
		memory: "3GB"
	}


	hints {
		openwdl: {
			foo: "bar"
		}

	}
	output {
		String out = read_string(stdout())
	}
}


workflow workflow_with_task_def_and_call {

  input {
    String inp
  }

  Array[Int] scatters = [1,2,3,4,5,6,7,8,10]

  scatter ( i in scatters) {
	  call foo as bar {
		input:
			inp = inp
	  }

	  if ( i % 2 == 0 ) {
	  	call foo as biz {
	  		input:
	  			inp = "Even"
	  	}

	  	call other.that_workflow as baz {
	  		input:
	  			test = i

	  	}
	  }
  }

  output {
  	String out = bar.out
  }
}