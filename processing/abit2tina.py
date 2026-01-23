#  Copyright (c) 2022-2026 Orange. All rights reserved in accordance to the CC-BY-NC-SA license
#  Project: graphameleon-ds
#  THIS SOFTWARE IS PROVIDED BY Orange "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL Orange BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import pandas as pd
from collections import defaultdict
import sys

def transform_to_petri_net(input_file, output_file):
    # Lecture des données à partir du fichier texte
    data = pd.read_csv(input_file, sep=' ', header=None, names=["page", "object", "action", "action_tag", "delta_t", "scénario"])

    # Initialisation des structures de données
    places = set()
    transitions = defaultdict(list)
    edges = []

    # Parcours des données pour collecter les places et les transitions
    for index, row in data.iterrows():
        current_page = row['page']
        next_page = data.loc[index + 1, 'page'] if index + 1 < len(data) else None
        object_action_tag = f"{row['object']}_{row['action_tag']}"

        # Ajouter les places
        places.add(current_page)
        if next_page:
            places.add(next_page)

        # Ajouter les transitions
        if next_page:
            transitions[current_page].append((object_action_tag, next_page))

    # Génération du format de sortie
    petri_net = []

    # Ajouter les places
    for i, place in enumerate(places):
        x = 30.0
        y = 160.0 + i * 50.0  # Espacement vertical pour les places
        petri_net.append(f"p {x} {y} {place} 0 n")

    # Ajouter les transitions et les arcs
    for i, (place, transition_list) in enumerate(transitions.items()):
        for transition, next_place in transition_list:
            x = 40.0
            y = 70.0 + i * 50.0  # Espacement vertical pour les transitions
            petri_net.append(f"t {x} {y} {transition} 0 w n")
            petri_net.append(f"e {place} {transition} 1 n")
            petri_net.append(f"e {transition} {next_place} 1 n")

    # Ajouter la dénomination du modèle
    petri_net.append("h my_net")

    # Sauvegarde des résultats dans le fichier de sortie
    with open(output_file, 'w') as f:
        f.write("\n".join(petri_net))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python abit2tina.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    transform_to_petri_net(input_file, output_file)
