task CopyNumberQCReport {
  action: command("python <libdir>run_matlab.py --with-display <libdir> fh_CopyNumberQCReport <individual.name> <tumor.rcl> <normal.rcl> <tumor.lanelist> <normal.lanelist> <lane.blacklist> <region.list> <normals.db> <tumor.seg> <normal.seg>");
  version: "1.4.2";
  description: "does CopyNumberQCReport";
  ...
}
