package org.broadinstitute.compositetask;

import java.util.ArrayList;
import java.util.List;

import org.broadinstitute.parser.Utility;

public class CompositeTaskSourceCodeFormatter {
  private CompositeTaskColorizer colorizer;

  CompositeTaskSourceCodeFormatter(CompositeTaskColorizer colorizer) {
    this.colorizer = colorizer;
  }

  CompositeTaskSourceCodeFormatter() {
    this(new NullColorizer());
  }

  public String format(CompositeTask ctask) {
    return format(ctask, 0);
  }

  private String format(CompositeTaskNode node, int indent) {
    StringBuilder builder = new StringBuilder();
    String indent_str = Utility.getIndentString(indent);
    if ( node instanceof CompositeTask ) {
      CompositeTask ctask = (CompositeTask) node;
      builder.append(indent_str + this.colorizer.keyword("composite_task") + " " + ctask.getName() + " {\n");
      for ( CompositeTaskNode sub_node : ctask.getNodes() ) {
        builder.append( indent_str );
        builder.append( format(sub_node, indent + 2) );
      }
      builder.append(indent_str + "}\n");
    } else if ( node instanceof CompositeTaskForLoop ) {
      CompositeTaskForLoop loop = (CompositeTaskForLoop) node;
      builder.append( indent_str + this.colorizer.keyword("for") + " ( " + this.colorizer.variable(variable_to_string(loop.getVariable())) + " " + this.colorizer.keyword("in") + " " + this.colorizer.variable(variable_to_string(loop.getCollection())) + " ) {\n" );
      for ( CompositeTaskNode sub_node : loop.getNodes() ) {
        builder.append( indent_str );
        builder.append( format(sub_node, indent + 2) );
      }
      builder.append( indent_str + "}\n" );
    } else if ( node instanceof CompositeTaskStep ) {
      CompositeTaskStep step = (CompositeTaskStep) node;
      CompositeTaskSubTask task = step.getTask();
      String rename = "";
      if ( !step.getName().equals(task.getTaskName()) ) {
        rename = " " + this.colorizer.keyword("as") + " " + step.getName();
      }
      builder.append( "  " + this.colorizer.keyword("step") + " " + this.colorizer.task(task.getTaskName()) + "[version=" + task.getVersion() + "]" + rename + " {\n" );

      if ( step.getInputs().size() > 0 ) {
        List<String> parameters = new ArrayList<String>();
        for ( CompositeTaskStepInput input : step.getInputs() ) {
          parameters.add(input.getParameter() + "=" + this.colorizer.variable(variable_to_string(input.getVariable())));
        }

        builder.append(indent_str  + "  " + this.colorizer.keyword("input") + ": " + Utility.join(parameters, ", ") + ";\n");
      }

      if ( step.getOutputs().size() > 0 ) {
        List<String> outputs = new ArrayList<String>();
        for ( CompositeTaskStepOutput output : step.getOutputs() ) {
          outputs.add(output.getType() + "(" + this.colorizer.string(output.getPath()) + ") " + this.colorizer.keyword("as") + " " + this.colorizer.variable(variable_to_string(output.getVariable())));
        }

        builder.append(indent_str + "  " + this.colorizer.keyword("output") + ": " + Utility.join(outputs, ", ") + ";\n");
      }

      builder.append( indent_str + "}\n" );
    }
    return builder.toString();
  }

  private String variable_to_string(CompositeTaskVariable var) {
    if ( var.getMember() != null ) {
      return var.getName() + "." + var.getMember();
    }
    else {
      return var.getName();
    }
  } 
}
