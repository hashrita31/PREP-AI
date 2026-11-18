# PREP-AI
Interview prep app built with Python, Streamlit and scikit-learn. Rate your skills, find weak topics, follow a study roadmap, practise questions and get an ML-based readiness level.
Rate your skills across core topics, see where you are strong or weak, follow a week-by-week study plan, practise with generated questions, and get a readiness level from a machine learning model.

## What it does

- **Assess your skills:** self-rate on Arrays, Linked List, Stack, Queue, DBMS and Operating Systems.
- **Find weak and strong topics:** scores below 50 are flagged as weak and scores of 75 or more as strong.
- **Follow a roadmap:** get a four-week study plan for each weak topic.
- **Practise questions:** generate random questions by topic and difficulty.
- **Check your readiness:** a Decision Tree classifier turns your average score into a level: Low, Medium, Good or Excellent.
- **Track progress:** see current scores against the target for every topic.

## Features

**Dashboard**
- Average score, weak-topic count and strong-topic count at a glance
- Topic-wise bar chart
- Separate lists of topics that need work and topics you have mastered

**Machine learning**
- Decision Tree Classifier built with scikit-learn
- Predicts interview readiness from your average skill score

**Question generator**
- Questions loaded from a JSON file, so you can add your own
- Random selection by topic and difficulty

**Interface**
- Clean dark theme with a sidebar menu and a home page with quick-start cards
- Works on desktop and mobile screens

## Tech stack

Python · Streamlit · scikit-learn · pandas
