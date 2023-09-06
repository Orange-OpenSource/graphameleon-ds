# graphameleon-ds

*graphameleon-ds*: a RDF dataset for process mining on Web navigation traces.

The following dataset was built using the *[Graphameleon](https://github.com/Orange-OpenSource/graphameleon)* Web extension,
an open-source plug-in that captures Web navigation traces and transforms them into a [RDF](https://www.w3.org/RDF/) graph for further exploration
(eg., process-mining of navigation traces, Web browser and server behavior analysis, network topology analysis).

The RDF dataset implements the concepts of *micro-activity* and
*macro-activity* (see below) on the basis of the [UCO](https://unifiedcyberontology.org/) (Unified Cyber Ontology)
vocabulary for the semantic representation of user activities.
UCO is a popular community-developed ontology built around the
cyber security domain, covering a wide range of important concepts
such as agents, resources, or actions. Since UCO is also used in
[NORIA-O](https://w3id.org/noria/), an ontology enabling to describe a IT network,
one could establish meaningful connections and access additional
contextual information within a knowledge graph combining Graphameleon data and network topology data.

## Usage

The data in the sub-folders are describing:

* **[exp-01](exp-01)**: 
RDF triples generated by Graphameleon during the initial connection to a set of websites.
We refer to this data as the "*Website complexity clustering*" experiment in which we sought to understand to what 
extent the behavior of a website during a first connection is crucial in creating a usable footprint subsequently 
for anomaly detection.

* **[exp-02](exp-02)**:
RDF triples generated by Graphameleon during three pre-defined Web navigation scenarios on a simulated online bookstore website.
We refer to this data as the "*Navigation trace classification*" experiment in which we sought to classify the Web navigation 
traces as either normal or abnormal behaviors.

The typical use of the provided data corresponds to:

* Cloning the repository to your computer,
* Query the data with SPARQL queries (eg., using the [Apache Jena](https://jena.apache.org) CLI toolset),
* Analyse the user activities with higher-level tools (eg., using the [PM4Py](https://pm4py.fit.fraunhofer.de) Python package).

## Semantic Modeling of User Activity

Semantic representation of a macro-activity:

![gpl_mapping_macro.png](img%2Fgpl_mapping_macro.png)

Semantic representation of a micro-activity:

![gpl_mapping_micro.png](img%2Fgpl_mapping_micro.png)

## Citation

If you use this dataset in a scientific publication, please cite:

> Benjamin Stach, Lionel Tailhardat, Yoan Chabot, and Raphaël Troncy. 2023.
> Web Navigation Capture for Anomaly Detection: a Web Browser-Level Approach Leveraging Knowledge Graphs.

BibTex format:

```bibtex
@inproceedings{graphemeleon-2023,
  title = {{Graphameleon: Relational Learning and Anomaly Detection on Web Navigation Traces Captured as Knowledge Graphs}},
  author = {{Benjamin Stach} and {Lionel Tailhardat} and {Yoan Chabot} and {Rapha\"el Troncy}},
  year = {2023}
}
```

## Copyright

Copyright (c) 2023, Orange. All rights reserved.

## License

[CC-BY-NC-SA](LICENSE.txt)

## Maintainer

* [Benjamin STACH](mailto:benjaminstach.pro@gmail.com)
* [Lionel TAILHARDAT](mailto:lionel.tailhardat@orange.com)
* [Yoan CHABOT](mailto:yoan.chabot@orange.com)
* [Raphaël TRONCY](mailto:raphael.troncy@eurecom.fr)
