#!/bin/bash
clear
sudo mkdir "output"
sudo mkdir "log"
pyout=`date +"PythonOutput-"%Y-%m-%d.%H:%M:%S".txt"`
pyexit=`date +"ExitOutput-"%Y-%m-%d.%H:%M:%S".txt"`
sudo python SingleProcessTest.py > $pyout
sudo echo $? > $pyexit
sudo mv $pyout log/
sudo mv $pyexit output/
tarname=`date +"SERVER_3_RUN_FILES_"%Y_%m_%d_%H_%M_%S".tgz"`
cd ..
sudo tar -zcvf $tarname server
sudo aws s3 cp $tarname s3://ecmega-project-bucket/server-outputs/
