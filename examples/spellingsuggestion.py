from Luci.Utils.rxnorm import RxNorm

rxnorm = RxNorm()

# Get spelling suggestions as a list for the term "paracetemo"
json_response = rxnorm.get_spelling_suggestions("pantopraz", return_format="json")
print(json_response)

#Get spelling suggestions as a list
suggestions = rxnorm.get_spelling_suggestions("pantopraz")
for suggestion in suggestions:
        print(f"{suggestion}")
