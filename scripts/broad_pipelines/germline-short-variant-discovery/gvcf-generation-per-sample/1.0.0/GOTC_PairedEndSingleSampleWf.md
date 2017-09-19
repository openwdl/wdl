## Workflow overview

This WDL pipeline implements data pre-processing and initial variant
calling (GVCF generation) according to the GATK Best Practices (June 2016) for 
germline SNP and Indel discovery in human whole-genome sequencing (WGS) 
data. 

### Data requirements/expectations :
- Human whole-genome pair-end sequencing data in unmapped BAM (uBAM) format
- One or more read groups, one per uBAM file, all belonging to a single sample (SM) (see further below for implementation notes related to read groups)
- Input uBAM files must additionally comply with the following requirements:
  - filenames all have the same suffix (we use ".unmapped.bam")
  - files must pass validation by ValidateSamFile
  - reads are provided in query-sorted order
  - all reads must have an RG tag
- GVCF output names must end in ".g.vcf.gz"
- Reference genome must be provided with an index of ALT contigs

### Version notes

This workflow replaces the `PublicPairedSingleSampleWf_170412.wdl` workflow. The processing done on the data is functionally equivalent; the major change in this new version consists in some technical refactoring that delivers significant cost optimizations on the Google Cloud Platform (GCP). This workflow will NOT run on other platforms due to the use of Google NIO; see below for details. 

----

## Implementation notes 

### Autosizing

This workflow uses autosizing, i.e. it estimates the disk size that is needed for each task depending on the total size of its input and some assumptions about the relative size of its outputs. This helps ensure that we're not requesting (and paying for) disk sizes that are unnecessarily large, without needing to configure this for each run. 

### Use of Google NIO

Several tasks in this workflow use the [NIO Filesystem Provider for GCS](https://github.com/GoogleCloudPlatform/google-cloud-java/tree/master/google-cloud-contrib/google-cloud-nio), which makes it specific to the Google Cloud platform. This manifests as inputs that would normally be typed as a `File` being typed as a `String` instead, in tasks that call GATK4 tools (BaseRecalibrator, ApplyBQSR, and HaplotypeCaller). Setting the input type to `String` means the file doesn’t get localized, but GATK4 knows how to deal with a gs:// path. IMPORTANT: This does not work outside of GCP, because either the other cloud providers don't have an equivalent streaming library like Google's NIO, or GATK4 doesn't know about them. To run this elsewhere you would need to switch the type of those inputs to `File` and adjust the disk autosizing to expect a full file instead of a slice (namely remove the denominator in the calculation).

Note that to run with NIO in FireCloud, you need to provide credentials in a private bucket. A howto document will be provided soon. 

### Read group inputs

The workflow is optimized for the shape of the data that is most prevalent at the Broad Institute, where genomes are comprised of data sequenced on many different lanes through multiplexing. The main way this manifests is that BWA alignment is scattered by read group. So for genomes comprised of single, monolithic read groups, this workflow may be less economical than expected, in large part because the individual tasks will run much longer (even as there are fewer of them) and are more likely to get preempted.

