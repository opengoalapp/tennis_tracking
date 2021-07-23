# Example demonstrating plotting of ball tracking data on a tennis court

import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from plotting import plot_court_3d, text3d
import numpy as np
import pandas as pd
from matplotlib.colors import ListedColormap
from scipy import interpolate


# Helper function to get gaussian kde for plotting - returns X,Y grid and Z density
def get_density(data):
    xmin = min(data[:, 0])
    xmax = max(data[:, 0])
    ymin = min(data[:, 1])
    ymax = max(data[:, 1])

    X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
    positions = np.vstack([X.ravel(), Y.ravel()])

    kernel = gaussian_kde(data.T, bw_method=0.35)
    Z = np.reshape(kernel(positions).T, X.shape)
    return X, Y, Z


# Helper function to integrate increasing alpha into cmap i.e. transparent when low and opaque when high
def cmap_alpha(min_colour, max_colour):
    # Choose colormap
    cmap = ListedColormap(max_colour, min_colour)

    # Get the colormap colors
    alpha_cmap = cmap(np.arange(cmap.N))

    # Set alpha
    alpha_cmap[:, -1] = np.linspace(0, 1, cmap.N)

    # Create new colormap
    alpha_cmap = ListedColormap(alpha_cmap)
    return alpha_cmap


# Helper function to fit a parabola curve (not surface) to date on a 3D axis - we'll use scipy spline functionality
def fit_parabola3d(x, y, z, npoints):
    #t = np.linspace(0, len(x) - 1, len(x) - 1)
    x = x
    y = y
    z = z

    tck, u = interpolate.splprep([x, y, z], s=1, k=len(x) - 1)
    u_fine = np.linspace(0, 1, npoints)
    x_fine, y_fine, z_fine = interpolate.splev(u_fine, tck)

    return x_fine, y_fine, z_fine


# ---------- DATA PREPARATION -----------------------

# Import data
pbp_data = pd.read_csv('data/french_open_mensfinal_pbp.csv')
tracking_data = pd.read_csv('data/french_open_mensfinal_tracking.csv')

# Define cutoff for serves to plot - outside of these we'll class as wayward
cutoff_x = 7.4  # box x + 1m
cutoff_y = 6.487  # box y + 1m

# Anything outside cut-off can be classed as wayward and we'll filter out net faults
djokovic_1stserves = pbp_data[(pbp_data['server_id'] == 9801) &
                              (pbp_data['serve_num'] == 1) &
                              (pbp_data['error_type'] != 'Net Error') &
                              (abs(pbp_data['x_serve_bounce']) <= cutoff_x) &
                              (abs(pbp_data['y_serve_bounce']) <= cutoff_y)]

# We'll extract aces as well and find their point_ids for lookup with detailed tracking
djokovic_aces = djokovic_1stserves[djokovic_1stserves['is_ace'] == 1]
track_ids = list(djokovic_aces['point_ID'])

# We'll get the x,y data for the bounce points of serves split into deuce and ad court
# We'll be plotting the bounce on the positive co-ordinates side of the x axis, so we must flip x and y for serves
# landing on the opposite side

xy_deuce = np.array(
    djokovic_1stserves[djokovic_1stserves['court_side'] == 'DeuceCourt'][['x_serve_bounce', 'y_serve_bounce']])
flipped = xy_deuce[:, 0] < 0
xy_deuce[flipped] = 0 - xy_deuce[flipped]

xy_ad = np.array(
    djokovic_1stserves[djokovic_1stserves['court_side'] == 'AdCourt'][['x_serve_bounce', 'y_serve_bounce']])
flipped = xy_ad[:, 0] < 0
xy_ad[flipped] = 0 - xy_ad[flipped]

# ------------------ PLOTTING ----------------------------

fig = plt.figure()
fig.set_size_inches(20, 20)
fig.subplots_adjust(left=0, right=1, bottom=-0.1, top=1.4)  # Get rid of some excess whitespace - adjust to taste

