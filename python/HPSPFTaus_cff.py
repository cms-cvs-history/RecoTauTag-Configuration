import FWCore.ParameterSet.Config as cms
import copy

'''

Sequences for HPS taus

'''

# Define the discriminators for this tau
from RecoTauTag.RecoTau.PFRecoTauDiscriminationByIsolation_cfi                      import *
from RecoTauTag.RecoTau.PFRecoTauDiscriminationByMVAIsolation_cfi                   import *
from RecoTauTag.RecoTau.PFRecoTauDiscriminationByLeadingTrackFinding_cfi            import *
from RecoTauTag.RecoTau.PFRecoTauDiscriminationAgainstElectron_cfi                  import *
from RecoTauTag.RecoTau.PFRecoTauDiscriminationAgainstElectronMVA_cfi               import *
from RecoTauTag.RecoTau.PFRecoTauDiscriminationAgainstElectronMVA2_cfi              import *
from RecoTauTag.RecoTau.PFRecoTauDiscriminationAgainstElectronMVA3_cfi              import *
from RecoTauTag.RecoTau.PFRecoTauDiscriminationAgainstElectronDeadECAL_cfi          import *
from RecoTauTag.RecoTau.PFRecoTauDiscriminationAgainstMuon_cfi                      import *
from RecoTauTag.RecoTau.PFRecoTauDiscriminationAgainstMuon2_cfi                     import *

# Load helper functions to change the source of the discriminants
from RecoTauTag.RecoTau.TauDiscriminatorTools import *

# Select those taus that pass the HPS selections
#  - pt > 15, mass cuts, tauCone cut
from RecoTauTag.RecoTau.PFRecoTauDiscriminationByHPSSelection_cfi import hpsSelectionDiscriminator
hpsPFTauDiscriminationByDecayModeFinding = hpsSelectionDiscriminator.clone(
    PFTauProducer = cms.InputTag('hpsPFTauProducer')
)

# Define decay mode prediscriminant
requireDecayMode = cms.PSet(
    BooleanOperator = cms.string("and"),
    decayMode = cms.PSet(
        Producer = cms.InputTag('hpsPFTauDiscriminationByDecayModeFinding'),
        cut = cms.double(0.5)
    )
)

#Building the prototype for  the Discriminator by Isolation
hpsPFTauDiscriminationByLooseIsolation = pfRecoTauDiscriminationByIsolation.clone(
    PFTauProducer = cms.InputTag("hpsPFTauProducer"),
    Prediscriminants = requireDecayMode.clone(),
    ApplyDiscriminationByTrackerIsolation = False,
    ApplyDiscriminationByECALIsolation = True,
    applyOccupancyCut = True
)
hpsPFTauDiscriminationByLooseIsolation.Prediscriminants.preIso = cms.PSet(
    Producer = cms.InputTag("hpsPFTauDiscriminationByLooseChargedIsolation"),
    cut = cms.double(0.5))

# Make an even looser discriminator
hpsPFTauDiscriminationByVLooseIsolation = hpsPFTauDiscriminationByLooseIsolation.clone(
    customOuterCone = cms.double(0.3),
    isoConeSizeForDeltaBeta = cms.double(0.3),
)
hpsPFTauDiscriminationByVLooseIsolation.qualityCuts.isolationQualityCuts.minTrackPt = 1.5
hpsPFTauDiscriminationByVLooseIsolation.qualityCuts.isolationQualityCuts.minGammaEt = 2.0
hpsPFTauDiscriminationByVLooseIsolation.Prediscriminants.preIso.Producer =  cms.InputTag("hpsPFTauDiscriminationByVLooseChargedIsolation")

hpsPFTauDiscriminationByMediumIsolation = hpsPFTauDiscriminationByLooseIsolation.clone()
hpsPFTauDiscriminationByMediumIsolation.qualityCuts.isolationQualityCuts.minTrackPt = 0.8
hpsPFTauDiscriminationByMediumIsolation.qualityCuts.isolationQualityCuts.minGammaEt = 0.8
hpsPFTauDiscriminationByMediumIsolation.Prediscriminants.preIso.Producer = cms.InputTag("hpsPFTauDiscriminationByMediumChargedIsolation")

hpsPFTauDiscriminationByTightIsolation = hpsPFTauDiscriminationByLooseIsolation.clone()
hpsPFTauDiscriminationByTightIsolation.qualityCuts.isolationQualityCuts.minTrackPt = 0.5
hpsPFTauDiscriminationByTightIsolation.qualityCuts.isolationQualityCuts.minGammaEt = 0.5
hpsPFTauDiscriminationByTightIsolation.Prediscriminants.preIso.Producer = cms.InputTag("hpsPFTauDiscriminationByTightChargedIsolation")

hpsPFTauDiscriminationByIsolationSeq = cms.Sequence(
    hpsPFTauDiscriminationByVLooseIsolation*
    hpsPFTauDiscriminationByLooseIsolation*
    hpsPFTauDiscriminationByMediumIsolation*
    hpsPFTauDiscriminationByTightIsolation
)

_isolation_types = ['VLoose', 'Loose', 'Medium', 'Tight']
# Now build the sequences that apply PU corrections

# Make Delta Beta corrections (on SumPt quantity)
hpsPFTauDiscriminationByVLooseIsolationDBSumPtCorr = hpsPFTauDiscriminationByVLooseIsolation.clone(
    deltaBetaPUTrackPtCutOverride = cms.double(0.5),
    applyDeltaBetaCorrection = True,
    isoConeSizeForDeltaBeta = 0.8,
    deltaBetaFactor = "%0.4f"%(0.0123/0.1687),
    applyOccupancyCut = False,
    applySumPtCut = True,
)
hpsPFTauDiscriminationByVLooseIsolationDBSumPtCorr.maximumSumPtCut=hpsPFTauDiscriminationByVLooseIsolationDBSumPtCorr.qualityCuts.isolationQualityCuts.minGammaEt

hpsPFTauDiscriminationByLooseIsolationDBSumPtCorr = hpsPFTauDiscriminationByLooseIsolation.clone(
    deltaBetaPUTrackPtCutOverride = cms.double(0.5),
    applyDeltaBetaCorrection = True,
    isoConeSizeForDeltaBeta = 0.8,
    deltaBetaFactor = "%0.4f"%(0.0123/0.1687),
    applyOccupancyCut = False,
    applySumPtCut = True,
)
hpsPFTauDiscriminationByLooseIsolationDBSumPtCorr.maximumSumPtCut=hpsPFTauDiscriminationByLooseIsolationDBSumPtCorr.qualityCuts.isolationQualityCuts.minGammaEt

