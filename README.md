# PCA Visualisation

Real-time tool for exploring the relationships between [PCA](https://en.wikipedia.org/wiki/Principal_component_analysis) components and input features.

Or, _"Roughly what do these principal components actually correspond to?"_

![Demonstration GIF](docs/demo.gif)

## Features
* Real-time plot to give intuition about prinipal components.
* Sliders dynamically created for each input feature.
* Sliders begin at mean and are scaled to feature data ranges, giving an intuitive feel of how "sensitive" the components are to each feature.

## Installation

```bash
pip install -r requirements.txt
```
Matplotlib has to be installed as a framework.

## Usage

Run the demo on the [iris dataset](http://archive.ics.uci.edu/ml/datasets/iris) using:

```bash
python3 pca_vis.py
```

Or load any dataset as a Pandas DataFrame and pass it into the `main()` function as an argument.


## Contributions

* Gianluca Truda — [Github](https://github.com/gianlucatruda) | [LinkedIn](https://za.linkedin.com/in/gianluca-truda)

This project was inspired by [this one](https://github.com/HackerPoet/FaceEditor) and adapted the generic slider code [from here](https://www.dreamincode.net/forums/topic/401541-buttons-and-sliders-in-pygame/).
