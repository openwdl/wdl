## Copyright Broad Institute, 2017
## 
## This WDL workflow runs GATK4 Mutect 2 on a single tumor-normal pair or on a single tumor sample, 
## and performs additional filtering and functional annotation tasks. 
##
## Main requirements/expectations :
## - One analysis-ready BAM file (and its index) for each sample 
##
## Description of inputs :
##
## ** Runtime ** (requires Docker; to use on-premises without Docker, change gatk4_jar from String to File)
## gatk4_jar: path to the java jar file containing GATK 4 (beta.2 or later) in the specified docker
## picard_jar: path to retrieve a Picard jar (will be replaced by a docker image in a future version)
## m2_docker, oncotator_docker: docker images to use for GATK4 Mutect2 and for Oncotator
## preemptible_attempts: how many preemptions to tolerate before switching to a non-preemptible machine (on Google)
##
## ** Workflow options **
## intervals: genomic intervals (will be used for scatter)
## scatter_count: number of parallel jobs to generate when scattering over intervals
## artifact_modes: filtering options
## m2_extra_args, m2_extra_filtering_args: additional arguments for Mutect2 calling and filtering (optional)
## is_run_orientation_bias_filter: if true, run the orientation bias filter post-processing step
## is_run_oncotator: if true, annotate the M2 VCFs using oncotator (to produce a TCGA MAF)
##
## ** Primary inputs **
## ref_fasta, ref_fasta_index, ref_dict: reference genome, index, and dictionary
## tumor_bam, tumor_bam_index, and tumor_sample_name: BAM, index and sample name for the tumor sample (sample name used for output naming)
## normal_bam, normal_bam_index, and normal_sample_name: BAM, index and sample name for the normal sample (optional if running tumor-only)
##
## ** Primary resources ** (optional but strongly recommended)
## pon, pon_index: optional panel of normals in VCF format containing probable technical artifacts (false positves)
## gnomad, gnomad_index: optional database of known germline variants (see http://gnomad.broadinstitute.org/downloads)
## variants_for_contamination, variants_for_contamination_index: VCF of common variants with allele frequencies fo calculating contamination
##
## ** Secondary resources ** (for optional tasks)
## onco_ds_tar_gz, default_config_file: Oncotator datasources and config file
## sequencing_center, sequence_source: metadata for Oncotator
##
## Outputs :
## - One VCF file and its index with primary filtering applied; secondary filtering and functional annotation if requested.
##
## Cromwell version support 
## - Successfully tested on v27
##
## LICENSING : 
## This script is released under the WDL source code license (BSD-3) (see LICENSE in 
## https://github.com/broadinstitute/wdl). Note however that the programs it calls may 
## be subject to different licenses. Users are responsible for checking that they are
## authorized to run all programs before running this script. Please see the docker 
## pages at https://hub.docker.com/r/broadinstitute/* for detailed licensing information 
## pertaining to the included programs.

