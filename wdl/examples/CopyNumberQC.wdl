composite_task CopyNumberQC {
  step LaneBlackList[version=6] {
    output: File("lane_blacklist.txt") as lane_blacklist;
  }

  for ( sample in samples ) {
    step MakeLaneList[version=11] as foobar {
      input: bam=sample.bam, id=sample.id, regions=sample.regions;
      output: File("${sample.id}.lanelist") as sample.lanelist;
    }

    step RegionCovPerLane[version=16] {
      input: bam=sample.bam, id=sample.id, regions=sample.regions;
      output: File("${sample.id}.rcl") as sample.rcl;
    }
  }

  step CopyNumberQC[version=25] {
    input: lanelist=samples.lanelist, rcl=samples.rcl, lane_blacklist=lane_blacklist;
  }
}
