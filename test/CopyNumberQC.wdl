composite_task CopyNumberQC {
  step MakeLaneList_Normal: (normal_rcl) = MakeLaneList( File("normal.bam"), sample_id );
  step MakeLaneList_Tumor: (tumor_rcl) = MakeLaneList( File("tumor.bam"), sample_id );
  step RegionCovPerLane_Normal: (normal_rcl) = RegionCovPerLane(File("normal.bam"), sample_id, region_list);
  step RegionCovPerLane_Tumor: (tumor_rcl) = RegionCovPerLane(File("sample.bam"), sample_id, region_list);
  step LaneBlackList: (lane_blacklist) = LaneBlackList()
  step CopyNumberQC_${sample.id}: (analysis_file, str) = CopyNumberQCReport(tumor_rcl, normal_rcl, individual_name, tumor_lanelist, normal_lanelist, region_list, normals_db, tumor_seg, normal_seg, lane_blacklist);
}

step MakeLaneList(File input_bam, String sample_id) {
  output: File("lanelist.txt");
  action: task("MakeLaneList", version=11);
}

step RegionCovPerLane(File input_bam, String sample_id, String region_list) {
  output: File("");
  action: task("RegionCovPerLane", version=16);
}

step LaneBackList() {
  output: File("LaneBlackList.txt");
  action: command("python ${libdir}script.py ${normal_bam} ${tumor_bam}");
}

step CopyNumberQcReport(File tumor_rcl, File normal_rcl, String individual_name, File tumor_lanelist, File normal_lanelist, region_list, normals_db, tumor_seg, normal_seg, lane_blacklist) {
  output: File("dir/analysis.txt"), "static string";
  action: command("python ${libdir}script.py ${normal_bam} ${tumor_bam}");
}

step CopyNumberQcReport(ListFile lanelist, ListFile rcl) {
  output: File("dir/analysis.txt"), "static string";
  action: command("python ${libdir}script.py ${normal_bam} ${tumor_bam}");
}