hpsPFTauDiscriminationByMediumIsolationDBSumPtCorr = hpsPFTauDiscriminationByMediumIsolation.clone(
    deltaBetaPUTrackPtCutOverride = cms.double(0.5),
    applyDeltaBetaCorrection = True,
    isoConeSizeForDeltaBeta = 0.8,
    deltaBetaFactor = "%0.4f"%(0.0462/0.1687),
    applyOccupancyCut = False,
    applySumPtCut = True,
)
hpsPFTauDiscriminationByMediumIsolationDBSumPtCorr.maximumSumPtCut=hpsPFTauDiscriminationByMediumIsolationDBSumPtCorr.qualityCuts.isolationQualityCuts.minGammaEt

hpsPFTauDiscriminationByTightIsolationDBSumPtCorr = hpsPFTauDiscriminationByTightIsolation.clone(
    deltaBetaPUTrackPtCutOverride = cms.double(0.5),
    applyDeltaBetaCorrection = True,
    isoConeSizeForDeltaBeta = 0.8,
    deltaBetaFactor = "%0.4f"%(0.0772/0.1687),
    applyOccupancyCut = False,
    applySumPtCut = True,
)
hpsPFTauDiscriminationByTightIsolationDBSumPtCorr.maximumSumPtCut=hpsPFTauDiscriminationByTightIsolationDBSumPtCorr.qualityCuts.isolationQualityCuts.minGammaEt

hpsPFTauDiscriminationByIsolationSeqDBSumPtCorr = cms.Sequence(
    hpsPFTauDiscriminationByVLooseIsolationDBSumPtCorr*
    hpsPFTauDiscriminationByLooseIsolationDBSumPtCorr*
    hpsPFTauDiscriminationByMediumIsolationDBSumPtCorr*
    hpsPFTauDiscriminationByTightIsolationDBSumPtCorr
)

hpsPFTauDiscriminationByVLooseCombinedIsolationDBSumPtCorr = hpsPFTauDiscriminationByVLooseIsolationDBSumPtCorr.clone(
    ApplyDiscriminationByTrackerIsolation = True,
    ApplyDiscriminationByECALIsolation = True,
    deltaBetaFactor = "%0.4f"%((0.09/0.25)*(0.0772/0.1687)),
    applyOccupancyCut = False,
    applySumPtCut = True,
    maximumSumPtCut = 3.0,
    Prediscriminants = requireDecayMode.clone()
)
hpsPFTauDiscriminationByVLooseCombinedIsolationDBSumPtCorr.qualityCuts.isolationQualityCuts.minTrackPt = 0.5
hpsPFTauDiscriminationByVLooseCombinedIsolationDBSumPtCorr.qualityCuts.isolationQualityCuts.minGammaEt = 0.5

hpsPFTauDiscriminationByLooseCombinedIsolationDBSumPtCorr = hpsPFTauDiscriminationByLooseIsolationDBSumPtCorr.clone(
    ApplyDiscriminationByTrackerIsolation = True,
    ApplyDiscriminationByECALIsolation = True,
    deltaBetaFactor = "%0.4f"%(0.0772/0.1687),
    applyOccupancyCut = False,
    applySumPtCut = True,
    maximumSumPtCut = 2.0,
    Prediscriminants = requireDecayMode.clone()
)
hpsPFTauDiscriminationByLooseCombinedIsolationDBSumPtCorr.qualityCuts.isolationQualityCuts.minTrackPt = 0.5
hpsPFTauDiscriminationByLooseCombinedIsolationDBSumPtCorr.qualityCuts.isolationQualityCuts.minGammaEt = 0.5

hpsPFTauDiscriminationByRelLooseCombinedIsolationDBSumPtCorr = hpsPFTauDiscriminationByLooseCombinedIsolationDBSumPtCorr.clone(
    applySumPtCut = False,
    applyRelativeSumPtCut = True,
    relativeSumPtCut = 0.09
)

hpsPFTauDiscriminationByRawCombinedIsolationDBSumPtCorr = hpsPFTauDiscriminationByLooseCombinedIsolationDBSumPtCorr.clone(
    applySumPtCut = False,
    storeRawSumPt = cms.bool(True)
)

hpsPFTauDiscriminationByRawChargedIsolationDBSumPtCorr = hpsPFTauDiscriminationByLooseCombinedIsolationDBSumPtCorr.clone(
    applySumPtCut = False,
    ApplyDiscriminationByECALIsolation = False,
    storeRawSumPt = cms.bool(True)
)

hpsPFTauDiscriminationByRawGammaIsolationDBSumPtCorr = hpsPFTauDiscriminationByLooseCombinedIsolationDBSumPtCorr.clone(
    applySumPtCut = False,
    ApplyDiscriminationByTrackerIsolation = False,
    storeRawSumPt = cms.bool(True)
)

hpsPFTauDiscriminationByMediumCombinedIsolationDBSumPtCorr = hpsPFTauDiscriminationByMediumIsolationDBSumPtCorr.clone(
    ApplyDiscriminationByTrackerIsolation = True,
    ApplyDiscriminationByECALIsolation = True,
    deltaBetaFactor = "%0.4f"%(0.0772/0.1687),
    applyOccupancyCut = False,
    applySumPtCut = True,
    maximumSumPtCut = 1.0,
    Prediscriminants = requireDecayMode.clone()
)
hpsPFTauDiscriminationByMediumCombinedIsolationDBSumPtCorr.qualityCuts.isolationQualityCuts.minTrackPt = 0.5
hpsPFTauDiscriminationByMediumCombinedIsolationDBSumPtCorr.qualityCuts.isolationQualityCuts.minGammaEt = 0.5

hpsPFTauDiscriminationByRelMediumCombinedIsolationDBSumPtCorr = hpsPFTauDiscriminationByMediumCombinedIsolationDBSumPtCorr.clone(
    applySumPtCut = False,
    applyRelativeSumPtCut = True,
    relativeSumPtCut = 0.06
)

