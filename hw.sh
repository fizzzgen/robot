#!/bin/bash
printf "Content-type: text/html\n\n"
read POST_STRING
printf "WORKING! HERE IS YOUR POST STRING:\n"
printf ${POST_STRING}



