README.md for wdl/scripts/tutorials/gatk/

This folder contains WDL scripts for workflows outlined in GATK website tutorials.

## Easily find information on each tutorial
The WDL scripts within this `gatk` folder come from tutorials from the [GATK Tutorials](https://software.broadinstitute.org/gatk/documentation/topic?name=tutorials) website. Numbers in the file names correspond to website article numbers. For example, for `tutorial_8017.wdl` you can plug in `8017` into the following URL to view the corresponding tutorial description. Use the base URL for each website as shown below.

- **GATK website URL**: https://software.broadinstitute.org/gatk/documentation/article?id=8017

## Download example data
The tutorials come with example data that you can use with the scripts. Find the links to download example data on respective tutorial webpages. Alternatively, you may download the example data from either the FTP site or our shared Google Drive folder. Example data bundle names also include the website article number.

- **FTP site**: `ftp://gsapubftp-anonymous@ftp.broadinstitute.org/tutorials/datasets`. Copy and paste the ftp address into a web browser. Leave the password field blank.
- **GoogleDrive folder**: [https://drive.google.com/open?id=0B3LMJn1Ee-xofnhyNF92cFY2bzJaMDMwZUF2amstcDdWNVpEenoxSGxiWGJkd1o2S1JNTXM](https://drive.google.com/open?id=0BzI1CyccGsZibnRtQjhaakxobEE).

## Be sure to fill in the JSON for your setup
If a WDL script comes with a matching example JSON file and you choose to use this file, then be sure to modify the directory paths to files for your own setup. Otherwise, generate a blank JSON file with the following command, then fill in the details.

    java -jar wdltool.jar inputs file.wdl > file.json

The example JSON file can show you how to list files that are in array format.

## Information on setting up Cromwell to run WDL scripts
- See [WDL Article#6671](https://software.broadinstitute.org/wdl/guide/article?id=6671) for Cromwell setup options.
- See [GATK Blog#7349](https://software.broadinstitute.org/gatk/blog?id=7349) for an introduction to Cromwell and WDL.
- For details on interpreting and writing WDL scripts, see the [QuickStart guide](https://software.broadinstitute.org/wdl/userguide/index).

If you modify a WDL script, be sure it passes validation with the following command.

    java -jar wdltool.jar validate file.wdl

Finally, run a script with inputs using this command:

    java -jar cromwell.jar run file.wdl file.json