hpsPFTauDiscriminationByTightCombinedIsolationDBSumPtCorr = hpsPFTauDiscriminationByTightIsolationDBSumPtCorr.clone(
    ApplyDiscriminationByTrackerIsolation = True,
    ApplyDiscriminationByECALIsolation = True,
    deltaBetaFactor = "%0.4f"%(0.0772/0.1687),
    applyOccupancyCut = False,
    applySumPtCut = True,
    maximumSumPtCut = 0.8,
    Prediscriminants = requireDecayMode.clone()
)
hpsPFTauDiscriminationByTightCombinedIsolationDBSumPtCorr.qualityCuts.isolationQualityCuts.minTrackPt = 0.5
hpsPFTauDiscriminationByTightCombinedIsolationDBSumPtCorr.qualityCuts.isolationQualityCuts.minGammaEt = 0.5

hpsPFTauDiscriminationByRelTightCombinedIsolationDBSumPtCorr = hpsPFTauDiscriminationByTightCombinedIsolationDBSumPtCorr.clone(
    applySumPtCut = False,
    applyRelativeSumPtCut = True,
    relativeSumPtCut = 0.03
)

hpsPFTauDiscriminationByCombinedIsolationSeqDBSumPtCorr = cms.Sequence(
    hpsPFTauDiscriminationByVLooseCombinedIsolationDBSumPtCorr*
    hpsPFTauDiscriminationByLooseCombinedIsolationDBSumPtCorr*hpsPFTauDiscriminationByRelLooseCombinedIsolationDBSumPtCorr*    
    hpsPFTauDiscriminationByMediumCombinedIsolationDBSumPtCorr*hpsPFTauDiscriminationByRelMediumCombinedIsolationDBSumPtCorr*
    hpsPFTauDiscriminationByTightCombinedIsolationDBSumPtCorr*hpsPFTauDiscriminationByRelTightCombinedIsolationDBSumPtCorr
)

#Charge isolation based on combined isolation
hpsPFTauDiscriminationByVLooseChargedIsolation = hpsPFTauDiscriminationByVLooseCombinedIsolationDBSumPtCorr.clone(
    ApplyDiscriminationByECALIsolation = False
)

hpsPFTauDiscriminationByLooseChargedIsolation = hpsPFTauDiscriminationByLooseCombinedIsolationDBSumPtCorr.clone(
    ApplyDiscriminationByECALIsolation = False
)

hpsPFTauDiscriminationByMediumChargedIsolation = hpsPFTauDiscriminationByMediumCombinedIsolationDBSumPtCorr.clone(
    ApplyDiscriminationByECALIsolation = False
)
hpsPFTauDiscriminationByTightChargedIsolation = hpsPFTauDiscriminationByTightCombinedIsolationDBSumPtCorr.clone(
    ApplyDiscriminationByECALIsolation = False
)


hpsPFTauDiscriminationByChargedIsolationSeq = cms.Sequence(
    hpsPFTauDiscriminationByVLooseChargedIsolation*
    hpsPFTauDiscriminationByLooseChargedIsolation*
    hpsPFTauDiscriminationByMediumChargedIsolation*
    hpsPFTauDiscriminationByTightChargedIsolation
)

# Define MVA based isolation discrimators
#   MVA Isolation Version 1
hpsPFTauDiscriminationByIsolationMVAraw = pfRecoTauDiscriminationByMVAIsolation.clone(
    PFTauProducer = cms.InputTag("hpsPFTauProducer"),
    Prediscriminants = requireDecayMode.clone(),
    returnMVA = cms.bool(True),
)

hpsPFTauDiscriminationByLooseIsolationMVA = hpsPFTauDiscriminationByDecayModeFinding.clone(
    Prediscriminants = cms.PSet(
        BooleanOperator = cms.string("and"),
        mva = cms.PSet(
            Producer = cms.InputTag('hpsPFTauDiscriminationByIsolationMVAraw'),
            cut = cms.double(0.795)
        )
    )
)
hpsPFTauDiscriminationByMediumIsolationMVA = copy.deepcopy(hpsPFTauDiscriminationByLooseIsolationMVA)
hpsPFTauDiscriminationByMediumIsolationMVA.Prediscriminants.mva.cut = cms.double(0.884)
hpsPFTauDiscriminationByTightIsolationMVA = copy.deepcopy(hpsPFTauDiscriminationByLooseIsolationMVA)
hpsPFTauDiscriminationByTightIsolationMVA.Prediscriminants.mva.cut = cms.double(0.921)

#   MVA Isolation Version 2
hpsPFTauDiscriminationByIsolationMVA2raw = pfRecoTauDiscriminationByMVAIsolation.clone(
    PFTauProducer = cms.InputTag("hpsPFTauProducer"),
    Prediscriminants = requireDecayMode.clone(),
    returnMVA = cms.bool(True),
    gbrfFilePath = cms.FileInPath('RecoTauTag/RecoTau/data/gbrfTauIso_v2.root')
)

hpsPFTauDiscriminationByLooseIsolationMVA2 = hpsPFTauDiscriminationByDecayModeFinding.clone(
    Prediscriminants = cms.PSet(
        BooleanOperator = cms.string("and"),
        mva = cms.PSet(
            Producer = cms.InputTag('hpsPFTauDiscriminationByIsolationMVA2raw'),
            cut = cms.double(0.85)
        )
    )
)
hpsPFTauDiscriminationByMediumIsolationMVA2 = copy.deepcopy(hpsPFTauDiscriminationByLooseIsolationMVA2)
hpsPFTauDiscriminationByMediumIsolationMVA2.Prediscriminants.mva.cut = cms.double(0.90)
hpsPFTauDiscriminationByTightIsolationMVA2 = copy.deepcopy(hpsPFTauDiscriminationByLooseIsolationMVA2)
hpsPFTauDiscriminationByTightIsolationMVA2.Prediscriminants.mva.cut = cms.double(0.94)

from RecoJets.Configuration.RecoPFJets_cff import kt6PFJets as _dummy
kt6PFJetsForRhoComputationVoronoi = _dummy.clone(
    doRhoFastjet = True,
    voronoiRfact = 0.9
)

