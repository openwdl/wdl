import java.util.Set;
import java.util.Collection;
import java.util.Map;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Comparator;
import java.util.Collections;
import org.jgrapht.DirectedGraph;
import org.jgrapht.EdgeFactory;

class CompositeTaskGraph implements DirectedGraph<CompositeTaskVertex, CompositeTaskEdge>
{
  private Map<CompositeTaskVariable, Set<CompositeTaskScope>> scope_output_map;
  private Set<CompositeTaskVertex> verticies;
  private Set<CompositeTaskEdge> edges;
  private CompositeTaskEdgeFactory edge_factory;

  public CompositeTaskGraph(CompositeTask composite_task) {
    this.scope_output_map = new HashMap<CompositeTaskVariable, Set<CompositeTaskScope>>();
    this.edge_factory = new CompositeTaskEdgeFactory();
    this.verticies = new HashSet<CompositeTaskVertex>();
    this.edges = new HashSet<CompositeTaskEdge>();

    generate_scope_output(composite_task);
    generate_graph(composite_task);
  }

  private void generate_graph(CompositeTaskScope scope) {
    for ( CompositeTaskNode node : scope.getNodes() ) {
      if ( node instanceof CompositeTaskStep ) {
        CompositeTaskStep step = (CompositeTaskStep) node;
        addVertex(step);
        for ( CompositeTaskStepInput input : step.getInputs() ) {
          CompositeTaskVariable var = input.getVariable();
          addVertex(var);
          addEdge(var, step);

          if ( this.scope_output_map.containsKey(var) ) {
            CompositeTaskScope closest = closest_scope(step, this.scope_output_map.get(var));
            addVertex(closest);
            addEdge(closest, step);
          }
        }

        for ( CompositeTaskStepOutput output : step.getOutputs() ) {
          CompositeTaskVariable var = output.getVariable();
          addVertex(var);
          addEdge(step, var);
        }
      }

      if ( node instanceof CompositeTaskForLoop ) {
        CompositeTaskForLoop loop = (CompositeTaskForLoop) node;
        addVertex(loop);
        addVertex(loop.getCollection());
        addVertex(loop.getVariable());
        addEdge(loop.getCollection(), loop);
        addEdge(loop, loop.getVariable());
        generate_graph(loop);
      }
    }
  }

  private class ScopeDepthComparator implements Comparator<CompositeTaskScope> {
    public int compare(CompositeTaskScope s1, CompositeTaskScope s2) {
      int s1_depth, s2_depth;
      CompositeTaskScope tmp;

      for (tmp=s1.getParent(), s1_depth=0; tmp != null; tmp = tmp.getParent(), s1_depth++);
      for (tmp=s2.getParent(), s2_depth=0; tmp != null; tmp = tmp.getParent(), s2_depth++);

      if ( s1_depth < s2_depth ) return -1;
      else if ( s1_depth > s2_depth ) return 1;
      else return 0;
    }
  }

  private CompositeTaskScope closest_scope(CompositeTaskNode node, Set<CompositeTaskScope> scopes) {
    Set<CompositeTaskScope> matches = new HashSet<CompositeTaskScope>();
    for ( CompositeTaskScope scope : scopes ) {
      if ( node.getParent().contains(scope) ) {
        matches.add(scope);
      }
    }

    if (matches.size() > 0) {
      return Collections.min(matches, new ScopeDepthComparator());
    }
    return closest_scope(node.getParent(), scopes);
  }

  private void generate_scope_output(CompositeTaskScope scope) {
    for ( CompositeTaskNode node : scope.getNodes() ) {
      if ( node instanceof CompositeTaskScope ) {
        CompositeTaskScope sub_scope = (CompositeTaskScope) node;
        Set<CompositeTaskVariable> scope_outputs = get_outputs(sub_scope);
        for ( CompositeTaskVariable variable : scope_outputs ) {
          if ( !scope_output_map.containsKey(variable) ) {
            scope_output_map.put(variable, new HashSet<CompositeTaskScope>());
          }
          scope_output_map.get(variable).add(sub_scope);
          generate_scope_output(sub_scope);
        }
      }
    }
  }

