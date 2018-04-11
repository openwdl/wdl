COMMONS_CODEC='commons-codec-1.10'
COMMONS_LANG='commons-lang3-3.4'

if [ ! -f ${COMMONS_LANG}.jar ]; then
  curl -L http://apache.spinellicreations.com//commons/lang/binaries/${COMMONS_LANG}-bin.tar.gz | tar xvz
  cp ${COMMONS_LANG}/${COMMONS_LANG}.jar .
  rm -rf ${COMMONS_LANG}
fi

if [ ! -f ${COMMONS_CODEC}.jar ]; then
  curl -L http://mirror.metrocast.net/apache//commons/codec/binaries/${COMMONS_CODEC}-bin.tar.gz | tar xvz
  cp ${COMMONS_CODEC}/${COMMONS_CODEC}.jar .
  rm -rf ${COMMONS_CODEC}
fi
