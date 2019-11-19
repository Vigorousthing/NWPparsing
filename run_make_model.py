# maker1 = VppTraining(LdapsFile, "unis",
#                     [2019102400, 2019102406], ["P31S2105", "P31S51157"],
#                     ["NDNSW"])
# maker2 = JenonTraining(RdapsFile, "unis", [2019080100, 2019093023],
#                        ["NDNSW", "XGWSS", "YGWSS", "LLRIB", "HFSFC",
#                         "TMOFS", "SHFO", "SUBS", "TMP", "TMIN",
#                         "TMAX", "UCAPE", "UPCIN", "LCDC", "MCDC",
#                         "HCDC", "TCAR", "TCAM", "TMP-SFC", "PRES"])

# maker1.create_nwp_checkpoint("ldaps_checkpoint")
# maker2.create_nwp_checkpoint("rdaps_checkpoint09")

# df = maker1.create_training_data_ldaps("ldaps_checkpoint")
# lists = maker2.create_training_data_rdaps("rdaps_checkpoint0809")

# modelob = RdapsModelObject(lists[0], lists[1])
# modelob.create_new_model("rdaps.h5", 30)