## Copyright Broad Institute, 2017
## 
## This WDL pipeline implements data pre-processing according to the GATK Best Practices 
## (June 2016) for SNP and Indel discovery. Example JSONs are provided for the WGS 
## use case but the workflow can be applied to Exomes and Targeted Panels.
##
## Requirements/expectations :
## - Pair-end sequencing data in unmapped BAM (uBAM) format
## - One or more read groups, one per uBAM file, all belonging to a single sample (SM)
## - Input uBAM files must additionally comply with the following requirements:
## - - filenames all have the same suffix (we use ".unmapped.bam")
## - - files must pass validation by ValidateSamFile 
## - - reads are provided in query-sorted order
## - - all reads must have an RG tag
##
## Output :
## - A clean BAM file and its index, suitable for variant discovery analyses.
##
## Cromwell version support 
## - Successfully tested on v25
## - Does not work on versions < v23 due to output syntax
##
## Runtime parameters are optimized for Broad's Google Cloud Platform implementation. 
## For program versions, see docker containers. 
##
## LICENSING : 
## This script is released under the WDL source code license (BSD-3) (see LICENSE in 
## https://github.com/broadinstitute/wdl). Note however that the programs it calls may 
## be subject to different licenses. Users are responsible for checking that they are
## authorized to run all programs before running this script. Please see the docker 
## page at https://hub.docker.com/r/broadinstitute/genomes-in-the-cloud/ for detailed
## licensing information pertaining to the included programs.

# TASK DEFINITIONS

# Get version of BWA
task GetBwaVersion {
  command {
    # Not setting "set -o pipefail" here because /bwa has a rc=1 and we don't want to allow rc=1 to succeed 
    # because the sed may also fail with that error and that is something we actually want to fail on.
    /usr/gitc/bwa 2>&1 | \
    grep -e '^Version' | \
    sed 's/Version: //'
  }
  runtime {
    docker: "broadinstitute/genomes-in-the-cloud:2.2.5-1486412288"
    memory: "1 GB"
  }
  output {
    String version = read_string(stdout())
  }
}

# Read unmapped BAM, convert on-the-fly to FASTQ and stream to BWA MEM for alignment
task SamToFastqAndBwaMem {
  File input_bam
  String bwa_commandline
  String output_bam_basename
  File ref_fasta
  File ref_fasta_index
  File ref_dict

  # This is the .alt file from bwa-kit (https://github.com/lh3/bwa/tree/master/bwakit), 
  # listing the reference contigs that are "alternative". Leave blank in JSON for legacy 
  # references such as b37 and hg19.
  File? ref_alt

  File ref_amb
  File ref_ann
  File ref_bwt
  File ref_pac
  File ref_sa

  Int disk_size

  command <<<
    set -o pipefail
    set -e

    # set the bash variable needed for the command-line
    bash_ref_fasta=${ref_fasta}

  	java -Xmx3000m -jar /usr/gitc/picard.jar \
    	SamToFastq \
    	INPUT=${input_bam} \
    	FASTQ=/dev/stdout \
    	INTERLEAVE=true \
    	NON_PF=true | \
  	/usr/gitc/${bwa_commandline} /dev/stdin -  2> >(tee ${output_bam_basename}.bwa.stderr.log >&2) | \
  	samtools view -1 - > ${output_bam_basename}.bam

  >>>
  runtime {
    docker: "broadinstitute/genomes-in-the-cloud:2.2.5-1486412288"
    memory: "14 GB"
    cpu: "16"
    disks: "local-disk " + disk_size + " HDD"
  }
  output {
    File output_bam = "${output_bam_basename}.bam"
    File bwa_stderr_log = "${output_bam_basename}.bwa.stderr.log"
  }
}

