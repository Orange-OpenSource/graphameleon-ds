#  Copyright (c) 2022-2026 Orange. All rights reserved in accordance to the CC-BY-NC-SA license
#  Project: graphameleon-ds
#  THIS SOFTWARE IS PROVIDED BY Orange "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL Orange BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""graphameleon-ds/interarrival.py: A script to compute inter-arrival times from Graphameleon traces.

This script takes a trace file as input,
 runs a SPARQL query to extract core:objectCreatedTime values,
 and computes inter-arrival times from these.
Results are saved in a CSV file for postprocessing, such as injecting
 inter-arrival times into the trace files for complementary analysis.
"""

# === Imports ==========================================================

import pandas as pd
from rdflib import Graph, Literal
import logging
import os

# === Fonctions ========================================================

def discretize(delta_time):
    """
    Fonction pour discrétiser les mesures d'intertemps
    :param delta_time: intertemps
    :return: label
    """
    logger.debug("low_threshold=%s:high_threshold=%s:delta_time=%s", low_threshold, high_threshold, delta_time)
    if delta_time <= low_threshold:
        return 'low'
    elif delta_time <= high_threshold:
        return 'medium'
    else:
        return 'high'


# === Init =============================================================

logger = logging.getLogger(__name__)
loggingFormatString = (
    "%(asctime)s:%(levelname)s:%(threadName)s:%(funcName)s:%(message)s"
)
logging.basicConfig(format=loggingFormatString, level=logging.DEBUG)

logger.info("INIT")

# Charger la requête SPARQL
with open('rq_list_objectCreatedTime.sparql') as f:
    query = f.read()
    logger.debug("INIT:Query loaded=\n%s", query)

# === Traitement =======================================================

# Parcourir les fichiers de données (graphes)
files = ['../exp-02/GPL_attack_scenario.ttl', '../exp-02/GPL_alternative_scenario.ttl', '../exp-02/GPL_normal_scenario.ttl']
logger.debug("INIT:Files to process=%s", files)
for f in files:
    logger.info("PROCESSING=%s", f)
    g = Graph()
    g.parse(f, format='turtle')
    results = g.query(query)

    # Extraire les résultats dans un DataFrame pandas
    data = []
    for row in results:
        data.append({
            'item': row.item,
            'timestamp': pd.to_datetime(row.timestamp)
        })
    df = pd.DataFrame(data)
    logger.debug("PROCESSING=%s:Query results=\n%s", f, df)

    # Calculer le delta de temps entre les mesures
    df['delta_time'] = df['timestamp'].diff().dt.total_seconds()

    # Supprimer la première ligne qui aura une valeur NaN pour le delta de temps
    df = df.dropna(subset=['delta_time'])
    logger.debug("PROCESSING=%s:Delta_time results=\n%s", f, df)

    # TODO: check row to row order using the item_next column to raise a warning if next row's item value is not the same.

    # Calculer les percentiles pour discrétiser les deltas de temps
    percentiles = df['delta_time'].quantile([0.33, 0.66])

    # Définir les seuils pour les niveaux low, medium et high
    low_threshold = percentiles[0.33]
    high_threshold = percentiles[0.66]
    logger.info("PROCESSING=%s:low_threshold=%s:high_threshold=%s", f, low_threshold, high_threshold)

    # Appliquer la fonction de discrétisation à la colonne delta_time
    df['delta_time_level'] = df['delta_time'].apply(discretize)
    logger.debug("PROCESSING=%s:Discretize results=\n%s", f, df)

    # Sauvegarder le DataFrame dans un fichier CSV
    out_file = "output_oct_interarrival_{}.csv".format(os.path.basename(f))
    df.to_csv(out_file, index=False)
    logger.info("PROCESSING=%s:Saved results to file=%s", f, out_file)

logger.info("END")

# ===EOF ===============================================================
