package org.broadinstitute.compositetask;

public class CompositeTaskEdgeFactory implements EdgeFactory<CompositeTaskVertex, CompositeTaskEdge>
{
    public CompositeTaskEdge createEdge(CompositeTaskVertex sourceVertex, CompositeTaskVertex targetVertex) {
      return new CompositeTaskEdge(sourceVertex, targetVertex);
    }
}
