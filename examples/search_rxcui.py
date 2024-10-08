from Luci.Utils.rxnorm import RxNorm

rxnorm = RxNorm()

# Get the RxTerm display name for the rxcui "198440"
display_name = rxnorm.get_rxterm_display_name(1101555)
print(display_name)