hpsPFTauDiscriminationByMVAIsolationSeq = cms.Sequence(
    kt6PFJetsForRhoComputationVoronoi*
    hpsPFTauDiscriminationByIsolationMVAraw*
    hpsPFTauDiscriminationByLooseIsolationMVA*
    hpsPFTauDiscriminationByMediumIsolationMVA*
    hpsPFTauDiscriminationByTightIsolationMVA*
    hpsPFTauDiscriminationByIsolationMVA2raw*
    hpsPFTauDiscriminationByLooseIsolationMVA2*
    hpsPFTauDiscriminationByMediumIsolationMVA2*
    hpsPFTauDiscriminationByTightIsolationMVA2
)

#copying discriminator against electrons and muons
hpsPFTauDiscriminationByLooseElectronRejection = pfRecoTauDiscriminationAgainstElectron.clone(
    PFTauProducer = cms.InputTag('hpsPFTauProducer'),
    Prediscriminants = noPrediscriminants,
    PFElectronMVA_maxValue = cms.double(0.6)
)

hpsPFTauDiscriminationByMediumElectronRejection = pfRecoTauDiscriminationAgainstElectron.clone(
    PFTauProducer = cms.InputTag('hpsPFTauProducer'),
    Prediscriminants = noPrediscriminants,
    ApplyCut_EcalCrackCut = cms.bool(True)
)

hpsPFTauDiscriminationByTightElectronRejection = pfRecoTauDiscriminationAgainstElectron.clone(
    PFTauProducer = cms.InputTag('hpsPFTauProducer'),
    Prediscriminants = noPrediscriminants,
    ApplyCut_EcalCrackCut = cms.bool(True),
    ApplyCut_BremCombined = cms.bool(True)
)

hpsPFTauDiscriminationByLooseMuonRejection = pfRecoTauDiscriminationAgainstMuon.clone(
    PFTauProducer = cms.InputTag('hpsPFTauProducer'),
    Prediscriminants = noPrediscriminants
)

hpsPFTauDiscriminationByMediumMuonRejection = pfRecoTauDiscriminationAgainstMuon.clone(
    PFTauProducer = cms.InputTag('hpsPFTauProducer'),
    Prediscriminants = noPrediscriminants,
    discriminatorOption = cms.string('noAllArbitrated')
)

hpsPFTauDiscriminationByTightMuonRejection = pfRecoTauDiscriminationAgainstMuon.clone(
    PFTauProducer = cms.InputTag('hpsPFTauProducer'),
    Prediscriminants = noPrediscriminants,
    discriminatorOption = cms.string('noAllArbitratedWithHOP')
)

hpsPFTauDiscriminationByLooseMuonRejection2 = pfRecoTauDiscriminationAgainstMuon2.clone(
    PFTauProducer = cms.InputTag('hpsPFTauProducer'),
    Prediscriminants = noPrediscriminants
)

hpsPFTauDiscriminationByMediumMuonRejection2 = pfRecoTauDiscriminationAgainstMuon2.clone(
    PFTauProducer = cms.InputTag('hpsPFTauProducer'),
    Prediscriminants = noPrediscriminants,
    discriminatorOption = cms.string('medium')
)

hpsPFTauDiscriminationByTightMuonRejection2 = pfRecoTauDiscriminationAgainstMuon2.clone(
    PFTauProducer = cms.InputTag('hpsPFTauProducer'),
    Prediscriminants = noPrediscriminants,
    discriminatorOption = cms.string('tight')
)

hpsPFTauDiscriminationByLooseMuonRejection3 = pfRecoTauDiscriminationAgainstMuon2.clone(
    PFTauProducer = cms.InputTag('hpsPFTauProducer'),
    Prediscriminants = noPrediscriminants,
    maxNumberOfMatches = cms.int32(1)
)

hpsPFTauDiscriminationByMediumMuonRejection3 = pfRecoTauDiscriminationAgainstMuon2.clone(
    PFTauProducer = cms.InputTag('hpsPFTauProducer'),
    Prediscriminants = noPrediscriminants,
    discriminatorOption = cms.string('medium'),
    maxNumberOfMatches = cms.int32(1)
)

hpsPFTauDiscriminationByTightMuonRejection3 = pfRecoTauDiscriminationAgainstMuon2.clone(
    PFTauProducer = cms.InputTag('hpsPFTauProducer'),
    Prediscriminants = noPrediscriminants,
    discriminatorOption = cms.string('tight'),
    maxNumberOfMatches = cms.int32(1)
)

hpsPFTauDiscriminationByMVAElectronRejection = pfRecoTauDiscriminationAgainstElectronMVA.clone(
    PFTauProducer = cms.InputTag('hpsPFTauProducer'),
    Prediscriminants = requireDecayMode.clone(),
)

# Additionally require that the MVA electrons pass electron medium
# (this discriminator was used on the training sample)
hpsPFTauDiscriminationByMVAElectronRejection.Prediscriminants.electronMedium = \
    cms.PSet(
        Producer = cms.InputTag('hpsPFTauDiscriminationByMediumElectronRejection'),
        cut = cms.double(0.5)
    )

hpsPFTauDiscriminationByMVA2rawElectronRejection = pfRecoTauDiscriminationAgainstElectronMVA2.clone(
    PFTauProducer = cms.InputTag('hpsPFTauProducer'),
    Prediscriminants = requireDecayMode.clone()
)

