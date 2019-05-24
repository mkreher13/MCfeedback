#!/bin/sh

for i in {1..40}
do
	rm PinGeo/*.xml
	cp PinGeo/Reference/*.xml PinGeo/
	python3 Feedback.py
done