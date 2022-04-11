#!/bin/bash

for lang in c h f f90
do
	for ext in report translated original
	do
		find . -name \*.${lang}.${ext} -delete
	done
done
