## Running the scripts

Require Python.

Download resource definition to folder implementation/io.

Replace `<resource-name>` with the resource name.

### Abstraction

```
# cd implementation\scripts
# python abstraction.py ..\io\<resource-name>.profile.json ..\configurations\types.definitions.json ..\io\
```

### Substitution

```
# cd implementation\scripts
# python substitution.py ..\io\<resource-name>.schema.fhir.json ..\configurations\equivalents.json ..\io\
```

### Definition

```
# cd implementation\scripts
# python definition.py ..\io\<resource-name>.schema.openehr.json ..\io\
```

### Creation

```
# cd implementation\scripts
# creation.bat ..\io\<resource-name>.profile.json ..\configurations\types.definitions.json ..\io\ ..\io\<resource-name>.schema.fhir.json ..\configurations\equivalents.json ..\io\<resource-name>.schema.openehr.json
```

## Running the tests

```
# cd implementation\scripts
# python -m unittest abstraction_test
# python -m unittest substitution_test
# python -m unittest definition_test
```
## Create paper

Require TeX program (with the LaTeX macros loaded).

### Spanish version

```
# cd paper\spanish
# pdflatex paper
# biber paper
# pdflatex paper
# pdflatex paper
```
