FROM amazonlinux:2017.03
RUN yum install libfreetype.so.6 -y yum install libpthread.so.0 -y yum install fontconfig -y 
COPY ["Lib/*"              , "/home/glasswall/"]
COPY ["GWQtCLI"            , "/home/glasswall/"]
RUN cd /home/glasswall/ && \
    ln -s /home/glasswall/libglasswall_core2.so /usr/lib/libglasswall_core2.so.2 && \
    ln -s /home/glasswall/libQt5Concurrent.so /usr/lib/libQt5Concurrent.so.5 && \
    ln -s /home/glasswall/libQt5Core.so /usr/lib/libQt5Core.so.5 && \
    ln -s /home/glasswall/libquazip.so /usr/lib/libquazip.so.1 && \
    ln -s /home/glasswall/libQt5Xml.so /usr/lib/libQt5Xml.so.5 && \
    ln -s /home/glasswall/libicui18n.so /usr/lib/libicui18n.so.56 && \
    ln -s /home/glasswall/libicuuc.so /usr/lib/libicuuc.so.56 && \
    ln -s /home/glasswall/libicudata.so /usr/lib/libicudata.so.56 && \
    ln -s /home/glasswall/libQt5Gui.so /usr/lib/libQt5Gui.so.5 && \
    ldconfig /usr/lib

WORKDIR /home/glasswall
RUN chmod +x ./GWQtCLI

CMD /home/glasswall/GWQtCLI -i /input -o /output
