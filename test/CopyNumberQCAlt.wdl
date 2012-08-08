composite_task CopyNumberQC {
  step {
    task: LaneBlackList[version=6]
  }

  for ( sample in samples ) {
    step MakeLaneList_v11 {
      task: MakeLaneList[version=11];
      input: sample.bam, sample.id, sample.regions;
      output: sample.lanelist;
    }

    step RegionCovPerLane_v16 {
      task: RegionCovPerLane[version=16];
      input: sample.bam, sample.id, sample.regions;
      output: sample.rcl;
    }
  }

  step CopyNumberQC_v25 {
    task: CopyNumberQCReport[version=25];
    input: samples.lanelist, samples.rcl, region_list, normals_db, tumor_seg, normal_seg, lane_blacklist;
  }
}
