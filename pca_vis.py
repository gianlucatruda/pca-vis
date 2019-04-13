import os
import time
import sys

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

from sliders import Slider


def plot_pair(x):
    plt.ion()
    plt.cla()
    ax = plt.scatter(x[0][0], x[0][1])
    plt.xlim(-10, 100)
    plt.ylim(-10, 100)


def setup_sliders(df):
    slides = []
    for i, col in enumerate(df.columns):
        slides.append(Slider(
            col,    # Label
            df[col].mean(),  # Start value
            df[col].max(),  # Max value
            -1,  # Min value (unstable)
            (i % 5) * 160,  # xpos
            (i//(5)) * 60,  # ypos
        ))

    return slides


def run_sim(scaler, pca, slides):
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
        print(f'{vect} -> {pair}')
        plot_pair(pair)


def main(df: pd.DataFrame):
    df = df.dropna()
    print(df.shape)

    features = df.columns.values.tolist()
    x = df.loc[:, features].values

    # Standardizing the features
    scaler = StandardScaler()
    scaler.fit(x)
    x = scaler.transform(x)

    pca = PCA(2)
    pca.fit(x)

    ex_variance = np.var(x, axis=0)
    ex_variance_ratio = ex_variance/np.sum(ex_variance)

    print(f'Components: {pca.n_components_}')
    print('Variance ratios of PCs:', ex_variance_ratio, sep='\n')

    slides = setup_sliders(df)

    run_sim(scaler, pca, slides)


if __name__ == '__main__':
    iris = datasets.load_iris()

    df = pd.DataFrame(data=np.c_[iris['data'], iris['target']],
                      columns=iris['feature_names'] + ['target'])

    print(df.info())

    main(df)