from RecoTauTag.RecoTau.RecoTauDiscriminantCutMultiplexer_cfi import recoTauDiscriminantCutMultiplexer
hpsPFTauDiscriminationByMVA2VLooseElectronRejection = recoTauDiscriminantCutMultiplexer.clone(
    PFTauProducer = cms.InputTag('hpsPFTauProducer'),
    Prediscriminants = requireDecayMode.clone(),
    toMultiplex = cms.InputTag('hpsPFTauDiscriminationByMVA2rawElectronRejection'),
    key = cms.InputTag('hpsPFTauDiscriminationByMVA2rawElectronRejection:category'),
    mapping = cms.VPSet(
        cms.PSet(
            category = cms.uint32(0), # minMVA1prongNoEleMatchBL
            cut = cms.double(-0.141383)
        ),
        cms.PSet(
            category = cms.uint32(1), # minMVA1prongBL
            cut = cms.double(-0.122568)
        ),
        cms.PSet(
            category = cms.uint32(2), # minMVA1prongStripsWOgsfBL
            cut = cms.double(-0.138286)
        ),
        cms.PSet(
            category = cms.uint32(3), # minMVA1prongStripsWgsfWOpfEleMvaBL
            cut = cms.double(-0.100279)
        ),
        cms.PSet(
            category = cms.uint32(4), # minMVA1prongStripsWgsfWpfEleMvaBL
            cut = cms.double(-0.116113)
        ),
        cms.PSet(
            category = cms.uint32(5), # minMVA1prongNoEleMatchEC
            cut = cms.double(-0.191557)
        ),
        cms.PSet(
            category = cms.uint32(6), # minMVA1prongEC
            cut = cms.double(-0.0921955)
        ),
        cms.PSet(
            category = cms.uint32(7), # minMVA1prongStripsWOgsfEC
            cut = cms.double(-0.0936173)
        ),
        cms.PSet(
            category = cms.uint32(8), # minMVA1prongStripsWgsfWOpfEleMvaEC
            cut = cms.double(-0.119732)
        ),
        cms.PSet(
            category = cms.uint32(9), # minMVA1prongStripsWgsfWpfEleMvaEC
            cut = cms.double(-0.1042)
        )
    )
)

hpsPFTauDiscriminationByMVA2LooseElectronRejection = copy.deepcopy(hpsPFTauDiscriminationByMVA2VLooseElectronRejection)
hpsPFTauDiscriminationByMVA2LooseElectronRejection.mapping[0].cut = cms.double(-0.0639254)
hpsPFTauDiscriminationByMVA2LooseElectronRejection.mapping[1].cut = cms.double(-0.0220708)
hpsPFTauDiscriminationByMVA2LooseElectronRejection.mapping[2].cut = cms.double(-0.102071)
hpsPFTauDiscriminationByMVA2LooseElectronRejection.mapping[3].cut = cms.double(-0.0233814)
hpsPFTauDiscriminationByMVA2LooseElectronRejection.mapping[4].cut = cms.double(-0.0391565)
hpsPFTauDiscriminationByMVA2LooseElectronRejection.mapping[5].cut = cms.double(-0.142564)
hpsPFTauDiscriminationByMVA2LooseElectronRejection.mapping[6].cut = cms.double(+0.00982555)
hpsPFTauDiscriminationByMVA2LooseElectronRejection.mapping[7].cut = cms.double(-0.0596019)
hpsPFTauDiscriminationByMVA2LooseElectronRejection.mapping[8].cut = cms.double(-0.0381238)
hpsPFTauDiscriminationByMVA2LooseElectronRejection.mapping[9].cut = cms.double(-0.100381)

hpsPFTauDiscriminationByMVA2MediumElectronRejection = copy.deepcopy(hpsPFTauDiscriminationByMVA2VLooseElectronRejection)
hpsPFTauDiscriminationByMVA2MediumElectronRejection.mapping[0].cut = cms.double(+0.011729)
hpsPFTauDiscriminationByMVA2MediumElectronRejection.mapping[1].cut = cms.double(+0.0203646)
hpsPFTauDiscriminationByMVA2MediumElectronRejection.mapping[2].cut = cms.double(+0.177502)
hpsPFTauDiscriminationByMVA2MediumElectronRejection.mapping[3].cut = cms.double(+0.0103449)
hpsPFTauDiscriminationByMVA2MediumElectronRejection.mapping[4].cut = cms.double(+0.257798)
hpsPFTauDiscriminationByMVA2MediumElectronRejection.mapping[5].cut = cms.double(-0.0966083)
hpsPFTauDiscriminationByMVA2MediumElectronRejection.mapping[6].cut = cms.double(-0.0466023)
hpsPFTauDiscriminationByMVA2MediumElectronRejection.mapping[7].cut = cms.double(+0.0467638)
hpsPFTauDiscriminationByMVA2MediumElectronRejection.mapping[8].cut = cms.double(+0.0863876)
hpsPFTauDiscriminationByMVA2MediumElectronRejection.mapping[9].cut = cms.double(+0.233436)

hpsPFTauDiscriminationByMVA2TightElectronRejection = copy.deepcopy(hpsPFTauDiscriminationByMVA2VLooseElectronRejection)
hpsPFTauDiscriminationByMVA2TightElectronRejection.mapping[0].cut = cms.double(+0.0306715)
hpsPFTauDiscriminationByMVA2TightElectronRejection.mapping[1].cut = cms.double(+0.992195)
hpsPFTauDiscriminationByMVA2TightElectronRejection.mapping[2].cut = cms.double(+0.308324)
hpsPFTauDiscriminationByMVA2TightElectronRejection.mapping[3].cut = cms.double(-0.0370998)
hpsPFTauDiscriminationByMVA2TightElectronRejection.mapping[4].cut = cms.double(+0.864643)
hpsPFTauDiscriminationByMVA2TightElectronRejection.mapping[5].cut = cms.double(+0.0832094)
hpsPFTauDiscriminationByMVA2TightElectronRejection.mapping[6].cut = cms.double(+0.791665)
hpsPFTauDiscriminationByMVA2TightElectronRejection.mapping[7].cut = cms.double(+0.675537)
hpsPFTauDiscriminationByMVA2TightElectronRejection.mapping[8].cut = cms.double(+0.87047)
hpsPFTauDiscriminationByMVA2TightElectronRejection.mapping[9].cut = cms.double(+0.233711)

hpsPFTauDiscriminationByMVA3rawElectronRejection = pfRecoTauDiscriminationAgainstElectronMVA3.clone(
    PFTauProducer = cms.InputTag('hpsPFTauProducer'),
    Prediscriminants = requireDecayMode.clone()
)