# Merge original input uBAM file with BWA-aligned BAM file
task MergeBamAlignment {
  File unmapped_bam
  String bwa_commandline
  String bwa_version
  File aligned_bam
  String output_bam_basename
  File ref_fasta
  File ref_fasta_index
  File ref_dict

  Int disk_size

  command {
    # set the bash variable needed for the command-line
    bash_ref_fasta=${ref_fasta}
    java -Xmx2500m -jar /usr/gitc/picard.jar \
      MergeBamAlignment \
      VALIDATION_STRINGENCY=SILENT \
      EXPECTED_ORIENTATIONS=FR \
      ATTRIBUTES_TO_RETAIN=X0 \
      ALIGNED_BAM=${aligned_bam} \
      UNMAPPED_BAM=${unmapped_bam} \
      OUTPUT=${output_bam_basename}.bam \
      REFERENCE_SEQUENCE=${ref_fasta} \
      PAIRED_RUN=true \
      SORT_ORDER="unsorted" \
      IS_BISULFITE_SEQUENCE=false \
      ALIGNED_READS_ONLY=false \
      CLIP_ADAPTERS=false \
      MAX_RECORDS_IN_RAM=2000000 \
      ADD_MATE_CIGAR=true \
      MAX_INSERTIONS_OR_DELETIONS=-1 \
      PRIMARY_ALIGNMENT_STRATEGY=MostDistant \
      PROGRAM_RECORD_ID="bwamem" \
      PROGRAM_GROUP_VERSION="${bwa_version}" \
      PROGRAM_GROUP_COMMAND_LINE="${bwa_commandline}" \
      PROGRAM_GROUP_NAME="bwamem" \
      UNMAPPED_READ_STRATEGY=COPY_TO_TAG \
      ALIGNER_PROPER_PAIR_FLAGS=true \
      UNMAP_CONTAMINANT_READS=true
  }
  runtime {
    docker: "broadinstitute/genomes-in-the-cloud:2.2.5-1486412288"
    memory: "3500 MB"
    cpu: "1"
    disks: "local-disk " + disk_size + " HDD"
  }
  output {
    File output_bam = "${output_bam_basename}.bam"
  }
}

# Sort BAM file by coordinate order and fix tag values for NM and UQ
task SortAndFixTags {
  File input_bam
  String output_bam_basename
  File ref_dict
  File ref_fasta
  File ref_fasta_index
  Int disk_size

  command {
    set -o pipefail

    java -Xmx4000m -jar /usr/gitc/picard.jar \
    SortSam \
    INPUT=${input_bam} \
    OUTPUT=/dev/stdout \
    SORT_ORDER="coordinate" \
    CREATE_INDEX=false \
    CREATE_MD5_FILE=false | \
    java -Xmx500m -jar /usr/gitc/picard.jar \
    SetNmAndUqTags \
    INPUT=/dev/stdin \
    OUTPUT=${output_bam_basename}.bam \
    CREATE_INDEX=true \
    CREATE_MD5_FILE=true \
    REFERENCE_SEQUENCE=${ref_fasta}
  }
  runtime {
    docker: "broadinstitute/genomes-in-the-cloud:2.2.5-1486412288"
    disks: "local-disk " + disk_size + " HDD"
    cpu: "1"
    memory: "5000 MB"
  }
  output {
    File output_bam = "${output_bam_basename}.bam"
    File output_bam_index = "${output_bam_basename}.bai"
    File output_bam_md5 = "${output_bam_basename}.bam.md5"
  }
}

# Mark duplicate reads to avoid counting non-independent observations
task MarkDuplicates {
  Array[File] input_bams
  String output_bam_basename
  String metrics_filename
  Int disk_size

 # Task is assuming query-sorted input so that the Secondary and Supplementary reads get marked correctly.
 # This works because the output of BWA is query-grouped and therefore, so is the output of MergeBamAlignment.
 # While query-grouped isn't actually query-sorted, it's good enough for MarkDuplicates with ASSUME_SORT_ORDER="queryname"
  command {
    java -Xmx4000m -jar /usr/gitc/picard.jar \
      MarkDuplicates \
      INPUT=${sep=' INPUT=' input_bams} \
      OUTPUT=${output_bam_basename}.bam \
      METRICS_FILE=${metrics_filename} \
      VALIDATION_STRINGENCY=SILENT \
      OPTICAL_DUPLICATE_PIXEL_DISTANCE=2500 \
      ASSUME_SORT_ORDER="queryname"
      CREATE_MD5_FILE=true
  }
  runtime {
    docker: "broadinstitute/genomes-in-the-cloud:2.2.5-1486412288"
    memory: "7 GB"
    disks: "local-disk " + disk_size + " HDD"
  }
  output {
    File output_bam = "${output_bam_basename}.bam"
    File duplicate_metrics = "${metrics_filename}"
  }
}

