#  Copyright (c) 2022-2026 Orange. All rights reserved in accordance to the CC-BY-NC-SA license
#  Project: graphameleon-ds
#  THIS SOFTWARE IS PROVIDED BY Orange "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL Orange BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""graphameleon-ds/percentiles_global.py: A script to compute global inter-arrival percentiles from Graphameleon traces.

This script takes as input a set of files from the interarrival.py
 script, and computes global percentiles times from these.
Results are saved in a CSV file for postprocessing, such as injecting
 inter-arrival levels into the trace files for complementary analysis.
"""

# === Imports ==========================================================

import pandas as pd
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

# === Traitement =======================================================

# Initialiser le dataframe
data = []

# Parcourir les fichiers de données
files = ['./output_oct_interarrival_GPL_normal_scenario.ttl.csv', './output_oct_interarrival_GPL_attack_scenario.ttl.csv', './output_oct_interarrival_GPL_alternative_scenario.ttl.csv']
logger.debug("INIT:Files to process=%s", files)
for f in files:
    logger.info("LOADING=%s", f)
    df = pd.read_csv(f, index_col=None, header=0)

    # Supprime la colonne delta_time_level si elle existe
    df = df.drop(['delta_time_level'], axis=1, errors='ignore')

    # Ajoute la provenance des données
    df['file'] = os.path.basename(f)

    # Concatène les données chargées
    data.append(df)

logger.debug("LOADING:data=%s", data)

# df = pd.DataFrame(data)
df = pd.concat(data, axis=0, ignore_index=True)

# Calculer les percentiles pour discrétiser les deltas de temps
percentiles = df['delta_time'].quantile([0.33, 0.66])

# Définir les seuils pour les niveaux low, medium et high
low_threshold = percentiles[0.33]
high_threshold = percentiles[0.66]
logger.info("PROCESSING:low_threshold=%s:high_threshold=%s", low_threshold, high_threshold)

# Appliquer la fonction de discrétisation à la colonne delta_time
df['delta_time_level'] = df['delta_time'].apply(discretize)
logger.debug("PROCESSING:Discretize results=\n%s", df)

# Sauvegarder le DataFrame dans un fichier CSV
out_file = "output_interarrival_global.csv"
df.to_csv(out_file, index=False)
logger.info("SAVING=%s:Saved results to file=%s", f, out_file)

logger.info("END")

# ===EOF ===============================================================
