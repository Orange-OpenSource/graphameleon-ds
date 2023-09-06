# Copyright (c) 2022-2023 Orange. All rights reserved in accordance to the CC-BY-NC-SA license
# Project: graphameleon-ds
# THIS SOFTWARE IS PROVIDED BY Orange "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL Orange BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

SHELL := /bin/bash
ROOT_DIR := $(PWD)

SPARQL_QUERY_TOOL := ~/.local/jena/bin/sparql

## makefile for the graphameleon-ds / exp-01 project
help:	## Show this help.
	# Get lines with double dash comments and display it
	@fgrep -h "## " $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/## //'

lint-turtle:	## Check Turtle syntax
	@echo -e "\033[35m > Check turtle syntax\033[0m - requires TurtleValidator: npm install -g turtle-validator (see https://github.com/IDLabResearch/TurtleValidator)"
	@find ./ -type f -name *.ttl -printf "\n%f\n" -exec /usr/local/bin/ttl {} \;

	@echo -e "\033[35m > Done  \033[0m"

lint: lint-turtle

rq-count-triples:	## Run local SPARQL query for counting triples
	@echo -e "\033[35m > Run SPARQL queries  \033[0m"
	@find ./ -type f -name "GPL_*.ttl" \
	  -printf "\n%f\n" \
	  -exec sh -c "$(SPARQL_QUERY_TOOL) --query queries/count-triples.sparql --data {} --results csv" \;
	@echo -e "\033[35m > Done  \033[0m"

rq-count-subjects:	## Run local SPARQL query for counting subjects
	@echo -e "\033[35m > Run SPARQL queries  \033[0m"
	@find ./ -type f -name "GPL_*.ttl" \
	  -printf "\n%f\n" \
	  -exec sh -c "$(SPARQL_QUERY_TOOL) --query queries/count-subjects.sparql --data {} --results csv" \;
	@echo -e "\033[35m > Done  \033[0m"

rq-count-classInstances:	## Run local SPARQL query for counting classes instances
	@echo -e "\033[35m > Run SPARQL queries  \033[0m"
	@find ./ -type f -name "GPL_*.ttl" \
	  -printf "\n%f\n" \
	  -exec sh -c "$(SPARQL_QUERY_TOOL) --query queries/count-classInstances.sparql --data {} --results csv" \;
	@echo -e "\033[35m > Done  \033[0m"