workflow Mutect2 {
  # Runtime
  String gatk4_jar
  File picard_jar
  String m2_docker
  String oncotator_docker
  Int preemptible_attempts
  # Workflow options
  Int scatter_count
  File? intervals  
  Array[String] artifact_modes
  String? m2_extra_args
  String? m2_extra_filtering_args
  Boolean is_run_orientation_bias_filter
  Boolean is_run_oncotator
  # Primary inputs 
  File ref_fasta
  File ref_fasta_index
  File ref_dict
  File tumor_bam
  File tumor_bam_index
  String tumor_sample_name
  File? normal_bam
  File? normal_bam_index
  String? normal_sample_name
  # Primary resources
  File? pon
  File? pon_index
  File? gnomad
  File? gnomad_index
  File? variants_for_contamination
  File? variants_for_contamination_index
  # Secondary resources / inputs
  File? onco_ds_tar_gz
  File? default_config_file
  String? sequencing_center
  String? sequence_source
  
  # This is a workaround for some missing functionality to name outputs
  call ProcessOptionalArguments {
    input:
      tumor_sample_name = tumor_sample_name,
      normal_bam = normal_bam,
      normal_sample_name = normal_sample_name,
      preemptible_attempts = preemptible_attempts,
      m2_docker=m2_docker
  }

  # Create lists of intervals for scattering
  call SplitIntervals {
    input:
      gatk4_jar = gatk4_jar,
      scatter_count = scatter_count,
      intervals = intervals,
      ref_fasta = ref_fasta,
      ref_fasta_index = ref_fasta_index,
      ref_dict = ref_dict,
      preemptible_attempts = preemptible_attempts,
      m2_docker = m2_docker

  }

  # Scatter M2 calling across intervals
  scatter (subintervals in SplitIntervals.interval_files ) {
    call M2 {
      input: 
        gatk4_jar = gatk4_jar,
        intervals = subintervals,
        ref_fasta = ref_fasta,
        ref_fasta_index = ref_fasta_index,
        ref_dict = ref_dict,
        tumor_bam = tumor_bam,
        tumor_bam_index = tumor_bam_index,
        tumor_sample_name = tumor_sample_name,
        normal_bam = normal_bam,
        normal_bam_index = normal_bam_index,
        normal_sample_name = normal_sample_name,
        pon = pon,
        pon_index = pon_index,
        gnomad = gnomad,
        gnomad_index = gnomad_index,
        output_vcf_name = ProcessOptionalArguments.output_name,
        preemptible_attempts = preemptible_attempts,
        m2_docker = m2_docker,
        m2_extra_args = m2_extra_args
    }
  }

  # Merge results from scattered calling
  call MergeVCFs {
    input:
      gatk4_jar = gatk4_jar,
      input_vcfs = M2.output_vcf,
      output_vcf_name = ProcessOptionalArguments.output_name,
      preemptible_attempts = preemptible_attempts,
      m2_docker = m2_docker
  }

  # Optional: collect orientation bias metrics
  if (is_run_orientation_bias_filter) {
      call CollectSequencingArtifactMetrics {
        input:
            preemptible_attempts = preemptible_attempts,
            m2_docker = m2_docker,
            tumor_bam = tumor_bam,
            tumor_bam_index = tumor_bam_index,
            ref_fasta = ref_fasta,
            ref_fasta_index = ref_fasta_index,
            picard_jar = picard_jar
      }
  }

  # Filter raw somatic calls
  call Filter {
    input:
      gatk4_jar = gatk4_jar,
      unfiltered_vcf = MergeVCFs.output_vcf,
      output_vcf_name = ProcessOptionalArguments.output_name,
      intervals = intervals,
      m2_docker = m2_docker,
      preemptible_attempts = preemptible_attempts,
      pre_adapter_metrics = CollectSequencingArtifactMetrics.pre_adapter_metrics,
      tumor_bam = tumor_bam,
      tumor_bam_index = tumor_bam_index,
      ref_fasta = ref_fasta,
      ref_fasta_index = ref_fasta_index,
      artifact_modes = artifact_modes,
      variants_for_contamination = variants_for_contamination,
      variants_for_contamination_index = variants_for_contamination_index,
      m2_extra_filtering_args = m2_extra_filtering_args
  }

  # Optional: run functional annotation with Oncotator
  if (is_run_oncotator) {
        call oncotate_m2 {
            input:
                m2_vcf = Filter.filtered_vcf,
                entity_id = tumor_sample_name,
                preemptible_attempts = preemptible_attempts,
                oncotator_docker = oncotator_docker,
                onco_ds_tar_gz = onco_ds_tar_gz,
                sequencing_center = sequencing_center,
                sequence_source = sequence_source,
                default_config_file = default_config_file
        }
  }

  # Final outputs of the workflow
  output {
        File unfiltered_vcf = MergeVCFs.output_vcf
        File unfiltered_vcf_index = MergeVCFs.output_vcf_index
        File filtered_vcf = Filter.filtered_vcf
        File filtered_vcf_index = Filter.filtered_vcf_index

        # select_first() fails if nothing resolves to non-null, so putting in "null" for now.
        File? oncotated_m2_maf = select_first([oncotate_m2.oncotated_m2_maf, "null"])
        File? preadapter_detail_metrics = select_first([CollectSequencingArtifactMetrics.pre_adapter_metrics, "null"])
  }
}