# Generate sets of intervals for scatter-gathering over chromosomes
task CreateSequenceGroupingTSV {
  File ref_dict

  # Use python to create the Sequencing Groupings used for BQSR and PrintReads Scatter. 
  # It outputs to stdout where it is parsed into a wdl Array[Array[String]]
  # e.g. [["1"], ["2"], ["3", "4"], ["5"], ["6", "7", "8"]]
  command <<<
    python <<CODE
    with open("${ref_dict}", "r") as ref_dict_file:
        sequence_tuple_list = []
        longest_sequence = 0
        for line in ref_dict_file:
            if line.startswith("@SQ"):
                line_split = line.split("\t")
                # (Sequence_Name, Sequence_Length)
                sequence_tuple_list.append((line_split[1].split("SN:")[1], int(line_split[2].split("LN:")[1])))
        longest_sequence = sorted(sequence_tuple_list, key=lambda x: x[1], reverse=True)[0][1]
    # We are adding this to the intervals because hg38 has contigs named with embedded colons (:) and a bug in 
    # some versions of GATK strips off the last element after a colon, so we add this as a sacrificial element.
    hg38_protection_tag = ":1+"
    # initialize the tsv string with the first sequence
    tsv_string = sequence_tuple_list[0][0] + hg38_protection_tag
    temp_size = sequence_tuple_list[0][1]
    for sequence_tuple in sequence_tuple_list[1:]:
        if temp_size + sequence_tuple[1] <= longest_sequence:
            temp_size += sequence_tuple[1]
            tsv_string += "\t" + sequence_tuple[0] + hg38_protection_tag
        else:
            tsv_string += "\n" + sequence_tuple[0] + hg38_protection_tag
            temp_size = sequence_tuple[1]
    # add the unmapped sequences as a separate line to ensure that they are recalibrated as well
    with open("sequence_grouping.txt","w") as tsv_file:
      tsv_file.write(tsv_string)
      tsv_file.close()

    tsv_string += '\n' + "unmapped"

    with open("sequence_grouping_with_unmapped.txt","w") as tsv_file_with_unmapped:
      tsv_file_with_unmapped.write(tsv_string)
      tsv_file_with_unmapped.close()
    CODE
  >>>
  runtime {
    docker: "python:2.7"
    memory: "2 GB"
  }
  output {
    Array[Array[String]] sequence_grouping = read_tsv("sequence_grouping.txt")
    Array[Array[String]] sequence_grouping_with_unmapped = read_tsv("sequence_grouping_with_unmapped.txt")
  }
}

# Generate Base Quality Score Recalibration (BQSR) model
task BaseRecalibrator {
  File input_bam
  File input_bam_index
  String recalibration_report_filename
  Array[String] sequence_group_interval
  File dbSNP_vcf
  File dbSNP_vcf_index
  Array[File] known_indels_sites_VCFs
  Array[File] known_indels_sites_indices
  File ref_dict
  File ref_fasta
  File ref_fasta_index
  Int disk_size

  command { // 
    java -Xmx4000m \
      -jar /usr/gitc/GATK35.jar \
      -T BaseRecalibrator \
      -R ${ref_fasta} \
      -I ${input_bam} \
      --useOriginalQualities \
      -o ${recalibration_report_filename} \
      -knownSites ${dbSNP_vcf} \
      -knownSites ${sep=" -knownSites " known_indels_sites_VCFs} \
      -L ${sep=" -L " sequence_group_interval}
  }
  runtime {
    docker: "broadinstitute/genomes-in-the-cloud:2.2.5-1486412288"
    memory: "6 GB"
    disks: "local-disk " + disk_size + " HDD"
  }
  output {
    File recalibration_report = "${recalibration_report_filename}"
  }
}

# Combine multiple recalibration tables from scattered BaseRecalibrator runs
# Note that when run from GATK 3.x the tool is not a walker and is invoked differently.
task GatherBqsrReports {
  Array[File] input_bqsr_reports
  String output_report_filename
  Int disk_size

  command {
    java -Xmx3000m \
      -cp /usr/gitc/GATK35.jar org.broadinstitute.gatk.tools.GatherBqsrReports \
      I= ${sep=' I= ' input_bqsr_reports} \
      O= ${output_report_filename}
    }
  runtime {
    docker: "broadinstitute/genomes-in-the-cloud:2.2.5-1486412288"
    memory: "3500 MB"
    disks: "local-disk " + disk_size + " HDD"
  }
  output {
    File output_bqsr_report = "${output_report_filename}"
  }
}

