import matplotlib.pyplot as plt
import numpy as np

import api.spotify as spotify
import api.utils as utils

from api.spotify import FeatureType, FeatureFilter

def plot_all_features(tracks, overlay_tracks=None):
    fig0, axs0 = double_plot()
    histogram(fig0, axs0[0], "Danceability", spotify.get_feature_values(tracks, FeatureType.DANCEABILITY))
    histogram(fig0, axs0[1], "Energy", spotify.get_feature_values(tracks, FeatureType.ENERGY))

    if overlay_tracks != None:
        histogram(fig0, axs0[0], "Danceability", spotify.get_feature_values(overlay_tracks, FeatureType.DANCEABILITY))
        histogram(fig0, axs0[1], "Energy", spotify.get_feature_values(overlay_tracks, FeatureType.ENERGY))        


    fig1, axs1 = double_plot()
    bar(fig1, axs1[0], "Key", utils.key_mapping, spotify.get_feature_values(tracks, FeatureType.KEY))
    histogram(fig1, axs1[1], "Loudness", spotify.get_feature_values(tracks, FeatureType.LOUDNESS), min_val=-60, max_val=0, num_bins=60, num_ticks=12)

    if overlay_tracks != None:
        bar(fig1, axs1[0], "Key", utils.key_mapping, spotify.get_feature_values(overlay_tracks, FeatureType.KEY))
        histogram(fig1, axs1[1], "Loudness", spotify.get_feature_values(overlay_tracks, FeatureType.LOUDNESS), min_val=-60, max_val=0, num_bins=60, num_ticks=12)


    if overlay_tracks == None:
        fig2, axs2 = single_plot()
        pie(fig2, axs2, "Mode", ['major', 'minor'], spotify.get_feature_values(tracks, FeatureType.MODE))
    else:
        fig2, axs2 = double_plot()
        pie(fig2, axs2[0], "Source Tracks' Mode", ['major', 'minor'], spotify.get_feature_values(tracks, FeatureType.MODE))
        pie(fig2, axs2[1], "Filtered Tracks' Mode", ['major', 'minor'], spotify.get_feature_values(overlay_tracks, FeatureType.MODE))


    fig3, axs3 = double_plot()
    histogram(fig3, axs3[0], "Speechiness", spotify.get_feature_values(tracks, FeatureType.SPEECHINESS))
    histogram(fig3, axs3[1], "Acousticness", spotify.get_feature_values(tracks, FeatureType.ACOUSTICNESS))

    if overlay_tracks != None:
        histogram(fig3, axs3[0], "Speechiness", spotify.get_feature_values(overlay_tracks, FeatureType.SPEECHINESS))
        histogram(fig3, axs3[1], "Acousticness", spotify.get_feature_values(overlay_tracks, FeatureType.ACOUSTICNESS))


    fig4, axs4 = double_plot()
    histogram(fig4, axs4[0], "Instrumentalness", spotify.get_feature_values(tracks, FeatureType.INSTRUMENTALNESS))
    histogram(fig4, axs4[1], "Liveness", spotify.get_feature_values(tracks, FeatureType.LIVENESS))

    if overlay_tracks != None:
        histogram(fig4, axs4[0], "Instrumentalness", spotify.get_feature_values(overlay_tracks, FeatureType.INSTRUMENTALNESS))
        histogram(fig4, axs4[1], "Liveness", spotify.get_feature_values(overlay_tracks, FeatureType.LIVENESS))


    fig5, axs5 = double_plot()
    histogram(fig5, axs5[0], "Valence", spotify.get_feature_values(tracks, FeatureType.VALENCE))
    histogram(fig5, axs5[1], "Tempo", spotify.get_feature_values(tracks, FeatureType.TEMPO), min_val=0, max_val=250, num_bins=50)

    if overlay_tracks != None:
        histogram(fig5, axs5[0], "Valence", spotify.get_feature_values(overlay_tracks, FeatureType.VALENCE))
        histogram(fig5, axs5[1], "Tempo", spotify.get_feature_values(overlay_tracks, FeatureType.TEMPO), min_val=0, max_val=250, num_bins=50)

def single_plot():
    fig, axs = plt.subplots(1, 1)
    fig.set_size_inches(15, 5)
    
    return fig, axs

def double_plot():
    fig, axs = plt.subplots(1, 2)
    fig.set_size_inches(15, 5)
    
    return fig, axs

def histogram(fig, ax, title, values, min_val=0.0, max_val=1.0, num_bins=50, num_ticks=10):
    ax.hist(values, bins=num_bins, range=(min_val, max_val), rwidth=1.0, edgecolor='black', linewidth=1.0)
    
    ax.set_xticks(np.linspace(min_val, max_val, num=num_ticks+1))
    ax.grid(which='major', axis='y')
    
    ax.set_title(title)
    ax.set_xlabel(title.lower())
    ax.set_ylabel("frequency")
    
def bar(fig, ax, title, categories, values):
    x = np.arange(len(categories))
    heights = [0]*len(categories)
    for value in values:
        heights[categories.index(value)] += 1
    
    ax.bar(x, heights)
    
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.grid(which='major', axis='y')
    
    ax.set_title(title)
    ax.set_ylabel("frequency")
    
def pie(fig, ax, title, categories, values):
    counts = [0]*len(categories)
    for value in values:
        counts[categories.index(value)] += 1
    
    ax.pie(counts, labels=categories, autopct=lambda percent:'{:.2f}%'.format(percent))
    ax.set_title(title)