  private Set<CompositeTaskVariable> get_outputs(CompositeTaskScope scope) {
    Set<CompositeTaskVariable> outputs = new HashSet<CompositeTaskVariable>();
    for ( CompositeTaskNode node : scope.getNodes() ) {
      if ( node instanceof CompositeTaskStep ) {
        CompositeTaskStep step = (CompositeTaskStep) node;
        for ( CompositeTaskStepOutput step_output : step.getOutputs() ) {
          outputs.add( step_output.getVariable() );
        }
      }

      if ( node instanceof CompositeTaskScope ) {
        outputs.addAll( get_outputs((CompositeTaskScope) node) );
      }
    }
    return outputs;
  }

  public Set<CompositeTaskEdge> getAllEdges(CompositeTaskVertex sourceVertex, CompositeTaskVertex targetVertex) {
    return this.edges;
  }

  public CompositeTaskEdge getEdge(CompositeTaskVertex sourceVertex, CompositeTaskVertex targetVertex) {
    for ( CompositeTaskEdge edge : this.edges ) {
      if ( edge.getStart().equals(sourceVertex) && edge.getEnd().equals(targetVertex) ) {
        return edge;
      }
    }
    return null;
  }

  public EdgeFactory<CompositeTaskVertex, CompositeTaskEdge> getEdgeFactory() {
    return this.edge_factory;
  }

  public CompositeTaskEdge addEdge(CompositeTaskVertex sourceVertex, CompositeTaskVertex targetVertex) {
    if ( getEdge(sourceVertex, targetVertex) != null ) {
      return null;
    }

    if ( !containsVertex(sourceVertex) || !containsVertex(targetVertex) ) {
      return null;
    }

    CompositeTaskEdge edge = this.edge_factory.createEdge(sourceVertex, targetVertex);
    this.edges.add(edge);
    return edge;
  }

  public boolean addEdge(CompositeTaskVertex sourceVertex, CompositeTaskVertex targetVertex, CompositeTaskEdge e) {return false;}

  public boolean addVertex(CompositeTaskVertex v) {
    if ( containsVertex(v) ) {
      return false;
    }

    this.verticies.add(v);
    return true;
  }

  public boolean containsEdge(CompositeTaskVertex sourceVertex, CompositeTaskVertex targetVertex) {return false;}
  public boolean containsEdge(CompositeTaskEdge e) {return false;}

  public boolean containsVertex(CompositeTaskVertex v) {
    for ( CompositeTaskVertex vertex : this.verticies ) {
      if ( v.equals(vertex) ) {
        return true;
      }
    }
    return false;
  }

  public Set<CompositeTaskEdge> edgeSet() {
    return this.edges;
  }

  public Set<CompositeTaskEdge> edgesOf(CompositeTaskVertex vertex) {return null;}
  public boolean removeAllEdges(Collection<? extends CompositeTaskEdge> edges) {return false;}
  public Set<CompositeTaskEdge> removeAllEdges(CompositeTaskVertex sourceVertex, CompositeTaskVertex targetVertex) {return null;}
  public boolean removeAllVertices(Collection<? extends CompositeTaskVertex> vertices) {return false;}
  public CompositeTaskEdge removeEdge(CompositeTaskVertex sourceVertex, CompositeTaskVertex targetVertex) {return null;}
  public boolean removeEdge(CompositeTaskEdge e) {return false;}
  public boolean removeVertex(CompositeTaskVertex v) {return false;}

  public Set<CompositeTaskVertex> vertexSet() {
    return this.verticies;
  }

  public CompositeTaskVertex getEdgeSource(CompositeTaskEdge e) {return null;}
  public CompositeTaskVertex getEdgeTarget(CompositeTaskEdge e) {return null;}
  public double getEdgeWeight(CompositeTaskEdge e) {return 1.0;}

  public int inDegreeOf(CompositeTaskVertex vertex) {return 0;}
  public Set<CompositeTaskEdge> incomingEdgesOf(CompositeTaskVertex vertex) {return null;}
  public int outDegreeOf(CompositeTaskVertex vertex) {return 0;}
  public Set<CompositeTaskEdge> outgoingEdgesOf(CompositeTaskVertex vertex) {return null;}
}
