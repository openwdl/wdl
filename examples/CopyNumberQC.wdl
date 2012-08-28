composite_task CopyNumberQC {
  step LaneBlackList[version=6] {
    output: File("lane_blacklist.txt") as lane_blacklist;
  }

  for ( sample in samples ) {
    step MakeLaneList[version=11] as foobar {
      input: bam=sample.bam, id=sample.id, regions=sample.regions;
      output: File("${sample.id}.lanelist") as lanelist;
    }

    step RegionCovPerLane[version=16] {
      input: bam=sample.bam, id=sample.id, regions=sample.regions;
      output: File("${sample.id}.rcl") as rcl;
    }
  }

  step CopyNumberQC[version=25] {
    input: lanelist=lanelist, rcl=rcl, lane_blacklist=lane_blacklist;
  }
}