# Apply Base Quality Score Recalibration (BQSR) model
task ApplyBQSR {
  File input_bam
  File input_bam_index
  String output_bam_basename
  File recalibration_report
  Array[String] sequence_group_interval
  File ref_dict
  File ref_fasta
  File ref_fasta_index
  Int disk_size

  command {  
    java -Xmx3000m \
      -jar /usr/gitc/GATK35.jar \
      -T PrintReads \
      -R ${ref_fasta} \
      -I ${input_bam} \
      --useOriginalQualities \
      -o ${output_bam_basename}.bam \
      -BQSR ${recalibration_report} \
      -SQQ 10 -SQQ 20 -SQQ 30 \
      -L ${sep=" -L " sequence_group_interval}
  }
  runtime {
    docker: "broadinstitute/genomes-in-the-cloud:2.2.5-1486412288"
    memory: "3500 MB"
    disks: "local-disk " + disk_size + " HDD"
  }
  output {
    File recalibrated_bam = "${output_bam_basename}.bam"
  }
}

# Combine multiple recalibrated BAM files from scattered ApplyRecalibration runs
task GatherBamFiles {
  Array[File] input_bams
  String output_bam_basename
  Int disk_size

  command {
    java -Xmx2000m -jar /usr/gitc/picard.jar \
      GatherBamFiles \
      INPUT=${sep=' INPUT=' input_bams} \
      OUTPUT=${output_bam_basename}.bam \
      CREATE_INDEX=true \
      CREATE_MD5_FILE=true
    }
  runtime {
    docker: "broadinstitute/genomes-in-the-cloud:2.2.5-1486412288"
    memory: "3 GB"
    disks: "local-disk " + disk_size + " HDD"
  }
  output {
    File output_bam = "${output_bam_basename}.bam"
    File output_bam_index = "${output_bam_basename}.bai"
    File output_bam_md5 = "${output_bam_basename}.bam.md5"
  }
}

