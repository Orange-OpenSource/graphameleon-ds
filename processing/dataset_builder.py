from rdflib import Graph, Literal
import re

query = """
PREFIX ucoact: <https://ontology.unifiedcyberontology.org/uco/action#>
PREFIX ucobs: <https://ontology.unifiedcyberontology.org/uco/observable#>
PREFIX core: <https://ontology.unifiedcyberontology.org/uco/core#>

SELECT DISTINCT ?actionTag ?object ?page
WHERE {
    ?action a ucoact:ObservableAction ;
            core:tag ?actionTag .
    ?action core:value ?object .
    {
        ?action ucobs:location ?location .
        ?location a ucobs:URLFacet ;
                  ucobs:fullValue ?page .
    }
    UNION
    {
        ?action core:tag "request" ;
                ucobs:object ?httpConnection .
        ?httpConnection a ucobs:HTTPConnectionFacet ;
                         ucobs:hasFacet ?urlFacet .
        ?urlFacet a ucobs:URLFacet ;
                   ucobs:fullValue ?page .
    }
}
"""

def slugify(value):
    value = str(value)
    value = value.lower()
    value = re.sub(r'[^\w\s-]', '', value)
    value = re.sub(r'[\s]+', '-', value)
    return value.strip('-')

files = ['GPL_attack_scenario.ttl','GPL_alternative_scenario.ttl','GPL_normal_scenario.ttl']

# Dictionary to store mappings for shorter variable names
action_map = {}
page_map = {}
object_map = {}
action_counter = 1
page_counter = 1
object_counter = 1

for f in files:
    g = Graph()
    g.parse(f, format='turtle')
    results = g.query(query)
    appreciation = Literal(f"{f.split('.')[0]}")
    with open(f"output_{f}", "w") as out_file:
        for row in results:
            action_slug = slugify(row.actionTag)
            page_slug = slugify(row.page)
            object_slug = slugify(row.object)
            appreciation_slug = slugify(appreciation)
            # Create shorter variable names for actions
            if action_slug not in action_map:
                action_map[action_slug] = f"A{action_counter}"
                action_counter += 1
            action_var = action_map[action_slug]
            # Create shorter variable names for pages
            if page_slug not in page_map:
                page_map[page_slug] = f"P{page_counter}"
                page_counter += 1
            page_var = page_map[page_slug]
            # Create shorter variable names for objects
            if object_slug not in object_map:
                object_map[object_slug] = f"O{object_counter}"
                object_counter += 1
            object_var = object_map[object_slug]
            out_file.write(f"{action_var} {page_var} {object_var} {appreciation_slug} \n")

# Write mapping files for reference
with open("action_mapping.txt", "w") as f:
    for original, variable in action_map.items():
        f.write(f"{variable}: {original}\n")
with open("page_mapping.txt", "w") as f:
    for original, variable in page_map.items():
        f.write(f"{variable}: {original}\n")
with open("object_mapping.txt", "w") as f:
    for original, variable in object_map.items():
        f.write(f"{variable}: {original}\n")