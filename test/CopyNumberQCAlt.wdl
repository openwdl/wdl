composite_task CopyNumberQC {
  step LaneBlackList: (lane_blacklist) = LaneBlackList();

  for ( sample in samples ) {
    step MakeLaneList: (sample.lanelist) = MakeLaneList(sample.bam, sample.id, sample.regions);
    step RegionCovPerLane: (sample.rcl) = RegionCovPerLane(sample.bam, sample.id, sample.regions);
  }

  step CopyNumberQc: CopyNumberQCReport(samples.lanelist, samples.rcl, region_list, normals_db, tumor_seg, normal_seg, lane_blacklist);
}

task MakeLaneList(File input_bam, String sample_id) {
  output: File("lanelist_${sample_id}.txt");
  action: task("MakeLaneList", version=11);
}

task RegionCovPerLane(File input_bam, String sample_id, String region_list) {
  output: File("sample_${sample_id}.rcl");
  action: task("RegionCovPerLane", version=16);
}

task LaneBackList() {
  output: File("LaneBlackList.txt");
  action: task("LaneBlackList", version=6);
}

task CopyNumberQcReport(ListFile lanelist, ListFile rcl, String individual_name, FileList region_list, FileList normals_db, File tumor_seg, File normal_seg, File lane_blacklist) {
  action: task("CopyNumberQCReport", version=25);
}