hpsPFTauDiscriminationByMVA3LooseElectronRejection = recoTauDiscriminantCutMultiplexer.clone(
    PFTauProducer = cms.InputTag('hpsPFTauProducer'),
    Prediscriminants = requireDecayMode.clone(),
    toMultiplex = cms.InputTag('hpsPFTauDiscriminationByMVA3rawElectronRejection'),
    key = cms.InputTag('hpsPFTauDiscriminationByMVA3rawElectronRejection:category'),
    mapping = cms.VPSet(
        cms.PSet(
            category = cms.uint32(0), # minMVA1prongNoEleMatchWOgWOgsfBL
            cut = cms.double(0.835)
        ),
        cms.PSet(
            category = cms.uint32(1), # minMVA1prongNoEleMatchWOgWgsfBL
            cut = cms.double(0.831)
        ),
        cms.PSet(
            category = cms.uint32(2), # minMVA1prongNoEleMatchWgWOgsfBL
            cut = cms.double(0.849)
        ),
        cms.PSet(
            category = cms.uint32(3), # minMVA1prongNoEleMatchWgWgsfBL
            cut = cms.double(0.859)
        ),
         cms.PSet(
            category = cms.uint32(4), # minMVA1prongWOgWOgsfBL
            cut = cms.double(0.873)
        ),
        cms.PSet(
            category = cms.uint32(5), # minMVA1prongWOgWgsfBL
            cut = cms.double(0.823)
        ),
        cms.PSet(
            category = cms.uint32(6), # minMVA1prongWgWOgsfBL
            cut = cms.double(0.85)
        ),
        cms.PSet(
            category = cms.uint32(7), # minMVA1prongWgWgsfBL
            cut = cms.double(0.855)
        ),
        cms.PSet(
            category = cms.uint32(8), # minMVA1prongNoEleMatchWOgWOgsfEC
            cut = cms.double(0.816)
        ),
        cms.PSet(
            category = cms.uint32(9), # minMVA1prongNoEleMatchWOgWgsfEC
            cut = cms.double(0.861)
        ),
        cms.PSet(
            category = cms.uint32(10), # minMVA1prongNoEleMatchWgWOgsfEC
            cut = cms.double(0.862)
        ),
        cms.PSet(
            category = cms.uint32(11), # minMVA1prongNoEleMatchWgWgsfEC
            cut = cms.double(0.847)
        ),
         cms.PSet(
            category = cms.uint32(12), # minMVA1prongWOgWOgsfEC
            cut = cms.double(0.893)
        ),
        cms.PSet(
            category = cms.uint32(13), # minMVA1prongWOgWgsfEC
            cut = cms.double(0.82)
        ),
        cms.PSet(
            category = cms.uint32(14), # minMVA1prongWgWOgsfEC
            cut = cms.double(0.845)
        ),
        cms.PSet(
            category = cms.uint32(15), # minMVA1prongWgWgsfEC
            cut = cms.double(0.851)
        ),
        cms.PSet(
            category = cms.uint32(16), # minMVA3prongMatch
            cut = cms.double(-1.)
        ),
        cms.PSet(
            category = cms.uint32(17), # minMVA3prongNoMatch
            cut = cms.double(-1.)
        )
    )
)

hpsPFTauDiscriminationByMVA3MediumElectronRejection = copy.deepcopy(hpsPFTauDiscriminationByMVA3LooseElectronRejection)
hpsPFTauDiscriminationByMVA3MediumElectronRejection.mapping[0].cut = cms.double(0.937)
hpsPFTauDiscriminationByMVA3MediumElectronRejection.mapping[1].cut = cms.double(0.949)
hpsPFTauDiscriminationByMVA3MediumElectronRejection.mapping[2].cut = cms.double(0.955)
hpsPFTauDiscriminationByMVA3MediumElectronRejection.mapping[3].cut = cms.double(0.956)
hpsPFTauDiscriminationByMVA3MediumElectronRejection.mapping[4].cut = cms.double(0.962)
hpsPFTauDiscriminationByMVA3MediumElectronRejection.mapping[5].cut = cms.double(0.934)
hpsPFTauDiscriminationByMVA3MediumElectronRejection.mapping[6].cut = cms.double(0.946)
hpsPFTauDiscriminationByMVA3MediumElectronRejection.mapping[7].cut = cms.double(0.948)
hpsPFTauDiscriminationByMVA3MediumElectronRejection.mapping[8].cut = cms.double(0.959)
hpsPFTauDiscriminationByMVA3MediumElectronRejection.mapping[9].cut = cms.double(0.95)
hpsPFTauDiscriminationByMVA3MediumElectronRejection.mapping[10].cut = cms.double(0.954)
hpsPFTauDiscriminationByMVA3MediumElectronRejection.mapping[11].cut = cms.double(0.954)
hpsPFTauDiscriminationByMVA3MediumElectronRejection.mapping[12].cut = cms.double(0.897)
hpsPFTauDiscriminationByMVA3MediumElectronRejection.mapping[13].cut = cms.double(0.951)
hpsPFTauDiscriminationByMVA3MediumElectronRejection.mapping[14].cut = cms.double(0.948)
hpsPFTauDiscriminationByMVA3MediumElectronRejection.mapping[15].cut = cms.double(0.953)
hpsPFTauDiscriminationByMVA3MediumElectronRejection.mapping[16].cut = cms.double(-1.)
hpsPFTauDiscriminationByMVA3MediumElectronRejection.mapping[17].cut = cms.double(-1.)
 
hpsPFTauDiscriminationByMVA3TightElectronRejection = copy.deepcopy(hpsPFTauDiscriminationByMVA3LooseElectronRejection)
hpsPFTauDiscriminationByMVA3TightElectronRejection.mapping[0].cut = cms.double(0.974)
hpsPFTauDiscriminationByMVA3TightElectronRejection.mapping[1].cut = cms.double(0.976)
hpsPFTauDiscriminationByMVA3TightElectronRejection.mapping[2].cut = cms.double(0.978)
hpsPFTauDiscriminationByMVA3TightElectronRejection.mapping[3].cut = cms.double(0.978)
hpsPFTauDiscriminationByMVA3TightElectronRejection.mapping[4].cut = cms.double(0.971)
hpsPFTauDiscriminationByMVA3TightElectronRejection.mapping[5].cut = cms.double(0.969)
hpsPFTauDiscriminationByMVA3TightElectronRejection.mapping[6].cut = cms.double(0.982)
hpsPFTauDiscriminationByMVA3TightElectronRejection.mapping[7].cut = cms.double(0.972)
hpsPFTauDiscriminationByMVA3TightElectronRejection.mapping[8].cut = cms.double(0.982)
hpsPFTauDiscriminationByMVA3TightElectronRejection.mapping[9].cut = cms.double(0.977)
hpsPFTauDiscriminationByMVA3TightElectronRejection.mapping[10].cut = cms.double(0.981)
hpsPFTauDiscriminationByMVA3TightElectronRejection.mapping[11].cut = cms.double(0.978)
hpsPFTauDiscriminationByMVA3TightElectronRejection.mapping[12].cut = cms.double(0.897)
hpsPFTauDiscriminationByMVA3TightElectronRejection.mapping[13].cut = cms.double(0.976)
hpsPFTauDiscriminationByMVA3TightElectronRejection.mapping[14].cut = cms.double(0.975)
hpsPFTauDiscriminationByMVA3TightElectronRejection.mapping[15].cut = cms.double(0.977)
hpsPFTauDiscriminationByMVA3TightElectronRejection.mapping[16].cut = cms.double(-1.)
hpsPFTauDiscriminationByMVA3TightElectronRejection.mapping[17].cut = cms.double(-1.)
 
