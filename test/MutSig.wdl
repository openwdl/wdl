composite_task MutSig {

  step MutSigPreprocess {
    task: MutSigPreprocess[version=86];
    input: individual_set_id, maf1, maf2, maf3, maf4, maflabel1, maflabel2, maflabel3, maflabel4, wig1, wig2, wig3, wig4, build, context65_dir, build_dir, num_categories, target_list, paramfile;
    output: File("coverage.prepare.txt") as coverage_prepare_file,
            File("patients.txt") as patient_list
            File("${individual_set_id}.maf") as mutation_list,
            File("mutation_preprocessing_report.txt") as mutation_preprocessing_report;
  }

  step ProcessCoverageForMutSig {
    task: ProcessCoverageForMutSig[version=75];
    input: coverage_prepare_file, patient_list, mutation_list;
    output: File("coverage.mat") as coverage_file,
            File("mutcategs.txt") as category_file;
  }

  step MutSigRun {
    task: MutSigRun[version=157]
    input: individual_set_id, mutation_list, coverage_file, patient_list, category_file, gene_list, build, geneset_file, cosmic_file, refseq_file, build_dir, param_file, mutation_preprocessing_report, jobcount;
    output: File("bargraphs.png") as graphs;
  }

  output {
    graphs
  }

}
