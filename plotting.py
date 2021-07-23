""" Module containing tennis court plotting functions"""

from matplotlib import colors
from matplotlib.patches import PathPatch
from matplotlib.text import TextPath
from matplotlib.transforms import Affine2D
import mpl_toolkits.mplot3d.art3d as art3d
import matplotlib.font_manager as fm


def plot_court_3d(ax, court_colour='cornflowerblue', line_colour='white', netpost_colour='black',
                  netcord_colour='ivory'):
    """ Plots a standard tennis court according to regulation dimensions in metres - centre of the court is (0,0)

    ----------
    ax: A matplotlib axis where ax = plt.gca(projection='3d')
        The 3D axes to plot on.
    court_colour: A matplotlib named colour string OR an RGBA (0-1) tuple
        The colour of the court floor.
    line_colour: Any valid matplotlib colour
        The colour of the court line markings.
    netpost_colour: Any valid matplotlib colour
        The colour of the net posts.
    netcord_colour: Any valid matplotlib colour
        The colour of the net cord.

    Returns
    -------
    matplotlib.axes.Axes"""

    COURT_X_BOUND = 15
    COURT_Y_BOUND = 8
    COURT_Z_BOUND = 5

    COURT_LENGTH = 23.77
    COURT_WIDTH_SING = 8.23
    COURT_WIDTH_DOUB = 10.973
    SERVICE_BOX_LENGTH = 6.4

    NET_HEIGHT_POST = 1.07
    NET_HEIGHT_CENTRE = 0.91

    NET_WIDTH = COURT_WIDTH_DOUB + 0.5

    min_h = 0  # Z height to plot court lines - 99% use cases will be ground level i.e. 0

    ax.set_xlim3d([-COURT_X_BOUND, COURT_X_BOUND])
    ax.set_ylim3d([-COURT_Y_BOUND, COURT_Y_BOUND])
    ax.set_zlim3d([0, COURT_Z_BOUND])

    sidelineX = [-COURT_LENGTH / 2, COURT_LENGTH / 2]
    sidelineY = [-COURT_WIDTH_DOUB / 2, -COURT_WIDTH_DOUB / 2]
    sidelineY2 = [COURT_WIDTH_DOUB / 2, COURT_WIDTH_DOUB / 2]
    ax.plot(sidelineX, sidelineY, min_h, c=line_colour)
    ax.plot(sidelineX, sidelineY2, min_h, c=line_colour)

    sing_sidelineX = [-COURT_LENGTH / 2, COURT_LENGTH / 2]
    sing_sidelineY = [-COURT_WIDTH_SING / 2, -COURT_WIDTH_SING / 2]
    sing_sidelineY2 = [COURT_WIDTH_SING / 2, COURT_WIDTH_SING / 2]
    ax.plot(sing_sidelineX, sing_sidelineY, min_h, c=line_colour)
    ax.plot(sing_sidelineX, sing_sidelineY2, min_h, c=line_colour)

    baselineX = [-COURT_LENGTH / 2, -COURT_LENGTH / 2]
    baselineY = [-COURT_WIDTH_DOUB / 2, COURT_WIDTH_DOUB / 2]
    baselineX2 = [COURT_LENGTH / 2, COURT_LENGTH / 2]
    ax.plot(baselineX, baselineY, min_h, c=line_colour)
    ax.plot(baselineX2, baselineY, min_h, c=line_colour)

    servicelineX = [-SERVICE_BOX_LENGTH, -SERVICE_BOX_LENGTH]
    servicelineY = [-COURT_WIDTH_SING / 2, COURT_WIDTH_SING / 2]
    servicelineX2 = [SERVICE_BOX_LENGTH, SERVICE_BOX_LENGTH]
    ax.plot(servicelineX, servicelineY, min_h, c=line_colour)
    ax.plot(servicelineX2, servicelineY, min_h, c=line_colour)

    centrelineX = [-SERVICE_BOX_LENGTH, SERVICE_BOX_LENGTH]
    centrelineY = [0, 0]
    ax.plot(centrelineX, centrelineY, min_h, c=line_colour)

    # Draw baseline centre marker
    x = [COURT_LENGTH / 2, (COURT_LENGTH / 2) - 0.2]
    y = [0, 0]
    x2 = [-COURT_LENGTH / 2, (-COURT_LENGTH / 2) + 0.2]
    ax.plot(x, y, min_h, c=line_colour)
    ax.plot(x2, y, min_h, c=line_colour)

    # Draw net
    x = [0, 0, 0, 0, 0]
    y = [-NET_WIDTH / 2, 0, NET_WIDTH / 2, NET_WIDTH / 2, -NET_WIDTH / 2]
    z = [NET_HEIGHT_POST, NET_HEIGHT_CENTRE, NET_HEIGHT_POST, 0, 0]
    verts = [list(zip(x, y, z))]
    ax.add_collection3d(art3d.Poly3DCollection(verts,
                                               edgecolors=(0.862, 0.862, 0.862, 0.25),
                                               facecolors=(0, 0, 0, 0),
                                               linewidths=0.2,
                                               alpha=0.1,
                                               hatch='+++++'))

    # Draw net post left
    x = [0, 0]
    y = [-NET_WIDTH / 2, -NET_WIDTH / 2]
    z = [0, NET_HEIGHT_POST]
    ax.plot(x, y, z, color=netpost_colour, linewidth=3)

    # Draw net post right
    x = [0, 0]
    y = [NET_WIDTH / 2, NET_WIDTH / 2]
    z = [0, NET_HEIGHT_POST]
    ax.plot(x, y, z, color=netpost_colour, linewidth=3)

    # Draw net cord
    x = [0, 0, 0]
    y = [-NET_WIDTH / 2, 0, NET_WIDTH / 2]
    z = [NET_HEIGHT_POST, NET_HEIGHT_CENTRE, NET_HEIGHT_POST]
    ax.plot(x, y, z, color=netcord_colour, linewidth=3)

    # Get rid of colored axes planes
    # First remove fill
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = True

    # Now set color to white (or whatever is "invisible")
    ax.xaxis.pane.set_edgecolor('w')
    ax.yaxis.pane.set_edgecolor('w')
    ax.zaxis.pane.set_edgecolor('w')

    # We accept either RGBA (0,1) or matplotlib named colour string
    if isinstance(court_colour, str):
        ax.w_zaxis.set_pane_color(colors.to_rgba(court_colour, 1))
    else:
        ax.w_zaxis.set_pane_color(court_colour)

    # Remove grid
    ax.grid(False)

    # Remove tick labels
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])

    # Transparent spines
    ax.w_xaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
    ax.w_yaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
    ax.w_zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))

    # No ticks
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    ax.set_box_aspect((2 * COURT_X_BOUND, 2 * COURT_Y_BOUND, COURT_Z_BOUND))


