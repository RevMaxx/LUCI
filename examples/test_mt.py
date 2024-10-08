from Luci.Utils.rxnorm import RxNorm

rxnorm = RxNorm()

# Fetch only 'rxcui' values for 'cymbalta'
rxcui_values = rxnorm.get_section("Paracetamol", "rxcui", "synonym", return_format="json")
for value in rxcui_values:
    print(value)