ax = plt.gca(projection='3d')  # We'll plot on a 3D axis

# Define some styling
court_colour = (0.603, 0.184, 0.035, 1)
ace_colour = 'pink'
deuce_textcolor = (0.203, 0.435, 0.325, 0.5)
ad_textcolor = (0.886, 0.454, 0.070, 0.5)

# Generate a tennis court
plot_court_3d(ax, court_colour=court_colour, netcord_colour='ivory', netpost_colour='black')

# Plot some text on the surface of the court - text angle is in radians
text3d(ax, (8, -4, 0),
       'Djokovic 1st Serve Locations',
       zdir="z", size=0.65, usetex=False, angle=np.pi / 2,
       facecolor=(0, 0, 0, 0.6), edgecolor=(0, 0, 0, 0.6))

text3d(ax, (3, -3.2, 0),
       'Ad Court',
       zdir="z", size=0.6, usetex=False, angle=np.pi / 2,
       facecolor=ad_textcolor, edgecolor=ad_textcolor, )

text3d(ax, (3, 0.42, 0),
       'Deuce Court',
       zdir="z", size=0.6, usetex=False, angle=np.pi / 2,
       facecolor=deuce_textcolor, edgecolor=deuce_textcolor)

text3d(ax, (14, 5, 0),
       'Aces',
       zdir="z", size=0.45, usetex=False, angle=np.pi / 2,
       facecolor='black', edgecolor='black')

# Set the "camera" position
ax.view_init(elev=20, azim=10)

# Plot some contour maps on the court for the service bounce points
X, Y, Z_deuce = get_density(xy_deuce)
ax.contour(X, Y, Z_deuce, 10, cmap=cmap_alpha(court_colour, 'teal'), linestyles="solid", offset=0)

X, Y, Z_ad = get_density(xy_ad)
ax.contour(X, Y, Z_ad, 10, cmap=cmap_alpha(court_colour, 'orange'), linestyles="solid", offset=0)

# Plot the bounce points as a scatter
ax.scatter(xy_deuce[:, 0], xy_deuce[:, 1], c='teal', edgecolor='black', alpha=0.5)
ax.scatter(xy_ad[:, 0], xy_ad[:, 1], c='orange', edgecolor='black', alpha=0.5)

# Plot the aces as lines with interpolated ball tracking - note this is not the real ball physics!
for id in track_ids:

    # Get the aces from the tracking data
    data = tracking_data[tracking_data['point_ID'] == id]

    # Flip relevant serves so they all from one end
    if data.iloc[0]['x'] > 0:
        data.loc[:, ['x', 'y']] = data.loc[:, ['x', 'y']] * -1

    # Plot separate curves for the down phase and up phase of the ball, to mimic a bouncing ball trajectory
    data_down = data.iloc[0:3, :]
    down_x, down_y, down_z = fit_parabola3d(data_down['x'], data_down['y'], data_down['z'], 100)
    data_up = data.iloc[2:, :]
    up_x, up_y, up_z = fit_parabola3d(data_up['x'], data_up['y'], data_up['z'], 100)

    x = np.concatenate([down_x, up_x])
    y = np.concatenate([down_y, up_y])
    z = np.concatenate([down_z, up_z])

    # Plot each line with circular marker
    ax.plot(x, y, z, c=ace_colour, linestyle='None', marker='o', linewidth=3, markevery=2, markersize=3, alpha=0.5)

# We'll plot the ball tracking key on the court as opposed to a matplotlib legend
key_nmarkers = 7  # Number of markers
key_y = np.linspace(4.75, 6.25, key_nmarkers)  # Evenly spaced y axis

# Plot the key as a line plot segment with circular marker as per the actual tracking plots
ax.plot(np.repeat(13.3, key_nmarkers), key_y, np.repeat(0, key_nmarkers), c=ace_colour, linestyle='None',
        marker='o', linewidth=3, markevery=1, markersize=3, alpha=0.5)

plt.show()
