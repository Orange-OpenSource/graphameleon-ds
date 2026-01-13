# Processing

This folder holds scripts for complementary optional analysis of the Graphameleon dataset.

## Inter-arrival times

### Per trace

Run the [interarrival.py](./interarrival.py) script to compute inter-arrival times from Graphameleon traces, and discretize these times according to the .33 and .66 percentiles for each trace file:

```shell
# Install pre-requisites
pip3 install -r ./requirements.txt

# Run the script
python3 interarrival.py

# Browse results (example for the GPL_normal_scenario.ttl dataset)
cat output_oct_interarrival_GPL_normal_scenario.ttl.csv

# Number of traces discretized as "low" using grep
grep -o 'low' ./output_oct_interarrival_GPL_normal_scenario.ttl.csv | wc -l

# Statistics on traces using csvkit (https://csvkit.readthedocs.io/)
csvstat ./output_oct_interarrival_GPL_normal_scenario.ttl.csv
```

### Global 

Complementarily, run the [percentiles_global.py](percentiles_global.py) to discretize the inter-arrival times according to the percentiles over the concatenation of the whole set of trace files:

```shell
# Run the script
python3 percentiles_global.py

# Browse results
cat output_interarrival_global.csv

# Number of traces discretized as "low" for a given source using grep
grep -o 'output_oct_interarrival_GPL_normal_scenario.ttl.csv,low' ./output_interarrival_global.csv | wc -l

# Statistics on traces using csvkit (https://csvkit.readthedocs.io/)
csvstat ./output_interarrival_global.csv
```

### Results

| data source                            | analysis file                                              | inter-arrival times | low_threshold | high_threshold | low | medium | high |
|----------------------------------------|------------------------------------------------------------|---------------------|---------------|----------------|-----|--------|------|
| ../exp-02/GPL_normal_scenario.ttl      | ./output_oct_interarrival_GPL_normal_scenario.ttl.csv      | 26                  | 0.06575       | 1.9895         | 9   | 9      | 8    |
| ../exp-02/GPL_attack_scenario.ttl      | ./output_oct_interarrival_GPL_attack_scenario.ttl.csv      | 27                  | 0.08732       | 1.71988        | 9   | 9      | 9    |
| ../exp-02/GPL_alternative_scenario.ttl | ./output_oct_interarrival_GPL_alternative_scenario.ttl.csv | 25                  | 0.03968       | 1.55124        | 9   | 8      | 8    |
| Global                                 | ./output_interarrival_global.csv                           | 78                  | 0.06597       | 1.64356        | 27  | 26     | 25   |
|                                        |                                                            |                     |               | Normal         | 9   | 7      | 10   |
|                                        |                                                            |                     |               | Attack         | 8   | 10     | 9    |
|                                        |                                                            |                     |               | Alternative    | 9   | 8      | 8    |

## ABIT dataset builder

TBC.

