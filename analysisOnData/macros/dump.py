import os

files = os.listdir('/scratchssd/sroychow/NanoAOD2016-V1MCFinal/')
filesQCD = []
for f in files:
    if 'QCD' not in f: continue
    filesQCD.append(f)
filesQCD.sort(key=lambda f: float((f.split('-')[1]).split('to')[0]), reverse=False )
xsec = open('../../PhysicsTools/NanoAODTools/crab/mcsamples_2016.txt', 'r')
xsec_lines = xsec.readlines()
out = open('dump.txt', 'w')
for f in filesQCD:
    if 'QCD' not in f: continue
    out.write("\""+f+"\": {\n")
    out.write("\"dirs\" : {\n")
    out.write("\""+f+"\": [\"tree\"],\n")
    out.write("\""+f+"\": [\"tree\"]\n")
    out.write("},\n")
    out.write("\"dataType\" :\"MC\",\n")
    xsec = ""
    for l in xsec_lines:
        l = l.strip('\n')
        if f in l or f.rstrip('_ext1') in l or f.rstrip('_ext2') in l: 
            xsec = l.split(',')[-1]
    out.write("\"xsec\" : "+xsec+",\n")
    out.write("\"ncores\" : -1,\n")
    out.write("\"categories\" : \"SIGNAL:nominal,SIDEBAND:nominal,QCD:nominal,AISO:nominal,SIGNALNORM:nominal,AISONORM:nominal,SIGNALNOISOSF:nominal\"\n")
    out.write("}\n")
out.close()
