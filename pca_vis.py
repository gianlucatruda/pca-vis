"""Dynamic visualisation of PCA components relative to feature inputs.

Concept inspired by this project: https://github.com/HackerPoet/FaceEditor
"""

# Standar library
import os
import time
import sys
import logging
# Third-party libraries
import numpy as np
import pandas as pd
import pygame
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
import matplotlib.colors as colors
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn import datasets
# Local project imports
from sliders import Slider


def plot_pair(x, xs=None):
    """Plots the dynamics point on 2D scatter.

    :param x: Pair of coordinates for 2D plane corresponding to the
        Principal Components
    :param xs: Coordinate pairs for other (static) data points to plot,
        defaults to None
    """

    plt.ion()
    plt.cla()
    xlim, ylim = (-10, 10), (-10, 10)

    if xs is not None:
        x_vals = [x[0] for x in xs]
        y_vals = [x[1] for x in xs]
        ax = plt.scatter(x_vals, y_vals)
        xlim, ylim = (min(x_vals), max(x_vals)), (min(y_vals), max(y_vals))

    ax2 = plt.scatter(x[0][0], x[0][1])

    plt.xlim(xlim)
    plt.ylim(ylim)


def setup_sliders(df):
    """Configures the PyGame sliders to match PCA transformation.

    :param df: Pandas DataFrame of features in 3+ dimensions.
    :return: The PyGame sliders configured to the feature ranges and
        means.
    """

    slides = []
    for i, col in enumerate(df.columns):
        slides.append(Slider(
            col,    # Label
            df[col].mean(),  # Start value
            df[col].max(),  # Max value
            df[col].min(),  # Min value (unstable)
            (i % 5) * 160,  # xpos
            (i//(5)) * 60,  # ypos
        ))

    return slides


def run_sim(scaler, pca, slides, data=None):
    """Runs the PyGame window and dynamic plot.

    :param scaler: The fitted sklearn Scaler to use for transforming.
    :param pca: The fitted sklearn PCA decompositor for dim. reduc.
    :param slides: The configured PyGame sliders.
    :param data: Optional datapoints to plot under the dynamic point,
        defaults to None
    """

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for s in slides:
                    if s.button_rect.collidepoint(pos):
                        s.hit = True
            elif event.type == pygame.MOUSEBUTTONUP:
                for s in slides:
                    s.hit = False

        # Move slides
        for s in slides:
            if s.hit:
                s.move()

        for s in slides:
            s.draw()

        pygame.display.flip()
        vect = [[s.val for s in slides]]
        vect = scaler.transform(vect)
        pair = pca.transform(vect)
        if data is not None:
            plot_pair(pair, xs=data)
        else:
            plot_pair(pair)


def main(df: pd.DataFrame):
    """Runs PCA vis. on given dataframe.

    :param df: Pandas DataFrame of features.
    """

    df = df.dropna()
    print(df.shape)

    features = df.columns.values.tolist()
    x = df.loc[:, features].values

    # Standardizing the features
    scaler = StandardScaler()
    scaler.fit(x)
    x = scaler.transform(x)

    # 2D PCA performed
    pca = PCA(2)
    pca.fit(x)

    ex_variance = np.var(x, axis=0)
    ex_variance_ratio = ex_variance/np.sum(ex_variance)

    logging.info(f'Components: {pca.n_components_}')
    logging.info(f'Variance ratios of PCs:\n{ex_variance_ratio}')

    # Configure PyGame sliders to match features
    slides = setup_sliders(df)

    # Run the visualisation
    run_sim(scaler, pca, slides, pca.transform(x))


if __name__ == '__main__':
    logging.info('Loading iris data...')
    iris = datasets.load_iris()

    df = pd.DataFrame(data=np.c_[iris['data']],
                      columns=iris['feature_names'])

    logging.info(df.info())

    main(df)
