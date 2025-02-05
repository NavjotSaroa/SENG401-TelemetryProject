import matplotlib.colors as mcolors
from matplotlib.path import Path
from matplotlib.colors import LinearSegmentedColormap
import json
import os
import numpy as np

class StyleManager():
    def __init__(self, metadata):
        self.fig = metadata["fig"]
        self.ax = metadata["ax"]
        self.lines = metadata["lines"]
        self.corner_nums = metadata["corners"]
        

        # Find the styles.json file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.abspath(os.path.join(script_dir, ".."))
        json_path = os.path.join(parent_dir, "styles.json")

        # Load up the colour schemes for all themes
        with open(json_path, 'r') as file:
            self.styles = json.load(file)

    def make_cyberpunk(self):
        # Get the relevant colour scheme
        color_scheme = self.styles["cyberpunk"]
        self.set_colors(color_scheme)
        # Set the colour of the background as a whole
        self.fig.patch.set_facecolor(color_scheme["OverallBackgorund"])

        for key in self.lines.keys():
            self.lines[key].set_color(color_scheme[key])

            # Assign basic variables
            ax = self.lines[key].axes
            x_data, y_data = self.lines[key].get_data()
            line = self.lines[key]
            xmin, xmax = ax.get_xlim()
            ymin, ymax = ax.get_ylim()
            fill_color = line.get_color()

            ylims = (min(y_data), max(y_data))  # Y-axis limits based on line data
            gradient_start = 'min'
            N_sampling_points = 50
            GRADIENT_OFFSET_MULTIPLIER = 0.2 # Scales how far glow goes down

            """
            The rest of this function has been taken from the mplcyberpunk library and has been
            modified.
            """
            Ay = {"min": ymin, "max": ymax, "top": ylims[1], "bottom": ylims[0], "zero": 0}[
                gradient_start
            ]
            gradient_offset = (ymax - ymin) * GRADIENT_OFFSET_MULTIPLIER  # Control how far the glow extends downward
            extent = [xmin, xmax, ymin, ymax + gradient_offset] 

            # find the visual extend of the gradient
            x, y = line.get_data(orig=False)
            x, y = np.array(x), np.array(y)  # enforce x,y as numpy arrays

            # alpha will be linearly interpolated on scaler(y)
            # {"linear","symlog","logit",...} are currentlty treated the same
            scaler = lambda x: x

            a, b = 0.0, 1.0
            ya, yb = extent[2], extent[3]
            moment = lambda y: (scaler(y) - scaler(ya)) / (scaler(yb) - scaler(ya))
            ys = np.linspace(ya, yb, N_sampling_points)

            k = moment(ys)
            alphas = k * b + (1 - k) * a
            
            rgb = mcolors.colorConverter.to_rgb(fill_color)
            z = np.empty((N_sampling_points, 1, 4), dtype=float)
            z[:, :, :3] = rgb
            z[:, :, -1] = alphas[:, None]

            zorder = line.get_zorder()
            alpha = line.get_alpha()
            alpha = 1.0 if alpha is None else alpha

            im = ax.imshow(z,
                aspect="auto",
                extent=extent,
                alpha=alpha,
                interpolation="bilinear",
                origin="lower",
                zorder=zorder,
            )

            path = line.get_path()
            extras = Path([[xmax, Ay], [xmin, Ay]], np.full(2, Path.MOVETO))
            extras.codes[:] = Path.LINETO
            path = path.make_compound_path(path, extras)
            im.set_clip_path(path, line._transform)

        return

    def make_barbie(self):
        color_scheme = self.styles["barbie"]
        self.set_colors(color_scheme)

        for key in self.lines.keys():
            self.lines[key].set_color(color_scheme[key])  # Apply line colors

            # Assign basic variables
            ax = self.lines[key].axes
            x_data, y_data = self.lines[key].get_data()
            line = self.lines[key]
            ymin, ymax = ax.get_ylim()
            fill_color = line.get_color()

            # Ensure y-axis is set properly to avoid gaps when filling under line
            ax.set_ylim(ymin, ymax)

            # Fill completely to the bottom of the subplot
            ax.fill_between(
                x_data, 
                y_data, 
                y2 = ymin - 0.01 * (ymax - ymin),  
                color = fill_color, 
                alpha = 0.15, # Transparency  
                zorder = line.get_zorder() - 1
            )

        # Create a vertical gradient (top to bottom)
        gradient = np.linspace(0, 1, 256).reshape(-1, 1)

        # Define a custom colormap for pink to white
        custom_cmap = LinearSegmentedColormap.from_list(
            "barbie_cmap",  # Name of the colormap
            [color_scheme["OverallBackgorund"], "#FFFFFF"]  # Gradient from pink to white
        )

        # Apply the gradient to the entire figure
        self.fig.add_axes([0, 0, 1, 1], zorder=-1).imshow(
            gradient,
            aspect="auto",
            cmap=custom_cmap,  # Use your custom colormap
            interpolation="bicubic",
            extent=(0, 1, 0, 1),  # Cover the entire figure
            transform=self.fig.transFigure,
        )
    
        return

    def set_colors(self, color_scheme):
        # Set the colour of the plots
        for axis in self.ax:
            axis.set_facecolor(color_scheme["Background"])
            axis.title.set_color(color_scheme["Text"])  # Title
            axis.xaxis.label.set_color(color_scheme["Text"])  # X-axis label
            axis.yaxis.label.set_color(color_scheme["Text"])  # Y-axis label
            for spine in axis.spines.values():
                spine.set_visible(False)
            for label in axis.get_xticklabels() + axis.get_yticklabels():
                label.set_color(color_scheme["Text"])


        for txt in self.corner_nums:
            txt.set_color(color_scheme["CornerNums"])

        return