def text3d(ax, xyz, s, zdir="z", size=None, angle=0, usetex=False, facecolor='black', edgecolor='black', **kwargs):
    """
    https://matplotlib.org/stable/gallery/mplot3d/pathpatch3d.html

    Plots the string *s* on the axes *ax*, with position *xyz*, size *size*,
    and rotation angle *angle*. *zdir* gives the axis which is to be treated as
    the third dimension. *usetex* is a boolean indicating whether the string
    should be run through a LaTeX subprocess or not.  Any additional keyword
    arguments are forwarded to `.transform_path`.

    Note: zdir affects the interpretation of xyz.
    """

    x, y, z = xyz
    if zdir == "y":
        xy1, z1 = (x, z), y
    elif zdir == "x":
        xy1, z1 = (y, z), x
    else:
        xy1, z1 = (x, y), z

    # Load font
    fname = 'fonts/FiraSans-ThinItalic.ttf'
    fp = fm.FontProperties(fname=fname)

    text_path = TextPath((0, 0), s, size=size, usetex=usetex, prop=fp)
    trans = Affine2D().rotate(angle).translate(xy1[0], xy1[1])

    p1 = PathPatch(trans.transform_path(text_path), facecolor=facecolor, edgecolor=edgecolor, fill=True)
    p1.set_alpha(None)  # Very important - needed so alpha is respected
    ax.add_patch(p1)
    art3d.pathpatch_2d_to_3d(p1, z=z1, zdir=zdir)
