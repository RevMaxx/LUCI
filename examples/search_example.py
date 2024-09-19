from Luci import Search

query = "Revmaxx LLC"
search_instance = Search(query)

results = search_instance.search_text(max_results=5)
search_instance.print_text_result(results)
