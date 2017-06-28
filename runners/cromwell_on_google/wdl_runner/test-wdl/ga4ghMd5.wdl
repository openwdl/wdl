task md5 {
  File inputFile

  command {
    /bin/my_md5sum ${inputFile}
  }

 output {
    File value = "md5sum.txt"
 }

 runtime {
   docker: "quay.io/briandoconnor/dockstore-tool-md5sum:1.0.2"
   cpu: 1
   memory: "512 MB"
 }
}

workflow ga4ghMd5 {
 File inputFile
 call md5 { input: inputFile=inputFile }
}