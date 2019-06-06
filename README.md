# ECS 289 Final Project
This is my final project for ECS 289G at UC Davis, Spring 2019 with Professor Devanbu.

The goal of this work is to provide a model that can predict python types based on natural language information. 

This could then be used to automatically add type annotations to python modules.

## Motivation
Python is one of the most widely used languages today. It is also the fastest growing major language. In a recent survey from [stackoverflow](https://insights.stackoverflow.com/survey/2019#technology
), 41% of developers stated that they use python, second only to JavaScript. Stackoverflow also asked on the survey, "What is your most Loved, Dreaded, and Wanted language?" Python ranked first for the wanted category at 25.7%. 

Python is a [dynamically typed language](https://en.wikipedia.org/wiki/Dynamic_programming_language). This means that types are not checked at compile time. Instead, at runtime, type errors are thrown as exceptions. Recently, python has started integrating [type hints](https://www.python.org/dev/peps/pep-0484/). These type hints allow static analyzers to catch potential errors, but cause no extra type checking to happen at runtime. They added a [typing module](https://docs.python.org/3/library/typing.html) in python 3.5 that allows developers to import common types (List, Dict, etc.) for use in type annotations.

However, these additions have not been widely adopted. Almost none of the large python packages have adopted type suggestions. This can partially be blamed on the fact that many projects still support python 2, while type suggestions are only available for python 3.5+. Even in the hobbyist community, where projects are smaller and more likely to only support newer python versions, type suggestions have not been adopted.

Types are generally recognized as useful for developers. A [recent study](https://ieeexplore.ieee.org/document/7985711) found that 15% of bugs in JavaScript could be prevented by type annotations. APIs that lack type annotations are harder to understand and are more difficult to read, maintain, and document. Additionally, IDEs can give much better autocomplete suggestions when they have type information to limit the scope of possible autocompletions.

Why have python types not become more mainstream in python projects? This work does not attempt to answer this research question, though it is interesting and should be a part of future work.

Instead, this work aims to provide a simple way to for developers to start adopting type annotations. 

## Prior Work

## Data Gathering

## Current Progress

### Directories

### Data/Source Files

## Future Work

## Related Work

## Diagrams

2 Prior work in the area, and the precise contribution of your project, and (if applicable) how it goes beyond. Include citations

3 What Data you gathered, and how you did that. Refer to diagram below.

4 Carefully document your work so far, so someone has a chance of picking it up. 

--explanation of directories in the Repo.

--Explanation of data/source files, and their purpose, shape, algorithm, etc. Please relate the files in the directory to the parts of the diagrams (see below for diagram requirements)  

5 Bibliography . (Related papers, cited)

6 Diagrams (could be in line, or after bibliography)

The  report should  include two  diagrams (diagrams  about 1/3  to 1/2

page, clearly legible)

--explaining the flow chart of the data gathering process, starting with your

raw sources.

 

--Diagram of of your machine learner, including layers, showing both test and

training time information flows.