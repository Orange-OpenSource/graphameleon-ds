from rdflib import Graph, Literal
import re
from datetime import datetime
from dateutil.parser import isoparse

query = """
PREFIX ucoact: <https://ontology.unifiedcyberontology.org/uco/action#>
PREFIX ucobs: <https://ontology.unifiedcyberontology.org/uco/observable#>
PREFIX core: <https://ontology.unifiedcyberontology.org/uco/core#>
PREFIX types: <https://ontology.unifiedcyberontology.org/uco/types#>

SELECT DISTINCT ?action ?actionTag ?object ?page ?actionTime
WHERE {
    ?action a ucoact:ObservableAction ;
            core:tag ?actionTag ;
            core:objectCreatedTime ?actionTime .
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
ORDER BY ?actionTime
"""

def slugify(value):
    value = str(value)
    value = value.lower()
    value = re.sub(r'[^\w\s-]', '', value)
    value = re.sub(r'[\s]+', '-', value)
    return value.strip('-')

def calculate_temporal_delta(action_time_str, previous_action_time_str):
    """Calculate temporal delta in seconds between two actions based on their core:objectCreatedTime"""
    if not previous_action_time_str or not action_time_str:
        return 0.0
    try:
        current_time = isoparse(str(action_time_str))
        previous_time = isoparse(str(previous_action_time_str))
        delta = current_time - previous_time
        # Return delta in seconds with millisecond precision
        return round(delta.total_seconds(), 3)  
    except:
        return 0.0

def discretize_temporal_deltas(deltas):
    """Discretize temporal deltas based on percentiles: 0-33% = low, 33-66% = medium, 66-100% = high"""
    import numpy as np
    if not deltas:
        return []
    # Calculate percentiles
    p33 = np.percentile(deltas, 33.33)
    p66 = np.percentile(deltas, 66.66)
    discretized = []
    for delta in deltas:
        if delta <= p33:
            discretized.append("low")
        elif delta <= p66:
            discretized.append("medium")
        else:
            discretized.append("high")
    
    return discretized

files = ['GPL_attack_scenario.ttl','GPL_alternative_scenario.ttl','GPL_normal_scenario.ttl']

# Dictionary to store mappings for shorter variable names
action_map = {}
tag_map = {}
page_map = {}
object_map = {}
appreciation_map = {}
action_counter = 1
tag_counter = 1
page_counter = 1
object_counter = 1
appreciation_counter = 1

for f in files:
    g = Graph()
    g.parse(f, format='turtle')
    results = list(g.query(query))  
    appreciation = Literal(f"{f.split('.')[0]}")
    
    # First pass: collect all temporal deltas for discretization
    temporal_deltas = []
    previous_action_time = None
    for i, row in enumerate(results):
        if i > 0:  # Skip first action as it has no previous action
            temporal_delta = calculate_temporal_delta(row.actionTime, previous_action_time)
            temporal_deltas.append(temporal_delta)
        previous_action_time = row.actionTime
    
    # Discretize temporal deltas
    discretized_deltas = discretize_temporal_deltas(temporal_deltas)
    
    # Second pass: write output files

    # Debug version without mapping and slugification
    with open(f"debug_raw_{f}", "w") as debug_file:
        previous_action_time = None
        for i, row in enumerate(results):
            # Get actual temporal delta value (0 for first action)
            if i == 0:
                temporal_delta_value = 0.0
            else:
                temporal_delta_value = calculate_temporal_delta(row.actionTime, previous_action_time)
            # Write raw values without mapping
            debug_file.write(f"{row.page} {row.object} {row.action} {temporal_delta_value} {appreciation}\n")
            previous_action_time = row.actionTime
    
    # Production version with mapping and slugification
    with open(f"output_{f}", "w") as out_file:
        previous_action_time = None
        delta_index = 0
        for i, row in enumerate(results):
            action_slug = slugify(row.action)
            tag_slug = slugify(row.actionTag)
            page_slug = slugify(row.page)
            object_slug = slugify(row.object)
            appreciation_slug = slugify(appreciation)
            # Get discretized temporal delta (0 for first action)
            if i == 0:
                temporal_delta_discretised = "none"
            else:
                temporal_delta_discretised = discretized_deltas[delta_index]
                delta_index += 1
            # Create shorter variable names for actions
            if action_slug not in action_map:
                action_map[action_slug] = f"A{action_counter}"
                action_counter += 1
            action_var = action_map[action_slug]
            # Create shorter variable names for tags
            if tag_slug not in tag_map:
                tag_map[tag_slug] = f"T{tag_counter}"
                tag_counter += 1
            tag_var = tag_map[tag_slug]
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
            # Create shorter variable names for appreciations
            if appreciation_slug not in appreciation_map:
                appreciation_map[appreciation_slug] = f"R{appreciation_counter}"
                appreciation_counter += 1
            appreciation_var = appreciation_map[appreciation_slug]
            out_file.write(f"{page_var} {object_var} {action_var} {temporal_delta_discretised} {appreciation_var}\n")
            previous_action_time = row.actionTime

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
