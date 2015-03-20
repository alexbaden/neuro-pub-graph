ns = "Neuroscience"
no = "Neurology"
pb = "Psychological and Brain Sciences"
bme = "Biomedical Engineering"
bio = "Biology"
cs = "Computer Science"
ece = "Electrical Engineering"
mb = "Molecular Biology"
pc = "Pharmacology"
ro = "Radiology"
cbe = "Chemical and Biomolecular Engineering"
ams = "Applied Mathematics and Statistics"
phy = "Physics"
apl = "Applied Physics Laboratory"
bs = "Biostatistics"
mse = "Materials Science & Engineering"
depts <- c(ns, bme, bs, no, bs, phy, ns, bme, ns, ns, ns, cbe, cs, ams, bme, ns, bio, ro,ns, ns, ns, bme, pb, bme, mse, ns, ams, pc, bme, ns, bs, bme, ams, pb, ns, apl, no, bme, ece, pb, cs, cs, bme, ams, ro, mb, cbe)

library("igraph")
gg = read.graph('jhu_neuro.graphml', format=c("graphml"))
V(gg)$dept <- depts

V(gg)$color=V(gg)$dept
V(gg)$color=gsub(ns, "indianred2", V(gg)$color)
V(gg)$color=gsub(no, "lightslateblue", V(gg)$color)
V(gg)$color=gsub(pb, "royalblue", V(gg)$color)
V(gg)$color=gsub(bme, "powderblue", V(gg)$color)
V(gg)$color=gsub(mb, "orchid", V(gg)$color)
V(gg)$color=gsub(bio, "seagreen", V(gg)$color)
V(gg)$color=gsub(cs, "aquamarine", V(gg)$color)
V(gg)$color=gsub(ece, "pink2", V(gg)$color)
V(gg)$color=gsub(pc, "lightsteelblue", V(gg)$color)
V(gg)$color=gsub(ro, "lightpink", V(gg)$color)
V(gg)$color=gsub(cbe, "khaki1", V(gg)$color)
V(gg)$color=gsub(ams, "lawngreen", V(gg)$color)
V(gg)$color=gsub(apl, "magenta3", V(gg)$color)
V(gg)$color=gsub(phy, "lightseagreen", V(gg)$color)
V(gg)$color=gsub(bs, "orange2", V(gg)$color)
V(gg)$color=gsub(mse, "wheat1", V(gg)$color)

tkplot(gg, edge.width=ceiling(log(E(gg)$weight)), layout=layout.fruchterman.reingold)
png(filename="/Users/gkiar/git/neuro-pub-graph/graphs/org_network.png", height=800, width=600)
