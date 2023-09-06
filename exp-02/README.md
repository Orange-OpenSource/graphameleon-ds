# Experiment 02

This folder contains the graphameleon-ds documents in relation to the *Navigation trace classification* experiment.

## Workbench settings

Here is a summary of the settings for the experiment:

* Graphameleon 2.1.0
  - Collect mode: Micro
  - General output format: Semantize
  - Export format: Turtle syntax

* Firefox Browser 116.0.2 (64 bits) - Mozilla Firefox for Ubuntu

## Data capture and analysis

Data file names follow the naming convention:

```
# Canonical form
GPL_<NavigationScenarioName>.ttl

# Example
GPL_attack_scenario.ttl
```

The *NavigationScenarioName* field refers to:

* **Base scenario (normal behavior)**: a user accesses the website, logs in to their account using their username and password, navigates to the "Sell a Book" page, fills out the form, and then returns to the homepage where they find their book.
* **Alternative scenario (different behavior)**: a user accesses the website, logs in to their account using Single Sign-On (SSO), navigates to the "Sell a Book" page, fills out the form, and then returns to the homepage where they find their book.
* **XSS attack scenario (abnormal behavior)**: an attacker accesses the website, logs in to their account using their username and password, navigates to the "Sell a Book" page, and performs a code injection in the "Author" field. Finally, they return to the homepage where the injected script is executed.