hpsPFTauDiscriminationByMVA3VTightElectronRejection = copy.deepcopy(hpsPFTauDiscriminationByMVA3LooseElectronRejection)
hpsPFTauDiscriminationByMVA3VTightElectronRejection.mapping[0].cut = cms.double(0.986)
hpsPFTauDiscriminationByMVA3VTightElectronRejection.mapping[1].cut = cms.double(0.986)
hpsPFTauDiscriminationByMVA3VTightElectronRejection.mapping[2].cut = cms.double(0.986)
hpsPFTauDiscriminationByMVA3VTightElectronRejection.mapping[3].cut = cms.double(0.99)
hpsPFTauDiscriminationByMVA3VTightElectronRejection.mapping[4].cut = cms.double(0.983)
hpsPFTauDiscriminationByMVA3VTightElectronRejection.mapping[5].cut = cms.double(0.977)
hpsPFTauDiscriminationByMVA3VTightElectronRejection.mapping[6].cut = cms.double(0.992)
hpsPFTauDiscriminationByMVA3VTightElectronRejection.mapping[7].cut = cms.double(0.981)
hpsPFTauDiscriminationByMVA3VTightElectronRejection.mapping[8].cut = cms.double(0.989)
hpsPFTauDiscriminationByMVA3VTightElectronRejection.mapping[9].cut = cms.double(0.989)
hpsPFTauDiscriminationByMVA3VTightElectronRejection.mapping[10].cut = cms.double(0.987)
hpsPFTauDiscriminationByMVA3VTightElectronRejection.mapping[11].cut = cms.double(0.987)
hpsPFTauDiscriminationByMVA3VTightElectronRejection.mapping[12].cut = cms.double(0.976)
hpsPFTauDiscriminationByMVA3VTightElectronRejection.mapping[13].cut = cms.double(0.991)
hpsPFTauDiscriminationByMVA3VTightElectronRejection.mapping[14].cut = cms.double(0.984)
hpsPFTauDiscriminationByMVA3VTightElectronRejection.mapping[15].cut = cms.double(0.986)
hpsPFTauDiscriminationByMVA3VTightElectronRejection.mapping[16].cut = cms.double(-1.)
hpsPFTauDiscriminationByMVA3VTightElectronRejection.mapping[17].cut = cms.double(-1.)
 
hpsPFTauDiscriminationByDeadECALElectronRejection = pfRecoTauDiscriminationAgainstElectronDeadECAL.clone(
    PFTauProducer = cms.InputTag('hpsPFTauProducer'),
    Prediscriminants = requireDecayMode.clone()
)

#Define new sequence that is using smaller number on hits cut
hpsPFTauDiscriminationByLooseCombinedIsolationDBSumPtCorr3Hits = hpsPFTauDiscriminationByLooseCombinedIsolationDBSumPtCorr.clone()
hpsPFTauDiscriminationByMediumCombinedIsolationDBSumPtCorr3Hits = hpsPFTauDiscriminationByMediumCombinedIsolationDBSumPtCorr.clone()
hpsPFTauDiscriminationByTightCombinedIsolationDBSumPtCorr3Hits = hpsPFTauDiscriminationByTightCombinedIsolationDBSumPtCorr.clone()

hpsPFTauDiscriminationByLooseCombinedIsolationDBSumPtCorr3Hits.qualityCuts.isolationQualityCuts.minTrackHits = cms.uint32(3)
hpsPFTauDiscriminationByMediumCombinedIsolationDBSumPtCorr3Hits.qualityCuts.isolationQualityCuts.minTrackHits = cms.uint32(3)
hpsPFTauDiscriminationByTightCombinedIsolationDBSumPtCorr3Hits.qualityCuts.isolationQualityCuts.minTrackHits = cms.uint32(3)

hpsPFTauDiscriminationByRawCombinedIsolationDBSumPtCorr3Hits = hpsPFTauDiscriminationByLooseCombinedIsolationDBSumPtCorr3Hits.clone(
    applySumPtCut = False,
    storeRawSumPt = cms.bool(True)
)

hpsPFTauDiscriminationByCombinedIsolationSeqDBSumPtCorr3Hits = cms.Sequence(
    hpsPFTauDiscriminationByLooseCombinedIsolationDBSumPtCorr3Hits*
    hpsPFTauDiscriminationByMediumCombinedIsolationDBSumPtCorr3Hits*
    hpsPFTauDiscriminationByTightCombinedIsolationDBSumPtCorr3Hits*
    hpsPFTauDiscriminationByRawCombinedIsolationDBSumPtCorr3Hits
)

# Define the HPS selection discriminator used in cleaning
hpsSelectionDiscriminator.PFTauProducer = cms.InputTag("combinatoricRecoTaus")

import RecoTauTag.RecoTau.RecoTauCleanerPlugins as cleaners