# WORKFLOW DEFINITION 
workflow GenericPreProcessingWorkflow {

  String sample_name
  String base_file_name
  Array[File] flowcell_unmapped_bams
  String unmapped_bam_suffix
  
  File ref_fasta
  File ref_fasta_index
  File ref_dict
  File ref_alt
  File ref_bwt
  File ref_sa
  File ref_amb
  File ref_ann
  File ref_pac
  
  File dbSNP_vcf
  File dbSNP_vcf_index
  Array[File] known_indels_sites_VCFs
  Array[File] known_indels_sites_indices
  
  Int flowcell_small_disk
  Int flowcell_medium_disk
  Int agg_small_disk
  Int agg_medium_disk
  Int agg_large_disk

  String bwa_commandline="bwa mem -K 100000000 -p -v 3 -t 16 -Y $bash_ref_fasta"

  String recalibrated_bam_basename = base_file_name + ".aligned.duplicates_marked.recalibrated"

  # Get the version of BWA to include in the PG record in the header of the BAM produced 
  # by MergeBamAlignment. 
  call GetBwaVersion

  # Align flowcell-level unmapped input bams in parallel
  scatter (unmapped_bam in flowcell_unmapped_bams) {
  
    # Because of a wdl/cromwell bug this is not currently valid so we have to sub(sub()) in each task
    # String base_name = sub(sub(unmapped_bam, "gs://.*/", ""), unmapped_bam_suffix + "$", "")

    String sub_strip_path = "gs://.*/"
    String sub_strip_unmapped = unmapped_bam_suffix + "$"

    # Map reads to reference
    call SamToFastqAndBwaMem {
      input:
        input_bam = unmapped_bam,
        bwa_commandline = bwa_commandline,
        output_bam_basename = sub(sub(unmapped_bam, sub_strip_path, ""), sub_strip_unmapped, "") + ".unmerged",
        ref_fasta = ref_fasta,
        ref_fasta_index = ref_fasta_index,
        ref_dict = ref_dict,
        ref_alt = ref_alt,
        ref_bwt = ref_bwt,
        ref_amb = ref_amb,
        ref_ann = ref_ann,
        ref_pac = ref_pac,
        ref_sa = ref_sa,
        disk_size = flowcell_medium_disk
     }

    # Merge original uBAM and BWA-aligned BAM 
    call MergeBamAlignment {
      input:
        unmapped_bam = unmapped_bam,
        bwa_commandline = bwa_commandline,
        bwa_version = GetBwaVersion.version,
        aligned_bam = SamToFastqAndBwaMem.output_bam,
        output_bam_basename = sub(sub(unmapped_bam, sub_strip_path, ""), sub_strip_unmapped, "") + ".aligned.unsorted",
        ref_fasta = ref_fasta,
        ref_fasta_index = ref_fasta_index,
        ref_dict = ref_dict,
        disk_size = flowcell_medium_disk
    }

    # Sort and fix tags in the merged BAM
    call SortAndFixTags as SortAndFixReadGroupBam {
      input:
      input_bam = MergeBamAlignment.output_bam,
      output_bam_basename = sub(sub(unmapped_bam, sub_strip_path, ""), sub_strip_unmapped, "") + ".sorted",
      ref_dict = ref_dict,
      ref_fasta = ref_fasta,
      ref_fasta_index = ref_fasta_index,
      disk_size = flowcell_medium_disk
    }

  }

  # Aggregate aligned+merged flowcell BAM files and mark duplicates
  # We take advantage of the tool's ability to take multiple BAM inputs and write out a single output
  # to avoid having to spend time just merging BAM files.
  call MarkDuplicates {
    input:
      input_bams = MergeBamAlignment.output_bam,
      output_bam_basename = base_file_name + ".aligned.unsorted.duplicates_marked",
      metrics_filename = base_file_name + ".duplicate_metrics",
      disk_size = agg_large_disk
  }

  # Sort aggregated+deduped BAM file and fix tags
  call SortAndFixTags as SortAndFixSampleBam {
    input:
      input_bam = MarkDuplicates.output_bam,
      output_bam_basename = base_file_name + ".aligned.duplicate_marked.sorted",
      ref_dict = ref_dict,
      ref_fasta = ref_fasta,
      ref_fasta_index = ref_fasta_index,
      disk_size = agg_large_disk
  }

  # Create list of sequences for scatter-gather parallelization 
  call CreateSequenceGroupingTSV {
    input:
      ref_dict = ref_dict
  }
  
  # Perform Base Quality Score Recalibration (BQSR) on the sorted BAM in parallel
  scatter (subgroup in CreateSequenceGroupingTSV.sequence_grouping) {
    # Generate the recalibration model by interval
    call BaseRecalibrator {
      input:
        input_bam = SortAndFixSampleBam.output_bam,
        input_bam_index = SortAndFixSampleBam.output_bam_index,
        recalibration_report_filename = base_file_name + ".recal_data.csv",
        sequence_group_interval = subgroup,
        dbSNP_vcf = dbSNP_vcf,
        dbSNP_vcf_index = dbSNP_vcf_index,
        known_indels_sites_VCFs = known_indels_sites_VCFs,
        known_indels_sites_indices = known_indels_sites_indices,
        ref_dict = ref_dict,
        ref_fasta = ref_fasta,
        ref_fasta_index = ref_fasta_index,
        disk_size = agg_small_disk
    }  
  }  
  
  # Merge the recalibration reports resulting from by-interval recalibration
  call GatherBqsrReports {
    input:
      input_bqsr_reports = BaseRecalibrator.recalibration_report,
      output_report_filename = base_file_name + ".recal_data.csv",
      disk_size = flowcell_small_disk
  }

  scatter (subgroup in CreateSequenceGroupingTSV.sequence_grouping_with_unmapped) {

    # Apply the recalibration model by interval
    call ApplyBQSR {
      input:
        input_bam = SortAndFixSampleBam.output_bam,
        input_bam_index = SortAndFixSampleBam.output_bam_index,
        output_bam_basename = recalibrated_bam_basename,
        recalibration_report = GatherBqsrReports.output_bqsr_report,
        sequence_group_interval = subgroup,
        ref_dict = ref_dict,
        ref_fasta = ref_fasta,
        ref_fasta_index = ref_fasta_index,
        disk_size = agg_small_disk
    }
  } 

  # Merge the recalibrated BAM files resulting from by-interval recalibration
  call GatherBamFiles {
    input:
      input_bams = ApplyBQSR.recalibrated_bam,
      output_bam_basename = base_file_name,
      disk_size = agg_large_disk
  }

  # Outputs that will be retained when execution is complete  
  output {
    File duplication_metrics = MarkDuplicates.duplicate_metrics
    File bqsr_report = GatherBqsrReports.output_bqsr_report
    File analysis_ready_bam = GatherBamFiles.output_bam
    File analysis_ready_bam_index = GatherBamFiles.output_bam_index
    File analysis_ready_bam_md5 = GatherBamFiles.output_bam_md5
  } 
}
