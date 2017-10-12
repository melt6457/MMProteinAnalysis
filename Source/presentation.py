import ProteinAnalyzer as pa
import fileManager as files
import matplotlib.pyplot as plt

print('End of Summer Presentation Files')

simNames = pa.selectMultipleSimulations()
simNames2 = pa.selectMultipleSimulations()
sims = []
sims2 = []

for count in range(0, len(simNames)):
    fileSet = files.getSimulationFiles(simNames[count])
    sim1 = pa.createSimAnalysis(fileSet)
    sim1.loadLog()
    sim1.loadRMSD()
    sims.append(sim1)

for count in range(1, len(simNames)):
    sims[0].combine(sims[count])


# sims[0].rmsd.calculateFrameTimes(0, sims[0].log.getEndTime() - sims[0].log.getStartTime())
plt.plot(sims[0].log.times, sims[0].log.pot_energy)

for count in range(0, len(simNames2)):
    fileSet2 = files.getSimulationFiles(simNames2[count])
    sim2 = pa.createSimAnalysis(fileSet2)
    sim2.loadLog()
    sim2.loadRMSD()
    sims2.append(sim2)

for num in range(1, len(simNames2)):
    sims2[0].combine(sims2[num])

# sims2[0].rmsd.calculateFrameTimes(0, sims2[0].log.getEndTime() - sims2[0].log.getStartTime())
# plt.plot(sims2[0].rmsd.times, sims2[0].rmsd.RMSDs)
plt.plot(sims2[0].log.times, sims2[0].log.pot_energy)

plt.show()