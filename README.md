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
Prior work in this area centers around two groups of research. Several papers revolve around the topic of Natural Language Processing for Type Inference. [DeepTyper](http://vhellendoorn.github.io/PDF/fse2018-j2t.pdf) is a deep learning model that understands which types naturally occur in certain contexts and relations and can provide _type suggestions_. DeepTyper specifically trains on TypeScript files, which contain type suggesetions, and then can be run on JavaScript or TypeScript to predict types. [JSNice](http://jsnice.org/) is another tool that can be used to predict types from JavaScript code. However, instead of using Natural Language Processing to guess at types, JSNice takes an input program and builds a dependency network, then leverages Conditional Random Fields to predict type annotations. A third tool, NL2Type also uses natural language information to predict types. Evidently, the set of identifiers that get accurately predicted from DeepTyper or NL2Type is somewhat orthogonal to the identifiers that get predicted from JSNice. This means that combining two of them actually yields significantly better results than either of them alone.

Another way that some researchers have attempted to predict types is using static analysis tools. [Typpete](https://github.com/caterinaurban/Typpete) is an SMT-based tool for static type inference. It uses the Z3 solver from Microsoft Research. Another paper does [Probabilistic Type Inference](https://dl.acm.org/citation.cfm?id=2950343) for python. This paper aggregates the probability of a variable type throughout a program, eventually converging on a solution. 

The initial three papers use machine learning to predict types, but they are all specifically built for JavaScript or TypeScript. The later papers predict types for python, but both use static analysis tools. This project aims to predict types for python using natural language information. Although the model has changed, this project was originally nicknamed "DeepTyper for Python".

## Data Gathering
Initially, this project attempted to use a [dataset](https://www.sri.inf.ethz.ch/py150) from the Software Reliability Lab at ETH Zurich. However, in the 150,000 python files included in the dataset, not a single one of them used python's typing module. This can probably be attributed to the fact that this dataset must have been generated prior to when the typing module was added in the release of Python 3.5 in 2015.

Instead, I generated my own dataset of python files by [searching github](https://github.com/search?p=99&q=%22from+typing+import%22+NOT+%22rasa_nlu%22+-filename%3Aann_module.py+-filename%3Abasecommand.py+-filename%3Atyping.py+-filename%3Atest.py+extension%3A.py&type=Code) and cloning repos. The search I used started out straightforward, but became more specific and complex as I continued to find duplicate results.

Combing through much of the possible code on github that contained the phrase `import typing` or `from typing import`, I was able to find 2062 python files that included the typing module. This amounted to 1,068,993 total lines of code. While this felt like a great accomplishment, I realize that ultimately, it is way too small. In 1 million lines of code there are only around 10,000 total type annotations.

Data preparation happens in several files.

1. `explore.py` iterates over every repo in the `repos` folder and copies over any files that contain the typing module into the `processed` folder, while adding an ID, to avoid name collisions.
2. `strip_hints_from_processed.py` iterates over every file in the `processed` folder and strips out all type hints. This uses the `strip_hints` python module. After the type hints are stripped, each file is copied into the `stripped` folder.
3. `flair_prepare.py` tokenizes the python files. It splits each token onto it's own line and tags it with it's token_type, exact_type, and type_suggestion. It then copies each of the files into the `tokenized` folder as a .txt file.


A function declaration in the `processed` folder might look like this:
```
def require_version_gte(pkg_name: str, version: str) -> None:
```
It would then have the type hints stripped and be copied to the `stripped` folder.
```
def require_version_gte(pkg_name     , version     )      :
```
Afterward, it is tokenized and placed in the `tokenized` folder.
```
require_version_gte NAME NAME None
pkg_name NAME NAME str
version NAME NAME str
```

![data flow diagram][data_flow]

## Current Progress
Once the data is prepared, it can be used to train a model. I am using the new framework [Flair](https://github.com/zalandoresearch/flair). Their documentation is fantastic and it was extremely easy to understand how to prepare my data. They also have a lot of code snippets showing how to use their framework. Flair is built directly on top of pytorch. Other than pytorch, few other libraries are required.

First, in order to train a language model, I needed to generate character mappings. That way, during training, I could use my own pre-built dictionary based on actual python code, instead of a generic english dictionary. The code to generate the mappings is in `generate_mappings.py`.

Although Flair is easy to get set up with, I have run into several issues actually trying to train using it.

1. The first issue I have run into relates to trying to train a model when input data has sentences of length 0. This happens because occasionally my .txt files had blank lines in them. While it is trivial to remove the blank lines, I wanted to avoid changing my data files, since I feared it might break how Flair reads in sentences. I had read in this [github issue](https://github.com/zalandoresearch/flair/issues/33) that if I was using the latest version of Flair, this shouldn't be a problem anyway. When I attempted to use the fix suggested in the github issue to just remove the empty sentences, I ran into another issue. It turns out that Flair has started using the python `property` decarator for the `train`, `test`, and `dev` class variables, which means that they are not directly settable anymore. This left me with no other choice than to remove all blank lines from my tokenized .txt files.
2. Next, I ran into a specific issue because I am running the code on my PC, using Windows 10 64 bit. I opened a [github issue](https://github.com/zalandoresearch/flair/issues/777) on Flair's repository. I dug through Flair's code for a bit, attempting to implement the fix found in this [pytorch issue](https://github.com/pytorch/pytorch/issues/7485), but was ultimately unsuccessful.
3. Lastly, I ported my code over to a google cloud VM. Since I was low on credits, I set up the VM with a Tesla P100 GPU and only 8GB of RAM. In hindsight, I should have given it significantly more RAM. Now, on Linux, I was able to get `train.py` to actually start training on my tokenized data. However, I ran it for several hours and it never completed the first epoch. I believe if I were to re-run this on a VM with something like 64GB of memory I might see different results.

Assuming I had gotten past the Flair bugs that I ran into, I had planned to use flair's built in `train` method. The `train` method runs on a `tagger`, which I create using Flair's GloVe embeddings and my own character dictionary.  

![nn_diagram][nn_diagram]

## Future Work
To continue this work, a few things should be done:
* Gather much more data. You'll probably need 10x-100x the amount of data I currently have.
* Fix [bug](https://github.com/tjchambers32/ecs289-final/issues/3) in type suggestion finder that sometimes misses a function's return type when it's on a different line.
* Fix flair bugs (outlined in this readme) that are preventing training.
* Find how many repos have added types later vs. used types from the beginning. If there are many repos that added types later, we can train on the commits when types are added and test on last commits before types were added. This would remove the need for stripping the type hints ourselves.
* Answer the RQ: Why have python types not been adopted more generally? What is preventing the python community from utilizing type annotations in their code?

At LLNL, we participate regularly in hackathons. I plan on garnering interest in continuing this project for our next hackathon. At the hackathon, we will have access to a server running Ubuntu with a GTX 1080 Ti and 64GB of RAM. This should help us avoid some of the errors I've already run into.

## Bibliography
**DeepTyper** - Vincent J. Hellendoorn, Christian Bird, Earl T. Barr, and Miltiadis Allamanis. 2018. Deep learning type inference. In Proceedings of the 2018 26th ACM Joint Meeting on European Software Engineering Conference and Symposium on the Foundations of Software Engineering (ESEC/FSE 2018). ACM, New York, NY, USA, 152-162. DOI: https://doi.org/10.1145/3236024.3236051

**JSNice** - 
Veselin Raychev, Martin Vechev, and Andreas Krause. 2019. Predicting program properties from 'big code'. Commun. ACM 62, 3 (February 2019), 99-107. DOI: https://doi.org/10.1145/3306204

**NL2Type** - Rabee Sohail Malik, Jibesh Patra, and Michael Pradel. 2019. NL2Type: inferring JavaScript function types from natural language information. In Proceedings of the 41st International Conference on Software Engineering (ICSE '19). IEEE Press, Piscataway, NJ, USA, 304-315. DOI: https://doi.org/10.1109/ICSE.2019.00045

**Typpete** - Hassan M., Urban C., Eilers M., Müller P. (2018) MaxSMT-Based Type Inference for Python 3. In: Chockler H., Weissenbacher G. (eds) Computer Aided Verification. CAV 2018. Lecture Notes in Computer Science, vol 10982. Springer, Cham. DOI: https://doi.org/10.1007/978-3-319-96142-2_2

**Python Probabilistic Type Inference** - Zhaogui Xu, Xiangyu Zhang, Lin Chen, Kexin Pei, and Baowen Xu. 2016. Python probabilistic type inference with natural language support. In Proceedings of the 2016 24th ACM SIGSOFT International Symposium on Foundations of Software Engineering (FSE 2016). ACM, New York, NY, USA, 607-618. DOI: https://doi.org/10.1145/2950290.2950343


[data_flow]: https://github.com/tjchambers32/ecs289-final/raw/master/images/data_flow_diagram.jpeg
[nn_diagram]: https://github.com/tjchambers32/ecs289-final/raw/master/images/neural_net_diagram.jpeg