#!/bin/sh

for SCRIPTDIR in scripts/*; do
	cp templates/kustomization.yml ${SCRIPTDIR}
	NAME=$(basename ${SCRIPTDIR})
	echo "nameSuffix: -${NAME}" >> ${SCRIPTDIR}/kustomization.yml
done
kustomize edit add resource scripts/*
sed -i 's/^-/  -/' kustomization.yml
