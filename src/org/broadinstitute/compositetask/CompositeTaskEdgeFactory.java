package org.broadinstitute.compositetask;

import org.jgrapht.EdgeFactory;

public class CompositeTaskEdgeFactory implements EdgeFactory<CompositeTaskVertex, CompositeTaskEdge>
{
    public CompositeTaskEdge createEdge(CompositeTaskVertex sourceVertex, CompositeTaskVertex targetVertex) {
      return new CompositeTaskEdge(sourceVertex, targetVertex);
    }
}
