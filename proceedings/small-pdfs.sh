#!/bin/bash
for filename in *.pdf; 
do 
 gs \
 -sDEVICE=pdfwrite \
 -dCompatibilityLevel=1.4 \
 -dPDFSETTINGS=/prepress \
 -dNOPAUSE \
 -dQUIET \
 -dBATCH \
 -o "${filename}-sml.pdf" \
 ${filename}; 
done
