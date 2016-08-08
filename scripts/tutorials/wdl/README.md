### Easily find information in each tutorial
---

The WDL scripts in this folder are designed to teach you aspects and features of WDL, mainly using GATK tools for demonstration purposes. They follow the tutorial documents located on the WDL website, under the Tutorials category

- https://software.broadinstitute.org/wdl/userguide/topic?name=wdl-tutorials

Each  tutorial script located in this folder will have a link in its header that points to its specific tutorial document. You can copy and paste that link into your browser window and follow along with the document in order to write your own script. These are designed in a way that you should be using the scripts uploaded to this folder as a means of checking your work. 

### Example data
---

Each tutorial document will link you to the specific `.zip` file associated with each script. These `.zip` files contain all the example data you will need to run the script, in addition to the sample script itself. You can find these `.zip` files here:

- https://drive.google.com/open?id=0BwTg3aXzGxEDMUs0cURPcnFiQzA

### Be sure to generate a JSON for your setup
---

You can also find in this folder the matching JSON files which point to the various inputs needed to run the script. These sample JSONs contain dummy paths that should be replaced with the appropriate path to the file in question. If you would like to simply generate a JSON with no dummy paths, you can use the command below.

```
java -jar wdltool.jar inputs file.wdl > file.json
```

### Additional resources
---

- **Set up your machine to run WDL scripts:** https://software.broadinstitute.org/wdl/guide/article?id=6671
- **Quick start guide to WDL:** https://software.broadinstitute.org/wdl/userguide/
- **GATK Best Practices:** https://software.broadinstitute.org/gatk/best-practices/
