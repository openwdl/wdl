import java.util.Set;
import java.util.Collection;
import org.jgrapht.DirectedGraph;
import org.jgrapht.EdgeFactory;

class CompositeTaskGraph implements DirectedGraph<CompositeTaskVertex, CompositeTaskEdge>
{
  public Set<CompositeTaskEdge> getAllEdges(CompositeTaskVertex sourceVertex, CompositeTaskVertex targetVertex) {return null;}
  public CompositeTaskEdge getEdge(CompositeTaskVertex sourceVertex, CompositeTaskVertex targetVertex) {return null;}
  public EdgeFactory<CompositeTaskVertex, CompositeTaskEdge> getEdgeFactory() {return null;}
  public CompositeTaskEdge addEdge(CompositeTaskVertex sourceVertex, CompositeTaskVertex targetVertex) {return null;}
  public boolean addEdge(CompositeTaskVertex sourceVertex, CompositeTaskVertex targetVertex, CompositeTaskEdge e) {return false;}
  public boolean addVertex(CompositeTaskVertex v) {return false;}
  public boolean containsEdge(CompositeTaskVertex sourceVertex, CompositeTaskVertex targetVertex) {return false;}
  public boolean containsEdge(CompositeTaskEdge e) {return false;}
  public boolean containsVertex(CompositeTaskVertex v) {return false;}
  public Set<CompositeTaskEdge> edgeSet() {return null;}
  public Set<CompositeTaskEdge> edgesOf(CompositeTaskVertex vertex) {return null;}
  public boolean removeAllEdges(Collection<? extends CompositeTaskEdge> edges) {return false;}
  public Set<CompositeTaskEdge> removeAllEdges(CompositeTaskVertex sourceVertex, CompositeTaskVertex targetVertex) {return null;}
  public boolean removeAllVertices(Collection<? extends CompositeTaskVertex> vertices) {return false;}
  public CompositeTaskEdge removeEdge(CompositeTaskVertex sourceVertex, CompositeTaskVertex targetVertex) {return null;}
  public boolean removeEdge(CompositeTaskEdge e) {return false;}
  public boolean removeVertex(CompositeTaskVertex v) {return false;}
  public Set<CompositeTaskVertex> vertexSet() {return null;}
  public CompositeTaskVertex getEdgeSource(CompositeTaskEdge e) {return null;}
  public CompositeTaskVertex getEdgeTarget(CompositeTaskEdge e) {return null;}
  public double getEdgeWeight(CompositeTaskEdge e) {return 1.0;}

  public int inDegreeOf(CompositeTaskVertex vertex) {return 0;}
  public Set<CompositeTaskEdge> incomingEdgesOf(CompositeTaskVertex vertex) {return null;}
  public int outDegreeOf(CompositeTaskVertex vertex) {return 0;}
  public Set<CompositeTaskEdge> outgoingEdgesOf(CompositeTaskVertex vertex) {return null;}
}