hpsPFTauProducerSansRefs = cms.EDProducer(
    "RecoTauCleaner",
    src = cms.InputTag("combinatoricRecoTaus"),
    cleaners = cms.VPSet(
        # Reject taus that have charge == 3
        cleaners.unitCharge,
         # Ignore taus reconstructed in pi0 decay modes in which the highest Pt ("leading") pi0 has pt below 2.5 GeV
         # (in order to make decay mode reconstruction less sensitive to pile-up)
         # NOTE: strips are sorted by decreasing pt
        cms.PSet(
            name = cms.string("leadStripPtLt2_5"),
            plugin = cms.string("RecoTauStringCleanerPlugin"),
            selection = cms.string("signalPiZeroCandidates().size() = 0 | signalPiZeroCandidates().at(0).pt() > 2.5"),
            selectionPassFunction = cms.string("0"),
            selectionFailValue = cms.double(1e3)
        ),
        # Reject taus that are not within DR<0.1 of the jet axis
        #cleaners.matchingConeCut,
        # Reject taus that fail HPS selections
        cms.PSet(
            name = cms.string("HPS_Select"),
            plugin = cms.string("RecoTauDiscriminantCleanerPlugin"),
            src = cms.InputTag("hpsSelectionDiscriminator"),
        ),
        # CV: Take highes pT tau (use for testing of new high pT tau reconstruction and check if it can become the new default)
        cleaners.pt,
        # CV: in case two candidates have the same Pt,
        #     prefer candidates in which PFGammas are part of strips (rather than being merged with PFRecoTauChargedHadrons)
        cleaners.stripMultiplicity,
        # Take most isolated tau
        cleaners.combinedIsolation
    )
)

hpsPFTauProducer = cms.EDProducer(
    "RecoTauPiZeroUnembedder",
    src = cms.InputTag("hpsPFTauProducerSansRefs")
)

from RecoTauTag.RecoTau.PFTauPrimaryVertexProducer_cfi      import *
from RecoTauTag.RecoTau.PFTauSecondaryVertexProducer_cfi    import *
from RecoTauTag.RecoTau.PFTauTransverseImpactParameters_cfi import *
hpsPFTauPrimaryVertexProducer = PFTauPrimaryVertexProducer.clone(
    PFTauTag = cms.InputTag("hpsPFTauProducer"),
    ElectronTag = cms.InputTag(""),
    MuonTag = cms.InputTag(""),
    PVTag = cms.InputTag("offlinePrimaryVertices"),
    beamSpot = cms.InputTag("offlineBeamSpot"),
    TrackCollectionTag = cms.InputTag("generalTracks"),
    Algorithm = cms.int32(1),
    useBeamSpot = cms.bool(True),
    RemoveMuonTracks = cms.bool(False),
    RemoveElectronTracks = cms.bool(False),
    useSelectedTaus = cms.bool(False),
    discriminators = cms.VPSet(
        cms.PSet(
            discriminator = cms.InputTag('hpsPFTauDiscriminationByDecayModeFinding'),
            selectionCut = cms.double(0.5)
        )
    ),
    cut = cms.string("pt > 18.0 & abs(eta) < 2.4")
)

hpsPFTauSecondaryVertexProducer = PFTauSecondaryVertexProducer.clone(
    PFTauTag = cms.InputTag("hpsPFTauProducer")
    )
hpsPFTauTransverseImpactParameters = PFTauTransverseImpactParameters.clone(
    PFTauTag = cms.InputTag("hpsPFTauProducer"),
    PFTauPVATag = cms.InputTag("hpsPFTauPrimaryVertexProducer"),
    PFTauSVATag = cms.InputTag("hpsPFTauSecondaryVertexProducer"),
    useFullCalculation = cms.bool(False)
    )
hpsPFTauVertexAndImpactParametersSeq = cms.Sequence(
    hpsPFTauPrimaryVertexProducer*
    hpsPFTauSecondaryVertexProducer*
    hpsPFTauTransverseImpactParameters
    )

produceHPSPFTaus = cms.Sequence(
    hpsSelectionDiscriminator
    #*hpsTightIsolationCleaner
    #*hpsMediumIsolationCleaner
    #*hpsLooseIsolationCleaner
    #*hpsVLooseIsolationCleaner
    *hpsPFTauProducerSansRefs
    *hpsPFTauProducer
)

produceAndDiscriminateHPSPFTaus = cms.Sequence(
    produceHPSPFTaus*
    hpsPFTauDiscriminationByDecayModeFinding*
    hpsPFTauDiscriminationByChargedIsolationSeq*
    hpsPFTauDiscriminationByIsolationSeq*
    #hpsPFTauDiscriminationByIsolationSeqRhoCorr*
    #hpsPFTauDiscriminationByIsolationSeqCustomRhoCorr*
    hpsPFTauDiscriminationByIsolationSeqDBSumPtCorr*
    hpsPFTauDiscriminationByMVAIsolationSeq*

    hpsPFTauDiscriminationByRawCombinedIsolationDBSumPtCorr*
    hpsPFTauDiscriminationByRawChargedIsolationDBSumPtCorr*
    hpsPFTauDiscriminationByRawGammaIsolationDBSumPtCorr*

    hpsPFTauDiscriminationByCombinedIsolationSeqDBSumPtCorr*
    hpsPFTauDiscriminationByCombinedIsolationSeqDBSumPtCorr3Hits*
    
    hpsPFTauDiscriminationByLooseElectronRejection*
    hpsPFTauDiscriminationByMediumElectronRejection*
    hpsPFTauDiscriminationByTightElectronRejection*
    hpsPFTauDiscriminationByMVAElectronRejection*
    hpsPFTauDiscriminationByMVA2rawElectronRejection*
    hpsPFTauDiscriminationByMVA2VLooseElectronRejection*
    hpsPFTauDiscriminationByMVA2LooseElectronRejection*
    hpsPFTauDiscriminationByMVA2MediumElectronRejection*
    hpsPFTauDiscriminationByMVA2TightElectronRejection*
    hpsPFTauDiscriminationByMVA3rawElectronRejection*
    hpsPFTauDiscriminationByMVA3LooseElectronRejection*
    hpsPFTauDiscriminationByMVA3MediumElectronRejection*
    hpsPFTauDiscriminationByMVA3TightElectronRejection*
    hpsPFTauDiscriminationByMVA3VTightElectronRejection*
    hpsPFTauDiscriminationByDeadECALElectronRejection*
    hpsPFTauDiscriminationByLooseMuonRejection*
    hpsPFTauDiscriminationByMediumMuonRejection*
    hpsPFTauDiscriminationByTightMuonRejection*
    hpsPFTauDiscriminationByLooseMuonRejection2*
    hpsPFTauDiscriminationByMediumMuonRejection2*
    hpsPFTauDiscriminationByTightMuonRejection2*
    hpsPFTauDiscriminationByLooseMuonRejection3*
    hpsPFTauDiscriminationByMediumMuonRejection3*
    hpsPFTauDiscriminationByTightMuonRejection3*

    hpsPFTauVertexAndImpactParametersSeq
)
