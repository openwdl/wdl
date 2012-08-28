package org.jgrapht.experimental.alg;

import java.util.*;


public interface ApproximationAlgorithm<ResultType, V>
{
    //~ Methods ----------------------------------------------------------------

    ResultType getUpperBound(Map<V, Object> optionalData);

    ResultType getLowerBound(Map<V, Object> optionalData);

    boolean isExact();
}

// End ApproximationAlgorithm.java
