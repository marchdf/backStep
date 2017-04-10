#!/bin/bash

cwd=`pwd`
mpibin=/Users/mhenryde/spack/opt/spack/darwin-elcapitan-x86_64/gcc-6.3.0/openmpi-2.0.2-62xsvcb5fa4rhlndyzdxdozaf7illg3s/bin/mpiexec

declare -a fdirs=("33" "65" "129" "257" "513")

for fdir in "${fdirs[@]}"
do
cd "$fdir"
echo `pwd`
${mpibin} -np 1 ${HOME}/wind/NaluWindUtils/build/preprocessing/nalu_preprocess -i add_ndtw.yaml
cd "$cwd"
done
