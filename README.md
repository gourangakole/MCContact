# MCContact

# To run
```
login to lxplus7
export SCRAM_ARCH=slc7_amd64_gcc700
cmsrel CMSSW_10_6_9
cd CMSSW_10_6_9/src
cmsenv
scram b
cd -
wget https://raw.githubusercontent.com/gourangakole/MCContact/master/HIG-RunIISummer19UL17wmLHEGEN-00538_1_cfg.py 
cmsRun HIG-RunIISummer19UL17wmLHEGEN-00538_1_cfg.py

```
# Dump eventcontent from root file
```
[gkole@lxplus729:gkole]$ edmDumpEventContent HIG-RunIISummer19UL17wmLHEGEN-00538.root
Type                                  Module                      Label     Process   
--------------------------------------------------------------------------------------
GenEventInfoProduct                   "generator"                 ""        "GEN"     
LHEEventProduct                       "externalLHEProducer"       ""        "GEN"     
ROOT::Math::PositionVector3D<ROOT::Math::Cartesian3D<float>,ROOT::Math::DefaultCoordinateSystemTag>    "genParticles"              "xyz0"    "GEN"     
edm::HepMCProduct                     "generatorSmeared"          ""        "GEN"     
edm::RandomEngineStates               "randomEngineStateProducer"   ""        "GEN"     
edm::TriggerResults                   "TriggerResults"            ""        "GEN"     
float                                 "genParticles"              "t0"      "GEN"     
vector<int>                           "genParticles"              ""        "GEN"     
vector<reco::GenJet>                  "ak4GenJets"                ""        "GEN"     
vector<reco::GenJet>                  "ak4GenJetsNoNu"            ""        "GEN"     
vector<reco::GenJet>                  "ak8GenJets"                ""        "GEN"     
vector<reco::GenJet>                  "ak8GenJetsNoNu"            ""        "GEN"     
vector<reco::GenMET>                  "genMetCalo"                ""        "GEN"     
vector<reco::GenMET>                  "genMetTrue"                ""        "GEN"     
vector<reco::GenParticle>             "genParticles"              ""        "GEN"     
[gkole@lxplus729:gkole]$ cp HIG-RunIISummer19UL17wmLHEGEN-00538_1_cfg.py /afs/cern.ch/user/g/gkole/work/MC_contact/various-script/public_file/MCContact/

```