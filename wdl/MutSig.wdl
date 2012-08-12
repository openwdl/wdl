/* inputs:
 *   1) MutSigPreprocess.{individual_set_id, maf1, maf2, maf3, maf4, maflabel1, maflabel2, maflabel3, maflabel4, wig1, wig2, wig3, wig4, build, context65_dir, build_dir, num_categories, target_list, paramfile}
 *   2) ProcessCoverageForMutSig has no variables.  All inputs come from prior step.
 *   3) MutSigRun.{individual_set_id, gene_list, build, geneset_file, cosmic_file, refseq_file, build_dir, param_file, jobcount}
 */

composite_task MutSig {

  step MutSigPreprocess[version=86] {
    output: File("coverage.prepare.txt") as coverage_prepare_file,
            File("patients.txt") as patient_list,
            File("${individual_set_id}.maf") as mutation_list,
            File("mutation_preprocessing_report.txt") as mutation_preprocessing_report;
  }

  step ProcessCoverageForMutSig[version=75] {
    input: coverage=coverage_prepare_file, patients=patient_list, mutations=mutation_list;
    output: File("coverage.mat") as coverage_file,
            File("mutcategs.txt") as category_file;
  }

  step MutSigRun[version=157] as MutSig {
    input: mutation_list=mutation_list, coverage_file=coverage_file, patients=patient_list, category_file=category_file, mutation_preprocessing_report=foobar;
    output: File("bargraphs.png") as graphs;
  }

}
