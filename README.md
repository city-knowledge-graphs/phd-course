# Knowledge Graphs in the era of Large Language Models

This PhD course is organised in 4 sessions of 3 hours each combining theory and practice.
This course is a tailored version of [City's Semantic Web Technologies and Knowledge Graphs module](https://github.com/turing-knowledge-graphs/teaching/tree/main/city).

## Setting-up 

The example codes will be in [Python](https://www.python.org/downloads/) (tested with Python version >=3.10). I strongly recommend using Python environments to use the right library versions.
Follow the instructions in the [lab session 0](https://github.com/city-knowledge-graphs/phd-course/blob/main/labs/phd-course-kgs-aalborg-lab-session-0.pdf) and run the scripts in the [test folder](https://github.com/city-knowledge-graphs/phd-course/tree/main/python/test) to check you have the required infrastructure and Python libraries.

To avoid clashes with the changes on the main branch it is suggested to add generated codes and data in the folder [student-codes-data](https://github.com/city-knowledge-graphs/phd-course/tree/main/python/student-codes-data).

## Session 1
- Lecture: Introduction to Knowledge Graphs ([Slides](https://github.com/city-knowledge-graphs/phd-course/blob/main/lectures/phd-course-kgs-aalborg-session-1-intro.pdf))
- Laboratory: Creating a small KG and ontology ([Lab notes](https://github.com/city-knowledge-graphs/phd-course/blob/main/labs/phd-course-kgs-aalborg-lab-session-1-kgs-onto.pdf)) ([support slides](https://github.com/city-knowledge-graphs/phd-course/blob/main/labs/phd-course-kgs-aalborg-lab-session-1-2-support-slides.pdf))
- [Support codes](https://github.com/city-knowledge-graphs/phd-course/tree/main/python/lab-session1).

## Session 2
- Lecture: Reasoning and Querying with Knowledge Graphs ([Slides](https://github.com/city-knowledge-graphs/phd-course/blob/main/lectures/phd-course-kgs-aalborg-session-2-querying-reasoning.pdf))
- Laboratory: First steps with the SPARQL query language ([Lab notes](https://github.com/city-knowledge-graphs/phd-course/blob/main/labs/phd-course-kgs-aalborg-lab-session-2-reasoning-sparql.pdf)) ([support slides](https://github.com/city-knowledge-graphs/phd-course/blob/main/labs/phd-course-kgs-aalborg-lab-session-1-2-support-slides.pdf))
- [Support codes](https://github.com/city-knowledge-graphs/phd-course/tree/main/python/lab-session2).

## Session 3
- Lecture: Matching: KG-to-KG and CSV-to-KG (Slides)
- Laboratory: Creation of a (simple) matching system (Lab notes)
- [Support codes](https://github.com/city-knowledge-graphs/phd-course/tree/main/python/lab-session3).
  
## Session 4
- Lecture: Knowledge Graphs and Language Models (Slides)
- Laboratory: Ontology Embeddings with OWL2Vec* (Lab notes)
- [Support codes](https://github.com/city-knowledge-graphs/phd-course/tree/main/python/lab-session4).
  
## Project description

Students need to work on a small project (max 2 students per group). There are two options:
1. Create a (simple) system that performs KG to KG alignment. Try to implement some sophisticated ideas as described in the lecture. Selected systems may try to participate in the [OAEI campaign](http://oaei.ontologymatching.org/).
2. Create a (simple) system that performs CSV to KG matching. Try to implement disambuguation techniques as shown in the lecture. Selected systems may try to participate in the [SemTab challenge](https://www.cs.ox.ac.uk/isg/challenges/sem-tab/).

Submission:
- **When:** June 16, 23:59 CEST (strict deadline)
- **What:** a link to the GitHub repository where the system codes are. Please document the repository so that the codes are easy to run
- **How:** via this [Google form](https://forms.gle/xxwynC59y1xCgdvj8).