task M2 {
  String gatk4_jar
  File? intervals
  File ref_fasta
  File ref_fasta_index
  File ref_dict
  File tumor_bam
  File tumor_bam_index
  String tumor_sample_name
  File? normal_bam
  File? normal_bam_index
  String? normal_sample_name
  File? pon
  File? pon_index
  File? gnomad
  File? gnomad_index
  String output_vcf_name
  String m2_docker
  Int preemptible_attempts
  String? m2_extra_args

  command <<<
  if [[ "_${normal_bam}" == *.bam ]]; then
      samtools view -H ${normal_bam} | sed -n "/SM:/{s/.*SM:\\(\\)/\\1/; s/\\t.*//p ;q};" > normal_name.txt
      normal_command_line="-I ${normal_bam} -normal `cat normal_name.txt`"
  fi

  samtools view -H ${tumor_bam} | sed -n "/SM:/{s/.*SM:\\(\\)/\\1/; s/\\t.*//p ;q};" > tumor_name.txt

  java -Xmx4g -jar ${gatk4_jar} Mutect2 \
    -R ${ref_fasta} \
    -I ${tumor_bam} \
    -tumor `cat tumor_name.txt` \
    $normal_command_line \
    ${"--germline_resource " + gnomad} \
    ${"--normal_panel " + pon} \
    ${"-L " + intervals} \
    -O "${output_vcf_name}.vcf" \
    ${m2_extra_args}
  >>>

  runtime {
      docker: "${m2_docker}"
      memory: "5 GB"
      disks: "local-disk " + 500 + " HDD"
      preemptible: "${preemptible_attempts}"
  }

  output {
    File output_vcf = "${output_vcf_name}.vcf"
  }
}

# HACK: cromwell can't handle the optional normal sample name in output or input --
# string interpolation of optionals only works inside a command block
# thus we use this hack
task ProcessOptionalArguments {
  String tumor_sample_name
  String? normal_bam
  String? normal_sample_name
  Int preemptible_attempts
  String m2_docker

  command {
      if [[ "_${normal_bam}" == *.bam ]]; then
        echo "${tumor_sample_name}-vs-${normal_sample_name}" > name.tmp
      else
        echo "${tumor_sample_name}-tumor-only" > name.tmp
      fi
  }

  runtime {
    docker: "broadinstitute/genomes-in-the-cloud:2.2.4-1469632282"
    memory: "2 GB"
    disks: "local-disk " + 10 + " HDD"
    preemptible: "${preemptible_attempts}"
  }

  output {
      String output_name = read_string("name.tmp")
  }
}

task MergeVCFs {
  String gatk4_jar
  Array[File] input_vcfs
  String output_vcf_name
  Int preemptible_attempts
  String m2_docker

  # using MergeVcfs instead of GatherVcfs so we can create indices
  # WARNING 2015-10-28 15:01:48 GatherVcfs  Index creation not currently supported when gathering block compressed VCFs.
  command {
    java -Xmx2g -jar ${gatk4_jar} MergeVcfs -I ${sep=' -I ' input_vcfs} -O ${output_vcf_name}.vcf
  }

  runtime {
    docker: "${m2_docker}"
    memory: "3 GB"
    disks: "local-disk " + 300 + " HDD"
    preemptible: "${preemptible_attempts}"
  }

  output {
    File output_vcf = "${output_vcf_name}.vcf"
    File output_vcf_index = "${output_vcf_name}.vcf.idx"
  }
}

task CollectSequencingArtifactMetrics {
  Int preemptible_attempts
  String m2_docker
  File tumor_bam
  File tumor_bam_index
  File ref_fasta
  File ref_fasta_index
  File picard_jar

  command {
        java -Xmx4G -jar ${picard_jar} CollectSequencingArtifactMetrics I=${tumor_bam} O="metrics" R=${ref_fasta}

        # Convert to GATK format
        sed -r "s/picard\.analysis\.artifacts\.SequencingArtifactMetrics\\\$PreAdapterDetailMetrics/org\.broadinstitute\.hellbender\.tools\.picard\.analysis\.artifacts\.SequencingArtifactMetrics\$PreAdapterDetailMetrics/g" \
            "metrics.pre_adapter_detail_metrics" > "gatk.pre_adapter_detail_metrics"
  }

  runtime {
    docker: "${m2_docker}"
    memory: "5 GB"
    disks: "local-disk " + 500 + " HDD"
    preemptible: "${preemptible_attempts}"
  }

  output {
    File pre_adapter_metrics = "gatk.pre_adapter_detail_metrics"
  }
}

