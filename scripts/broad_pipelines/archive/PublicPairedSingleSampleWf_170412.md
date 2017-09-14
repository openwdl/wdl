This document outlines the data transformation steps and describes some pertinent parameters of the **PairedEndSingleSampleWf** workflow. As the name implies, the workflow is specific to processing paired end reads for a single sample. The pipeline implements the first segment of the GATK Best Practices (ca. June 2016) for performing germline variant discovery in human whole-genome sequencing (WGS) data. It begins with unaligned paired reads in BAM format, proceeds through alignment against GRCh38/hg38 as the reference genome, pre-processing and variant calling with HaplotypeCaller, and results in a sample-level germline SNP and INDEL variant callset in GVCF format.

- This document is specific to the public WDL script **PublicPairedSingleSampleWf_170412.wdl** with an April 12, 2017 date stamp found [here](https://github.com/broadinstitute/wdl/blob/develop/scripts/broad_pipelines).
- The workflow uses Docker container **broadinstitute/genomes-in-the-cloud:2.2.5-1486412288**. [Docker](https://software.broadinstitute.org/firecloud/documentation/article?id=6886) containers provide reproducible analysis environments, including specific tool versions. Thus, the commands and the given parameters pertain only to these specific tool versions. It is possible for prior or future versions of tools to give different results.
- Furthermore, the **parameters within the pipeline are optimized for WGS and GRCh38**. Optimal performance on other types of data and other species may require changes to parameters. For example, [Step 3](#3) includes code that calculates how to split the reference contigs for parallel processing that caps the genomic interval per process by the longest contig in the reference. This splits human GRCh38 18-ways and caps each group of contigs by the size of human chromosome 1. This approach may need revision for efficient processing of genomes where the longest contig length deviates greatly from human.
- The **JSON files of inputs and options** provided with this WDL constitute a runnable example, as all files and dependencies are publicly available. The read data provided was downsampled to run in a reasonable amount of time on most platforms, so it is not representative of a full scale data, but it does exercise all processing and analysis steps realistically. 

The structure of this document distinguishes the WORKFLOW section and the TASKS that are called in the workflow. The **WORKFLOW definition section** provides an overview of the logic and organization of the data transformations and analyses performed in the pipeline. The **TASK definitions section** provides more granular details of each step, where each task generally corresponds to the invocation of one tool command. By convention, tasks are generally written before the workflow in WDL scripts, but here we go over the workflow first because it will make more sense to the reader -- unless they're from Mars, in which case who knows. Note that **Quality control tasks** are not mentioned in the description of the workflow to avoid distracting from the narrative flow of data transformations and analyses, and their task definitions are summarized as a group at the end of this document.

----
## Jump to a section

### WORKFLOW definition [overview](#0)
1. [Map with BWA-MEM and merge to create clean BAM](#1)
2. [Flag duplicates with MarkDuplicates](#2)
3. [Base quality score recalibration](#3)
4. [Call SNP and INDEL variants with HaplotypeCaller](#4)

### TASK definitions [overview](#tasksoverview)
- [CheckFinalVcfExtension](#CheckFinalVcfExtension)
- [GetBwaVersion](#GetBwaVersion)
- [SamToFastqAndBwaMem](#SamToFastqAndBwaMem)
- [MergeBamAlignment](#MergeBamAlignment)
- [SortAndFixTags](#SortAndFixTags)
- [MarkDuplicates](#MarkDuplicates)
- [CreateSequenceGroupingTSV](#CreateSequenceGroupingTSV)
- [BaseRecalibrator](#BaseRecalibrator)
- [GatherBqsrReports](#GatherBqsrReports)
- [ApplyBQSR](#ApplyBQSR)
- [GatherBamFiles](#GatherBamFiles)
- [ConvertToCram](#ConvertToCram)
- [HaplotypeCaller](#HaplotypeCaller)
- [GatherVCFs](#GatherVCFs)
- [Quality control tasks](#QC)

----
## What is NOT covered
- How to read WDL. This document assumes a basic understanding of WDL components.
- The JSON files describing inputs and options. 
- Runtime parameters optimized for Broad's Google Cloud Platform implementation.
- Interpretation of quality control results.

### Related resources
- For details on interpreting and writing WDL scripts, see the [QuickStart guide](https://software.broadinstitute.org/wdl/userguide/index).
- Scatter-Gather Parallelism. See [wdl plumbing options](https://software.broadinstitute.org/wdl/userguide/topic?name=wdl-plumbing) for information.
- Intervals lists. See **Section 3** of [Article#1204](https://software.broadinstitute.org/gatk/documentation/article?id=1204).

----
## Requirements
### Software
- See [Article#6671](https://software.broadinstitute.org/wdl/documentation/article?id=6671) for setup options in using Cromwell to execute WDL workflows. For an introduction, see [Article#7349](https://software.broadinstitute.org/gatk/blog?id=7349).
- Docker container `broadinstitute/genomes-in-the-cloud:2.2.5-1486412288` uses the following tool versions for this pipeline. These tools in turn require Java JDK v8 (specifically 8u111 is used) and Python v2.7.

````
*PICARD_VERSION="1.1150"
GATK35_VERSION="3.5-0-g36282e4"
GATK36_VERSION="3.6-44-ge7d1cd2"
GATK4_VERSION="4.alpha-249-g7df4044"
SAMTOOLS_VERSION="1.3.1"
BWA_VERSION="0.7.15.r1140"
SVTOOLKIT_VERSION="2.00-1650"
TABIX_VERSION=0.2.5_r1005"
BGZIP_VERSION="1.3"

* Note that the Picard version given here does not use the same numbering as the public Picard releases.

````

### Scripts and data
- Pipeline WDL script and JSON file defining input data.
- (Optional) JSON file defining additional Cromwell options.
- Human whole genome paired end sequence reads in unmapped BAM (uBAM) format.
    - Each uBAM is per read group and the header defines read group `ID`, `SM`, `LB`, `PL` and optionally `PU`. Because each file is for the same sample, their `SM` fields will be identical. Each read has an `RG` tag.
    - Each uBAM has the same suffix, e.g. `.unmapped.bam`.
    - Each uBAM passes validation by [ValidateSamFile](https://software.broadinstitute.org/gatk/guide/article?id=7571).
    - Reads are in query-sorted order.
- GRCh38 reference genome FASTA including [alternate contigs](https://software.broadinstitute.org/gatk/documentation/article?id=7857), corresponding `.fai` index and `.dict` dictionary and six BWA-specific index files `.alt`, `.sa`, `.amb`, `.bwt`, `.ann` and `.pac`.
- Known variant sites VCFs and corresponding indexes for masking during base quality score recalibration (BQSR). A separate article will document these data resources.
- Intervals lists for scattered variant calling with HaplotypeCaller. It is necessary to predefine the calling intervals carefully. In this workflow we use 50 `.interval_list` files that each contain multiple calling intervals. The calling intervals are an intersection of (i) calling regions of interest and (ii) regions bounded by Ns, otherwise known as gaps in the genome. See the **External Resources** section of [Article#7857](https://software.broadinstitute.org/gatk/documentation/article?id=7857) for an example gap file. Use of these defined intervals has the following benefits.
    - Avoids calling twice on a locus. This can happen when reads overlapping an interval boundary expand the interval under consideration such that the same variant is called twice.
    - Makes calls taking into consideration all the available reads that align to the same locus.

----
<a name="0"></a>
# WORKFLOW definition overview
L1087 opens the WORKFLOW block; the workflow name is **PairedEndSingleSampleWorkflow**.

After the workflow name, we start the WORKFLOW body by listing the variables that can stand in for files, parameters or even parts of commands within tasks, e.g. the command for BWA alignment (L1128). The actual file paths and values are provided in an accompanying [**JSON** file](https://github.com/broadinstitute/wdl/blob/develop/scripts/broad_pipelines/PublicPairedSingleSampleWf_170412.inputs.json).

Then we list the calls to tasks that will be executed. Calls may be listed in any order, as the order in which steps are run only depends on how they're connected to other tasks (and therefore, when their inputs become available), but we like to list them in the order that is most intuitively understandable for humans.

Let's break down the workflow into logical steps and examine their component commands.

----
<a name="1"></a>
## 1. Map with BWA-MEM and merge to create clean BAM
#### This step takes the unaligned BAM, aligns with BWA-MEM, merges information between the unaligned and aligned BAM and fixes tags and sorts the BAM.

- 1.0: L1134 - Call task [GetBwaVersion](#GetBwaVersion) to note the version of BWA for use in step [1.3] and call [CheckFinalVcfExtension](#CheckFinalVcfExtension) to make sure the final output is named according to our convention.
- 1.1: L1143 - Define a "scatter" block to parallelize the next set of operations (including [1.2], [1.3] and [1.4]) over each `unmapped_bam` in the list of BAMs (given by the variable `flowcell_unmapped_bams`). These "flowcell BAMs" correspond to subsets of the data that were run on different flowcells (because the sample library was multiplexed) and therefore are identified as separate "readgroups". As a result of the scatter definition, each flowcell BAM (also often called "readgroup BAM") will be processed independently through this segment of the pipeline.

▶︎ Observe the nesting of commands via their relative indentation. Our script writers use these indentations not because they make a difference for Cromwell interpretation but because they allow us human readers to visually comprehend where the scattering applies. 

- 1.2: L1161 - Call task [SamToFastqAndBwaMem](#SamToFastqAndBwaMem) to map reads to the reference using BWA-MEM. We use `bwa_commandline` from LX(549) as the actual command.
- 1.3: L1180 - Call task [MergeBamAlignment](#MergeBamAlignment) to merge information between the unaligned and aligned BAM. Both `bwa_commandline` and `bwa_version` define elements of the `bwamem` program group `@PG` line in the BAM header. The data resulting from this step go on to step [2].
- 1.4: L1204 - Call task [SortAndFixTags](#SortAndFixTags) and uses [task aliasing](https://software.broadinstitute.org/wdl/userguide/plumbing#alias) to rename it **SortAndFixReadGroupBam**. The consequence of this is that the workflow can then differentiate outputs from those a later call made to the same task on different inputs in [2.1]. This task coordinate sorts and indexes the alignments and fixes the `NM` and `UQ` tags whose calculations depend on coordinate sort order. This data transformation allows for validation with [ValidateSamFile](https://www.broadinstitute.org/gatk/guide/article?id=7571), which is covered briefly in the section on [Quality Control tasks](#QC).

----
<a name="2"></a>
## 2. Flag duplicates with MarkDuplicates
#### This step aggregates sample BAMs, flags duplicate sets, fixes tags and coordinate sorts. It starts with the output of [1.3]
- 2.0: L1235 - Call task [MarkDuplicates](#MarkDuplicates) to accomplish two aims. First, since MarkDuplicates is given all the files output by the [MergeBamAlignment](#MergeBamAlignment) task, and these by design all belong to the same sample, we effectively aggregate the starting BAMs into a single sample-level BAM. Second, MarkDuplicates flags reads it determines are from duplicate inserts with the 0x400 bitwise SAM flag. Because MarkDuplicates sees query-grouped read alignment records from the output of MergeBamAlignment, it will also mark as duplicate the unmapped mates and supplementary alignments within the duplicate set.
- 2.1: L1244 - Call task [SortAndFixTags](#SortAndFixTags) and renames it as **SortAndFixSampleBam** to differentiate outputs from those of the earlier call made to the same task. This task coordinate sorts and indexes the alignments and fixes the `NM` and `UQ` tags whose calculations depend on coordinate sort order. Resulting data go on to step [3].

----
<a name="3"></a>
## 3. Base quality score recalibration
#### This step creates intervals for scattering, performs BQSR, merges back the scattered results into a single file and finally compresses the BAM to CRAM format.

- 3.0: L1267 - Call task [CreateSequenceGroupingTSV](#CreateSequenceGroupingTSV) to create intervals from the reference genome's `.dict` dictionary for subsequent use in [3.1] and [3.3].
- 3.1: L1286 - Define a scatter across the intervals created in [3.0] and call task [BaseRecalibrator](#BaseRecalibrator) to act on each interval of the BAM from [2.1], resulting in a recalibration table per interval.
- 3.2: L1307 - Call task [GatherBqsrReports](#GatherBqsrReports) to consolidate the per-interval recalibration tables into a single recalibration table whose sums reflect the consolidated data.
- 3.3: L1315 - Define a scatter across the intervals created in [3.0] and call task [ApplyBQSR](#ApplyBQSR) to use the `GatherBqsrReports.output_bqsr_report` from [3.2] and apply the recalibration to the BAM from [2.1] per interval defined by [3.0]. Each resulting recalibrated BAM will contain alignment records from the specified interval including [unmapped reads from singly mapping pairs](https://software.broadinstitute.org/gatk/documentation/article?id=6976). These unmapped records _retain_ SAM alignment information, e.g. mapping contig and coordinate information, but have an asterisk `*` in the CIGAR field.
- 3.4: L1334 - Call task [GatherBamFiles](#GatherBamFiles) to concatenate the recalibrated BAMs from [3.3], in order, into a single indexed BAM that retains the header from the first BAM. Resulting data go onto step [4].
- 3.5: L1427 - Call task [ConvertToCram](#ConvertToCram) to compress the BAM further into reference-dependent indexed CRAM format. Note that there is also a CramToBam task that roundtrips the data back into BAM format; the purpose is to check that nothing was lost in the conversion process. The corresponding quality check will fail if you use a CRAM compression setting that produces lossy compression (which we do not use here).

----
<a name="4"></a>
## 4. Call SNP and INDEL variants with HaplotypeCaller
#### This final step uses HaplotypeCaller to call variants over intervals then merges data into a GVCF for the sample, the final output of the workflow.

- 4.0: L1464 - Define a scatter across intervals (defined within the JSON file under `scattered_calling_intervals`) to parallelize the HaplotypeCaller GVCF generation. We use only the [primary assembly contigs](https://software.broadinstitute.org/gatk/documentation/article?id=7857) of GRCh38, grouped into 50 intervals lists, to call variants. Within the GRCh38 intervals lists, the primary assembly's contigs are divided by contiguous regions between regions of Ns. The called task then uses this list of regions to parallelize the task via the `-L ${interval_list}` option.

▶︎ For this pipeline workflow's setup, fifty parallel processes makes sense for a genome of 3 billion basepairs. However, given the same setup, the 50-way split is overkill for a genome of 370 million basepairs as in the case of the [pufferfish](http://www.genomenewsnetwork.org/articles/06_00/puffer_fish.shtml).

- 4.1: L1467 - Call task [HaplotypeCaller](#HaplotypeCaller) to call SNP and INDEL variants on the BAM from [3.5] per interval, resulting in a [GVCF format](https://software.broadinstitute.org/gatk/documentation/article?id=4017) variant call file for each interval interval.

- 4.2: L1483 - Call task [MergeVCFs](#MergeVCFs) to merge the per-interval GVCFs into one single-sample GVCF. The tool concatenates the GVCFs in the same order as the `input_vcfs` array, which is ordered by contig.

- 4.3: L1522 - Define files that copy to an output directory if given an OPTIONS JSON file that defines the output directory. If you omit the OPTIONS JSON or omit defining the outputs directory in the OPTIONS JSON, then the workflow skips this step.

-------------------------
<a name="tasksoverview"></a>
# TASK DEFINITIONS

<a name="CheckFinalVcfExtension"></a>
### CheckFinalVcfExtension
This task checks that the final GVCF filename that is going to be used ends with ".g.vcf.gz". This is a GATK convention that is intended to help differentiate GVCFs from regular VCFs. There is also a practical consequence: when we use this convention, the GATK engine recognizes that it needs to adjust some settings when it writes the output file's index, and so we don't need to specify those settings manually in our command. Note that we still specify those arguments in this pipeline to be really explicit, even though they are not necessary. 

<a name="GetBwaVersion"></a>
### GetBwaVersion
This task obtains the version of BWA to later notate within the BAM program group (`@PG`) line. This is because we like to keep a record of all commands that were run on the data within the file headers. 

<a name="SamToFastqAndBwaMem"></a>
### SamToFastqAndBwaMem
The input to this task is an unaligned queryname-sorted BAM and the output is an aligned query-grouped BAM. This step pipes three processes: (i) conversion of BAM to FASTQ reads, (ii) alternate-contig-aware alignment with BWA-MEM and (iii) conversion of SAM to BAM reads. BWA-MEM requires FASTQ reads as input and produces SAM format reads. This task maps the reads using the BWA command defined as a string variable.

- _Dictionary_ [Article#7857](https://software.broadinstitute.org/gatk/documentation/article?id=7857) defines alternate contigs and other reference genome components.
- [Step 3D of Tutorial#6483](https://software.broadinstitute.org/gatk/documentation/article?id=6483#step3D) explains the concepts behind piping these processes.
- See [Tutorial#8017](https://software.broadinstitute.org/gatk/documentation/article?id=8017) for more details on BWA-MEM's alt-aware alignment.

The alt-aware alignment depends on use of GRCh38 as the reference, the versions 0.7.13+ of BWA and the presence of BWA's ALT index from [bwa-kit](https://github.com/lh3/bwa/tree/master/bwakit). If the `ref_alt` ALT index has no content or is not present, then the script exits with an `exit 1` error. What this means is that this task is only compatible with a reference with ALT contigs and it only runs in an alt-aware manner.

<a name="MergeBamAlignment"></a>
### MergeBamAlignment
This step takes an unmapped BAM and the aligned BAM and merges information from each. Reads, sequence and quality information and meta information from the unmapped BAM merge with the alignment information in the aligned BAM. The BWA version the script obtains from task [GetBwaVersion](#GetBwaVersion) is used here in the program group (`@PG`) `bwamem`. What is imperative for this step, that is implied by the script, is that the sort order of the unmapped and aligned BAMs are identical, i.e. query-group sorted. The BWA-MEM alignment step outputs reads in exactly the same order as they are input and so groups mates, secondary and supplementary alignments together for a given read name. The merging step requires both files maintain this ordering and will produce a final merged BAM in the same query-grouped order given the `SORT_ORDER="unsorted"` parameter. This has implications for how the [MarkDuplicates task](#MarkDuplicates) will flag duplicate sets.

Because the `ATTRIBUTES_TO_RETAIN` option is set to `X0`, any aligner-specific tags that are literally `X0` will carryover to the merged BAM. BWA-MEM does not output such a tag but does output `XS` and `XA` tags for suboptimal alignment score and alternative hits, respectively. However, these do not carryover into the merged BAM. Merging retains certain tags from either input BAM (`RG`, `SA`, `MD`, `NM`, `AS` and `OQ` if present), replaces the `PG` tag as the command below defines and adds new tags (`MC`, `MQ` and `FT`).

▶︎ Note the `NM` tag values will be incorrect at this point and the `UQ` tag is absent. Update and addition of these are dependent on coordinate sort order. Specifically, the script uses a separate [SortAndFixTags](#SortAndFixTags) task to fix `NM` tags and add `UQ` tags.

The `UNMAP_CONTAMINANT_READS=true` option applies to likely cross-species contamination, e.g. bacterial contamination. MergeBamAlignment identifies reads that are (i) softclipped on both ends and (ii) map with less than 32 basepairs as contaminant. For a similar feature in GATK, see [OverclippedReadFilter](https://software.broadinstitute.org/gatk/documentation/tooldocs/org_broadinstitute_gatk_engine_filters_OverclippedReadFilter.php). If MergeBamAlignment determines a read is contaminant, then the mate is also considered contaminant. MergeBamAlignment unmaps the pair of reads by (i) setting the 0x4 flag bit, (ii) replacing column 3's contig name with an asterisk `*`, (iii) replacing columns 4 and 5 (POS and MAPQ) with zeros, and (iv) adding the `FT` tag to indicate the reason for unmapping the read, e.g. `FT:Z:Cross-species contamination`. The records retain their CIGAR strings. Note other processes also use the `FT` tag, e.g. to indicate reasons for setting the QCFAIL 0x200 flag bit, and will use different tag descriptions.

<a name="SortAndFixTags"></a>
### SortAndFixTags
This task (i) sorts reads by coordinate and then (ii) corrects the NM tag values, adds UQ tags and indexes a BAM. The task pipes the two commands. First, SortSam sorts the records by genomic coordinate using the `SORT_ORDER="coordinate"` option. Second, SetNmAndUqTags calculates and fixes the UQ and NM tag values in the BAM. Because `CREATE_INDEX=true`, SetNmAndUqTags creates the `.bai` index. Again, we create an MD5 file with the `CREATE_MD5_FILE=true` option.

As mentioned in the [MergeBamAlignment](#MergeBamAlignment) task, tag values dependent on coordinate-sorted records require correction in this separate task given this workflow maintains query-group ordering through the pre-processing steps.

<a name="MarkDuplicates"></a>
### MarkDuplicates
This task flags duplicate reads. Because the input is query-group-sorted, MarkDuplicates flags with the 0x400 bitwise SAM flag duplicate primary alignments as well as the duplicate set's secondary and supplementary alignments. Also, for singly mapping mates, duplicate flagging extends to cover unmapped mates. These extensions are features that are only available to query-group-sorted BAMs.

This command uses the `ASSUME_SORT_ORDER="queryname"` parameter to tell the tool the sort order to expect. Within the context of this workflow, at the point this task is called, we will have avoided any active sorting that would label the BAM header. We know that our original flowcell BAM is queryname-sorted and that BWA-MEM maintains this order to give us query-grouped alignments.

The `OPTICAL_DUPLICATE_PIXEL_DISTANCE` of 2500 is set for Illumina sequencers that use patterned flowcells to _estimate_ the number of sequencer duplicates. Sequencer duplicates are a subspecies of the duplicates that the tool flags. The Illumina HiSeq X and HiSeq 4000 platforms use patterened flowcells. If [estimating library complexity](https://software.broadinstitute.org/gatk/documentation/article?id=6747#section4) (see section _Duplicate metrics in brief_) is important to you, then adjust the `OPTICAL_DUPLICATE_PIXEL_DISTANCE` appropriately for your sequencer platform.

Finally, in this task and others, we produce an MD5 file with the `CREATE_MD5_FILE=true` option. This creates a 128-bit hash value using the [MD5 algorithm](https://en.wikipedia.org/wiki/MD5) that is to files much like a fingerprint is to an individual. Compare MD5 values to verify data integrity, e.g. after moving or copying large files.

<a name="CreateSequenceGroupingTSV"></a>
### CreateSequenceGroupingTSV
This task uses a python script written as a single command using [heredoc syntax](https://en.wikipedia.org/wiki/Here_document) to create a list of contig groupings. The workflow uses the intervals to scatter the base quality recalibration step [3] that calls on BaseRecalibrator and ApplyBQSR tasks.

This workflow specifically uses [Python v2.7](https://docs.python.org/2/).

The input to the task is the reference `.dict` dictionary that lists contigs. The code takes the information provided by the `SN` and `LN` tags of each `@SQ` line in the dictionary to pair the information in a tuple list. The `SN` tag names a contig while the `LN` tag measures the contig length. This list is ordered by descending contig length.

The contig groupings this command creates is in WDL array format where each line represents a group and each group's members are tab-separated. The command adds contigs to each group from the previously length-sorted list in descending order and caps the sum of member lengths by the first contig's sequence length (the longest contig). This has the effect of somewhat evenly distributing sequence per group. For GRCh38, `CreateSequenceGroupingTSV-stdout.log` shows 18 such groups.

As the code adds contig names to groups, it adds a `:1+` to the end of each name. This is to protect the names from downstream tool behavior that removes elements after the last `:` within a contig name. GRCh38 introduces contig names that include `:`s and removing the last element make certain contigs indistinguishable from others. With this appendage, we preserve the original contig names through downstream processes. GATK v3.5 and prior versions require this addition.

<a name="BaseRecalibrator"></a>
### BaseRecalibrator
The task runs BaseRecalibrator to detect errors made by the sequencer in estimating base quality scores. BaseRecalibrator builds a model of covariation from mismatches in the alignment data while excluding known variant sites and creates a recalibration report for use in the next step. The engine parameter `--useOriginalQualities` asks BaseRecalibrator to use original sequencer-produced base qualities stored in the `OQ` tag if present or otherwise use the standard QUAL score. The known sites files should include sites of known common SNPs and INDELs.

This task runs per interval grouping defined by each `-L` option. The `sep` in  `-L ${sep=" -L " sequence_group_interval}` ensures each interval in the _sequence_group_interval_ list is given by the command.

<a name="GatherBqsrReports"></a>
### GatherBqsrReports
This task consolidates the recalibration reports from each sequence group interval into a single report using GatherBqsrReports, so that the recalibration will be based on the observations made on all the data, not just per-batch of contigs.

<a name="ApplyBQSR"></a>
### ApplyBQSR
The task uses ApplyBQSR and the recalibration report to correct base quality scores in the BAM. Again, using parallelization, this task applies recalibration for the sequence intervals defined with `-L`. A resulting recalibrated BAM will contain only reads for the intervals in the applied intervals list.

<a name="GatherBamFiles"></a>
### GatherBamFiles
This task concatenates provided BAMs in order, into a single BAM and retains the header of the first file. For this pipeline, this includes the recalibrated sequence grouped BAMs and the recalibrated unmapped reads BAM. For GRCh38, this makes 19 BAM files that the task concatenates together. The resulting BAM is already in coordinate-sorted order. The task creates a new sequence index and MD5 file for the concatenated BAM.

<a name="ConvertToCram"></a>
### ConvertToCram
This task compresses a BAM to an even smaller [CRAM format](https://samtools.github.io/hts-specs/CRAMv3.pdf) using the `-C` option of Samtools. The task then indexes the CRAM and renames it from `{basename}.cram.crai` to `{basename}.crai`. CRAM is a fairly new format and tool developers are actively refining features for compatibility. Make sure your tool chain is compatible with CRAM before deleting BAMs. Be aware when using CRAMs that you will have to specify the _identical_ reference genome, not just _equivalent_ reference, with matching MD5 hashes for each contig. These can differ if the capitalization of reference sequences differ.

<a name="HaplotypeCaller"></a>
### HaplotypeCaller
This task runs HaplotypeCaller on the recalibrated BAM for given intervals and produces variant calls in [GVCF format](https://software.broadinstitute.org/gatk/documentation/article?id=4017). HaplotypeCaller reassembles and realign reads around variants and calls genotypes and genotype likelihoods for single nucleotide polymorphism (SNP) and insertion and deletion (INDELs) variants. Proximal variants are phased. The resulting file is a GZ compressed file, a valid VCF format file with extension `.g.vcf.gz`, containing variants for the given interval.

- The WORKFLOW's [step 4](#4) defines whether any parallelization is applied.

The `-ERC GVCF` or _emit reference confidence_ mode has two key consequences. First, the tool will emit block records for non-variant sites, which allows us to record information about the quality and quantity of the evidence observed there, and estimate how confident we are that sites in these blocks are actually non-variant. Second, for each record in the GVCF call, the tool will include a symbolic `<NON_REF>` _non-reference allele_ and will calculate phred-scaled likelihoods (PL annotation) for all possible genotypes. See the GATK documentation for more information on this functionality.

- The `--max_alternate_alleles` is set to 3 for performance optimization. This does not limit the alleles that are genotyped, only the number of alleles that HaplotypeCaller emits.
- We specify `-variant_index_parameter 128000` and `-variant_index_type LINEAR` to set the indexing strategy for the output GVCF (though it's not strictly necessary when we use the ".g.vcf" output naming convention). See [Article#3893](https://software.broadinstitute.org/gatk/documentation/article?id=3893) for details on this convention.
- The command invokes an additional read, the [OverclippedReadFilter]((https://software.broadinstitute.org/gatk/documentation/tooldocs/org_broadinstitute_gatk_engine_filters_OverclippedReadFilter.php)), with `--read_filter OverclippedRead` that removes  reads that are likely from foreign contaminants, e.g. bacterial contamination. The filter define such reads as those that align with less than 30 basepairs and are softclipped on both ends of the read. This option is similar to the [MergeBamAlignment task](#MergeBamAlignment)'s `UNMAP_CONTAMINANT_READS=true` option that unmaps contaminant reads less than 32 basepairs.

<a name="MergeVCFs"></a>
### MergeVCFs
The task uses MergeVcfs to combine multiple VCF files resulting from scatter-gather parallelization into a single VCF file and index. Note that in this case we are applying it to GVCFs; the tool is agnostic to the differences between regular VCFs and GVCFS, and just cares that the files are valid VCFs (which GVCFs are).

<a name="QC"></a>
### Quality Control tasks
A considerable number of quality control tasks are run in the course of this workflow. We do not recapitulate them all here, but we note that there are two general categories of QC tasks: format validation, identity validation, and metrics collection. 

- **Format validation** aims to verify that the outputs are correctly formatted, to ensure that they will go through the rest of the pipeline smoothly. You can read more about BAM file validation in [Article#7571](https://software.broadinstitute.org/gatk/documentation/article?id=7571). 
- **Identity validation** aims to verify that the read data we are working with belongs to the sample identified in the inputs. This is done to detect cases where materials or data files got mislabeled (generally through human error), resulting in either partial swaps (e.g. one readgroup does not belong to the same sample as the others) or total swaps (all the data belongs to a different sample). The most important identity validation is based on "fingerprinting", i.e. comparing genotypes determined on-the-fly from the read data with genotypes determined by running the original biological sample through a genotyping array (which we do for every sample that enters our facility). This allows us to detect sample swaps extremely accurately. As secondary validation measures, we also compare that all read groups support the same genotypes (to detect partial swaps) and we estimate cross-sample contamination. The contamination estimate is used later to inform the variant calling process.
- **Metrics collection** aims to evaluate the quality of the data at multiple levels. This allows us to flag problem samples early in the process and continuously monitor the quality of the outputs of our facilities. 

In addition, the WDL script includes some basic descriptive comments for all QC calls and tasks. 


----
