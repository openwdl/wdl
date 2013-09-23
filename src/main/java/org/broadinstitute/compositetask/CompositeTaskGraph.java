package org.broadinstitute.compositetask;

import java.util.Set;
import java.util.Collection;
import java.util.Map;
import java.util.HashMap;
import java.util.LinkedHashSet;
import java.util.Comparator;
import java.util.Collections;
import java.util.Iterator;

public class CompositeTaskGraph implements DirectedGraph<CompositeTaskVertex, CompositeTaskEdge>
{
    private Map<CompositeTaskVariable, Set<CompositeTaskScope>> scope_output_map;
    private Set<CompositeTaskVertex> verticies;
    private Set<CompositeTaskEdge> edges;
    private CompositeTaskEdgeFactory edge_factory;

    public CompositeTaskGraph(CompositeTask composite_task) {
        this.scope_output_map = new HashMap<CompositeTaskVariable, Set<CompositeTaskScope>>();
        this.edge_factory = new CompositeTaskEdgeFactory();
        this.verticies = new LinkedHashSet<CompositeTaskVertex>();
        this.edges = new LinkedHashSet<CompositeTaskEdge>();

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
                        if ( !closest.contains(step) ) {
                            addVertex(closest);
                            addEdge(closest, step);
                        }
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
        Set<CompositeTaskScope> matches = new LinkedHashSet<CompositeTaskScope>();
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
                        scope_output_map.put(variable, new LinkedHashSet<CompositeTaskScope>());
                    }
                    scope_output_map.get(variable).add(sub_scope);
                    generate_scope_output(sub_scope);
                }
            }
        }
    }

    private Set<CompositeTaskVariable> get_outputs(CompositeTaskScope scope) {
        Set<CompositeTaskVariable> outputs = new LinkedHashSet<CompositeTaskVariable>();
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

    public boolean addEdge(CompositeTaskVertex sourceVertex, CompositeTaskVertex targetVertex, CompositeTaskEdge e) {
        return false;
    }

    public boolean addVertex(CompositeTaskVertex v) {
        if ( containsVertex(v) ) {
            return false;
        }

        this.verticies.add(v);
        return true;
    }

    public boolean containsEdge(CompositeTaskVertex sourceVertex, CompositeTaskVertex targetVertex) {
        return false;
    }

    public boolean containsEdge(CompositeTaskEdge e) {
        return false;
    }

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

    public Set<CompositeTaskEdge> edgesOf(CompositeTaskVertex vertex) {
        if ( vertex == null ) {
            throw new NullPointerException("edgesOf(): null vertex");
        }

        if ( !containsVertex(vertex) ) {
            throw new IllegalArgumentException("edgesOf(): vertex is not in graph");
        }

        Set<CompositeTaskEdge> edges = new LinkedHashSet<CompositeTaskEdge>();
        for ( CompositeTaskEdge edge : this.edges ) {
            if ( edge.getStart().equals(vertex) || edge.getEnd().equals(vertex) ) {
                edges.add(edge);
            }
        }
        return edges;
    }

    public boolean removeAllEdges(Collection<? extends CompositeTaskEdge> edges) {
        if ( edges == null ) {
            throw new NullPointerException("removeAllEdges(): null edge collection");
        }

        Set<CompositeTaskEdge> removed_edges = new LinkedHashSet<CompositeTaskEdge>();
        for ( CompositeTaskEdge edge : this.edges ) {
            if (edges.contains(edge)) {
                removed_edges.add(edge);
            }
        }

        boolean changed = false;
        for ( CompositeTaskEdge edge : removed_edges ) {
            /* Interface says you need to call removeEdge for each edge you're going to remove */
            removeEdge(edge);
            changed = true;
        }

        return changed;
    }

    public Set<CompositeTaskEdge> removeAllEdges(CompositeTaskVertex sourceVertex, CompositeTaskVertex targetVertex) {
        if (!containsVertex(sourceVertex) || !containsVertex(targetVertex)) {
            return null;
        }

        Set<CompositeTaskEdge> edges = new LinkedHashSet<CompositeTaskEdge>();
        while ( true ) {
            CompositeTaskEdge removed_edge = removeEdge(sourceVertex, targetVertex);
            if ( removed_edge == null ) {
                break;
            }
            edges.add(removed_edge);
        }        
        return edges;
    }

    public boolean removeAllVertices(Collection<? extends CompositeTaskVertex> vertices) {
        if ( verticies == null ) {
            throw new NullPointerException("removeAllVerticies(): null edge collection");
        }

        Set<CompositeTaskVertex> removed_verticies = new LinkedHashSet<CompositeTaskVertex>();
        for ( CompositeTaskVertex vertex : this.verticies ) {
            if (verticies.contains(vertex)) {
                removed_verticies.add(vertex);
            }
        }

        boolean changed = false;
        for ( CompositeTaskVertex vertex : removed_verticies ) {
            /* Interface says you need to call removeVertex for each edge you're going to remove */
            removeVertex(vertex);
            changed = true;
        }

        return changed;
    }

    public CompositeTaskEdge removeEdge(CompositeTaskVertex sourceVertex, CompositeTaskVertex targetVertex) {
        for ( Iterator<CompositeTaskEdge> i = this.edges.iterator(); i.hasNext(); ) {
            CompositeTaskEdge edge = i.next();
            if ( edge.getStart().equals(sourceVertex) && edge.getEnd().equals(targetVertex) ) {
                removeEdge(edge);
                return edge;
            }
        }

        return null;
    }

    public boolean removeEdge(CompositeTaskEdge e) {
        if ( e == null ) {
            return false;
        }

        for ( Iterator<CompositeTaskEdge> i = this.edges.iterator(); i.hasNext(); ) {
            CompositeTaskEdge edge = i.next();
            if ( edge.equals(edge) ) {
                removeEdge(edge);
                return true;
            }
        }

        return false;
    }

    public boolean removeVertex(CompositeTaskVertex v) {
        if ( !containsVertex(v) ) {
            return false;
        }

        

        return false;
    }

    public Set<CompositeTaskVertex> vertexSet() {
        return this.verticies;
    }

    public CompositeTaskVertex getEdgeSource(CompositeTaskEdge e) {
        return e.getStart();
    }

    public CompositeTaskVertex getEdgeTarget(CompositeTaskEdge e) {
        return e.getEnd();
    }

    public double getEdgeWeight(CompositeTaskEdge e) {
        return 1.0;
    }

    public int inDegreeOf(CompositeTaskVertex vertex) {
        int degree = 0;
        for ( CompositeTaskEdge edge : this.edges ) {
            if ( edge.getEnd().equals(vertex) ) {
                degree += 1;
            }
        }
        return degree;
    }

    public Set<CompositeTaskEdge> incomingEdgesOf(CompositeTaskVertex vertex) {
        Set<CompositeTaskEdge> incoming = new LinkedHashSet<CompositeTaskEdge>();
        for ( CompositeTaskEdge edge : this.edges ) {
            if ( edge.getEnd().equals(vertex) ) {
                incoming.add(edge);
            }
        }
        return incoming;
    }

    public int outDegreeOf(CompositeTaskVertex vertex) {
        int degree = 0;
        for ( CompositeTaskEdge edge : this.edges ) {
            if ( edge.getStart().equals(vertex) ) {
                degree += 1;
            }
        }
        return degree;
    }

    public Set<CompositeTaskEdge> outgoingEdgesOf(CompositeTaskVertex vertex) {
        Set<CompositeTaskEdge> outgoing = new LinkedHashSet<CompositeTaskEdge>();
        for ( CompositeTaskEdge edge : this.edges ) {
            if ( edge.getStart().equals(vertex) ) {
                outgoing.add(edge);
            }
        }
        return outgoing;
    }
}
