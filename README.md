# MCContact

# To run
```
login to lxplus6
cmsrel CMSSW_9_3_6_patch1
cd CMSSW_9_3_6_patch1/src
cmsenv
cd -
cmsRun HIG-RunIIFall17wmLHEGS-01124_1_cfg.py
```

# For running madspin issues
```
login to lxplus6/7
cmsrel CMSSW_9_3_8
cd CMSSW_9_3_8/src/
cmsenv
scram b
cd -
#(check the gridpack path)
cmsRun HIG-RunIIFall17wmLHEGS-01124_2_cfg.py
```