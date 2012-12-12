composite_task CopyNumberQC {
  step LaneBlackList[version=6] {
    output: File("lane_blacklist.txt") as lane_blacklist;
  }
  for ( sample in samples ) {
    step RegionCovPerLane[version=16] {
      input: bam_file=sample.bam, sample_id=sample.id;
      output: File("${sample.id}.rcl") into rcl;
    }
    step MakeLaneList[version=11] {
      input: bam_file=sample.bam, sample_id=sample.id;
      output: File("${sample.id}.lanelist") into lanelist;
    }
  }
  step CopyNumberQC[version=25] {
    input: lanes_list=lanelist, rcl_list=rcl, lane_blacklist=lane_blacklist;
  }
}
