# Luci/Utils/rxnorm.py
import requests

class RxNorm:
    def __init__(self):
        self.base_url = "https://rxnav.nlm.nih.gov/REST/drugs.json"
        self.spelling_url = "https://rxnav.nlm.nih.gov/REST/spellingsuggestions.json"
        self.rxterm_url = "https://rxnav.nlm.nih.gov/REST/RxTerms/rxcui"

    def fetch_drug_info(self, query):
        response = requests.get(f"{self.base_url}?name={query}")
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to fetch data from RxNorm API")

    def get_section(self, query, *fields, return_format="list"):
        """
        Retrieves the specified fields from the RxNorm API data.
        
        Parameters:
        - query (str): The drug name to search.
        - fields (str): Fields to extract (e.g., 'rxcui', 'synonym').
        - return_format (str): "list" for simple value output, "json" for JSON output.
        
        Returns:
        - list: A list of values or a JSON structure based on `return_format`.
        """
        data = self.fetch_drug_info(query).get("drugGroup", {})
        concept_groups = data.get("conceptGroup", [])
        
        results = []
        
        # Loop through each concept group and extract 'conceptProperties'
        for concept_group in concept_groups:
            if 'conceptProperties' in concept_group:
                for concept in concept_group['conceptProperties']:
                    # Extract only the specified fields
                    result = {field: concept[field] for field in fields if field in concept}
                    
                    # Store results according to the specified return format
                    if return_format == "json":
                        results.append(result)
                    else:
                        # Output in list format
                        for field in fields:
                            if field in result:
                                results.append(result[field])
        
        return results
    
    def get_spelling_suggestions(self, query, return_format="list"):
        """
        Fetch spelling suggestions for a given query from the RxNorm API.

        Parameters:
        - query (str): The term to check for spelling suggestions.
        - return_format (str): "list" for simple suggestions, "json" for the full JSON response.

        Returns:
        - list: A list of spelling suggestions or
        - dict: JSON response if return_format is set to "json".
        """
        response = requests.get(f"{self.spelling_url}?name={query}")
        if response.status_code == 200:
            data = response.json()
            
            if return_format == "json":
                data = response.json()
            # Extract only the suggestion list
                suggestions = data.get("suggestionGroup", {}).get("suggestionList", {}).get("suggestion", [])
                return {"suggestion": suggestions[0]} if suggestions else {"suggestion": None}
            
            suggestions = data.get("suggestionGroup", {}).get("suggestionList", {}).get("suggestion", [])
            return suggestions
        else:
            raise Exception("Failed to fetch spelling suggestions from RxNorm API")
    
    def get_rxterm_display_name(self, rxcui, return_format="string"):
        """
        Fetch the RxTerm display name for a given rxcui.

        Parameters:
        - rxcui (int or str): The rxcui number to retrieve the display name for.
        - return_format (str): "string" for plain text output, "json" for JSON output.

        Returns:
        - str: The display name as a string, or
        - dict: JSON response containing {"displayName": "value"}.
        """
        response = requests.get(f"{self.rxterm_url}/{rxcui}/name.json")
        if response.status_code == 200:
            data = response.json()
            display_name = data.get("displayGroup", {}).get("displayName", None)

            if return_format == "json":
                return {"displayName": display_name} if display_name else {"displayName": None}
            else:
                return display_name if display_name else "No display name found"
        else:
            raise Exception("Failed to fetch display name from RxTerms API")

    def get_rxterm_all_info(self, rxcui, *fields, return_format="list"):
        """
        Fetch all RxTerm information for a given rxcui.

        Parameters:
        - rxcui (int or str): The rxcui number to retrieve the information for.
        - fields (str): The fields to extract (e.g., "displayName", "fullGenericName").
        - return_format (str): "list" for plain text values, "json" for JSON output.

        Returns:
        - list/str: The values of the specified fields, or
        - dict: JSON response containing the specified fields.
        """
        response = requests.get(f"{self.rxterm_url}/{rxcui}/allinfo.json")
        if response.status_code == 200:
            data = response.json()
            rxterms_properties = data.get("rxtermsProperties", {})

            if return_format == "json":
                # Return only the specified fields as a JSON response
                return {field: rxterms_properties[field] for field in fields if field in rxterms_properties}

            # Return only the values of specified fields
            return [rxterms_properties[field] for field in fields if field in rxterms_properties]
        else:
            raise Exception("Failed to fetch all info from RxTerms API")   