task Filter {
  String gatk4_jar
  File unfiltered_vcf
  String output_vcf_name
  File? intervals
  Int preemptible_attempts
  String m2_docker
  File? pre_adapter_metrics
  File? tumor_bam
  File? tumor_bam_index
  File? ref_fasta
  File? ref_fasta_index
  Array[String]? artifact_modes
  File? variants_for_contamination
  File? variants_for_contamination_index
  String? m2_extra_filtering_args

  command {
    set -e

    if [[ "${variants_for_contamination}" == *.vcf ]]; then
        java -Xmx4g -jar ${gatk4_jar} GetPileupSummaries -I ${tumor_bam} ${"-L " + intervals} -V ${variants_for_contamination} -O pileups.table
        java -Xmx4g -jar ${gatk4_jar} CalculateContamination -I pileups.table -O contamination.table
        contamination_cmd="-contaminationTable contamination.table"
    fi

    java -Xmx4g -jar ${gatk4_jar} FilterMutectCalls -V ${unfiltered_vcf} \
            -O filtered.vcf $contamination_cmd \
            ${m2_extra_filtering_args}

    # FilterByOrientationBias must come after all of the other filtering.
    if [[ ! -z "${pre_adapter_metrics}" ]]; then
        java -jar ${gatk4_jar} FilterByOrientationBias -A ${sep=" -A " artifact_modes} \
            -V filtered.vcf -P ${pre_adapter_metrics} --output "${output_vcf_name}-filtered.vcf"
    else
        mv filtered.vcf "${output_vcf_name}-filtered.vcf"
        mv filtered.vcf.idx "${output_vcf_name}-filtered.vcf.idx"
    fi

  }

  runtime {
    docker: "${m2_docker}"
    memory: "5 GB"
    disks: "local-disk " + 500 + " HDD"
    preemptible: "${preemptible_attempts}"
  }

  output {
    File filtered_vcf = "${output_vcf_name}-filtered.vcf"
    File filtered_vcf_index = "${output_vcf_name}-filtered.vcf.idx"
  }
}

task SplitIntervals {
  String gatk4_jar
  Int scatter_count
  File? intervals
  File ref_fasta
  File ref_fasta_index
  File ref_dict
  Int preemptible_attempts
  String m2_docker

  command {
    # fail if *any* command below (not just the last) doesn't return 0, in particular if GATK SplitIntervals fails
    set -e
    mkdir interval-files
    java -jar ${gatk4_jar} SplitIntervals -R ${ref_fasta} ${"-L " + intervals} -scatter ${scatter_count} -O interval-files
    cp interval-files/*.intervals .
  }

  runtime {
    docker: "${m2_docker}"
    memory: "3 GB"
    disks: "local-disk " + 100 + " HDD"
    preemptible: "${preemptible_attempts}"
  }

  output {
    Array[File] interval_files = glob("*.intervals")
  }
}

task oncotate_m2 {
    File m2_vcf
    String entity_id
    Int preemptible_attempts
    String oncotator_docker
    File? onco_ds_tar_gz
    String? sequencing_center
    String? sequence_source
    File? default_config_file
    command <<<

        # fail if *any* command below (not just the last) doesn't return 0
        set -e

        mkdir onco_dbdir
        tar zxvf ${onco_ds_tar_gz} -C onco_dbdir --strip-components 1

        /root/oncotator_venv/bin/oncotator --db-dir onco_dbdir/ -c $HOME/tx_exact_uniprot_matches.AKT1_CRLF2_FGFR1.txt  \
            -v ${m2_vcf} ${entity_id}.maf.annotated hg19 -i VCF -o TCGAMAF --skip-no-alt --infer-onps --collapse-number-annotations --log_name oncotator.log \
            -a Center:${default="Unknown" sequencing_center} \
            -a source:${default="Unknown" sequence_source} \
            ${"--default_config " + default_config_file}
    >>>

    runtime {
        docker: "${oncotator_docker}"
        memory: "3 GB"
        bootDiskSizeGb: 12
        disks: "local-disk 100 HDD"
        preemptible: "${preemptible_attempts}"
    }

    output {
        File oncotated_m2_maf="${entity_id}.maf.annotated"
    }
}