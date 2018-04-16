COMMONS_CODEC='commons-codec-1.10'
COMMONS_LANG='commons-lang3-3.4'

if [ ! -f ${COMMONS_CODEC}.jar ]; then
  wget https://repo1.maven.org/maven2/commons-codec/commons-codec/1.10/${COMMONS_CODEC}.jar
fi

if [ ! -f ${COMMONS_LANG}.jar ]; then
  wget http://central.maven.org/maven2/com/hynnet/commons-lang3/3.4/${COMMONS_LANG}.jar
fi
