// PYTHIA is licenced under the GNU GPL version 2, see COPYING for details.
// Please respect the MCnet Guidelines, see GUIDELINES for details.

#include "Pythia8/Pythia.h"

#include "fastjet/PseudoJet.hh"
#include "fastjet/ClusterSequence.hh"

using namespace Pythia8;

bool isLeptonic(Event& process, int j){

  int idau = process[j].daughter1(); 
  if (process[idau].idAbs() == 5) idau = process[j].daughter2(); 
  if (process[idau].idAbs() > 10 && process[idau].idAbs() < 20)    return true;
  else if (process[idau].isFinal()) return false;
  else return isLeptonic(process, idau);

}


int main() {
  // Settings
  int  nEvent = 1000;
  bool doMPI  = false;

  // Generator
  Pythia pythia;

  // Single W production
  pythia.readString("Top:gg2ttbar = on");
  pythia.readString("Top:qqbar2ttbar = on");  

  // Swtich between top -> H+ and tbar -> H-
  bool top2H = true;

  // Switch between turning above decay on/off
  bool allowH = true;

  // Switch to tun on jets (Anti-kt)
  bool makeJets = false;

  // Add new top decay; 

  if (allowH) {
    pythia.readString("37:m0 = 81.0");
    pythia.readString("6:addChannel = on 0.10 100 5 37");
    pythia.readString("37:oneChannel = on 1.0 100 4 -3");
    pythia.readString("6:onMode = off");

  }

  // Turn off W decay to selectively choose based on top
  pythia.readString("24:onMode = off");


  if (top2H) {
    // Positive t to H+ b (or W+ (-> cs) b)
    if (allowH) {
      pythia.readString("6:onPosIfAny = 37");
      pythia.readString("6:onNegIfAny = 24");
    }
    pythia.readString("24:onNegIfAny = 11 13 -11 -13");
    pythia.readString("24:onPosIfAny = 4 3 -4 -3");
  }
  else {
    // tbar to H- bbar (or W- (->cs) bbar)
    if (allowH){
      pythia.readString("6:onNegIfAny = 37");
      pythia.readString("6:onPosIfAny = 24");
    }
    pythia.readString("24:onPosIfAny = 11 13 -11 -13");
    pythia.readString("24:onNegIfAny = 4 3 -4 -3");
  }

  if (!makeJets) {
    pythia.readString("PartonLevel:ISR = off");
    pythia.readString("PartonLevel:FSR = off");    
    pythia.readString("PartonLevel:MPI = off");
    pythia.readString("HadronLevel:Hadronize = off");
  }

  pythia.init();

  // Histograms

  Hist costc("Cosine of angle between top and charm", 100,-1.0,1.0);
  Hist cosbc("Cosine of angle between bottom and charm (of the same top)", 100,-1.0,1.0);
  Hist coslc("Cosine of angle between lepton (other top) and charm", 100, -1.0, 1.0);

  // Fastjet analysis - select algorithm and parameters
  double Rparam = 0.4;
  fastjet::Strategy               strategy = fastjet::Best;
  fastjet::RecombinationScheme    recombScheme = fastjet::E_scheme;
  fastjet::JetDefinition         *jetDef = NULL;
  jetDef = new fastjet::JetDefinition(fastjet::kt_algorithm, Rparam,
                                      recombScheme, strategy);

  // Fastjet input
  std::vector <fastjet::PseudoJet> fjInputs;

  // Begin event loop. Generate event. Skip if error.
  for (int iEvent = 0; iEvent < nEvent; ++iEvent) {
    if (!pythia.next()) continue;

    Vec4 hadtop, leptop, charm, csSum, lep, bhad;
    int ihadTop = 0, ilepTop = 0, icharm = 0, ilep = 0;

    // Loop over hard event
    for (int i = 0; i < pythia.process.size(); i++){
      
      // Find hadronic and leptonic tops
      if (pythia.process[i].idAbs() == 6){
	
	if (isLeptonic(pythia.process, i)) { leptop = pythia.process[i].p(); ilepTop = i;}
	else { hadtop = pythia.process[i].p(); ihadTop = i;}

      }
      
      // Find the charm
      if (pythia.process[i].idAbs() == 4) {
	icharm = i;

	if (allowH) charm = pythia.process[i].p();
	else charm = pythia.process[i].p();
      }

      // Find the charged lepton
      if (pythia.process[i].idAbs() == 11 || pythia.process[i].idAbs() == 13) {
	ilep = i;
	lep = pythia.process[i].p();
      }
    }

    // Find the b from hadronic top
    for(int i = pythia.process[ihadTop].daughter1(); i < pythia.process[ihadTop].daughter2(); i++)
      if (pythia.process[i].idAbs() == 5) bhad = pythia.process[i].p();

    double costcVal = dot3(hadtop, charm)/ hadtop.pAbs() / charm.pAbs();
    double cosbcVal = dot3(bhad, charm)/ bhad.pAbs() / charm.pAbs();
    double coslcVal = dot3(lep, charm)/ lep.pAbs() / charm.pAbs();    

    costc.fill(costcVal);
    cosbc.fill(cosbcVal);
    coslc.fill(coslcVal);

    // Use jets
    if (!makeJets) continue;

    // Reset Fastjet input
    fjInputs.resize(0);

    // Keep track of missing ET
    Vec4 missingETvec;

    // Loop over event record to decide what to pass to FastJet
    for (int i = 0; i < pythia.event.size(); ++i) {
      // Final state only
      if (!pythia.event[i].isFinal())        continue;

      // No neutrinos
      if (pythia.event[i].idAbs() == 12 || pythia.event[i].idAbs() == 14 ||
          pythia.event[i].idAbs() == 16)     continue;

      // Skip leptons coming from hard W decay
      if (pythia.event[i].idAbs() == 11 || pythia.event[i].idAbs() == 13) {
	int iMoth = pythia.event[i].mother1();
	bool skip = false;
	while(true){
	  if (iMoth == 0) break; 
	  if (pythia.event[iMoth].idAbs() == 24) { skip = true; break;}
	  else { iMoth = pythia.event[iMoth].mother1(); }
	}

	if (skip) continue;
      }
	  
      // Only |eta| < 3.6
      if (fabs(pythia.event[i].eta()) > 3.6) continue;

      // Missing ET
      missingETvec += pythia.event[i].p();

      // Store as input to Fastjet
      fjInputs.push_back( fastjet::PseudoJet( pythia.event[i].px(),
        pythia.event[i].py(), pythia.event[i].pz(), pythia.event[i].e() ) );
    }

    if (fjInputs.size() == 0) {
      cout << "Error: event with no final state particles" << endl;
      continue;
    }

    // Run Fastjet algorithm
    vector <fastjet::PseudoJet> inclusiveJets, sortedJets;
    fastjet::ClusterSequence clustSeq(fjInputs, *jetDef);

    // For the first event, print the FastJet details
    if (iEvent == 0) {
      cout << "Ran " << jetDef->description() << endl;
      cout << "Strategy adopted by FastJet was "
           << clustSeq.strategy_string() << endl << endl;
    }

    // Extract inclusive jets sorted by pT (note minimum pT of 20.0 GeV)
    inclusiveJets = clustSeq.inclusive_jets(20.0);
    sortedJets    = sorted_by_pt(inclusiveJets);

  // End of event loop.
  }

  // Statistics
  pythia.stat();

  // Output histograms
  double sigmapb = pythia.info.sigmaGen() * 1.0E9;

  costc *= sigmapb / nEvent;
  cosbc *= sigmapb / nEvent;
  coslc *= sigmapb / nEvent;

  ofstream of;
  of.open("hist.dat");

  costc.table(of);
  of << endl << endl;

  //cosbc.table(of);
  //of << endl << endl;

  //coslc.table(of);
  //of << endl << endl;

  of.close();

  // Done.
  delete jetDef;
  return 0;
}
