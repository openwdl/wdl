all: deps compile run
deps:
	sh ../download.sh
compile:
	javac -cp ".:*" Main.java
run:
	java -cp ".:*" Main ../example.wdl
clean:
	-rm -rf *.class *.jar
