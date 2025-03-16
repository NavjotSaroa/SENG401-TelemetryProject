import matplotlib
matplotlib.use("Agg") # For macos setups
from matplotlib import pyplot as plt
from services.styling import StyleManager

class Plotter():
    @staticmethod
    def plotting(car_data, circuit_info):
        """
        Produces basic plot given car_data, and circuit_info

        Args:
            - car_data: Telemetry data for the driver from their fastest lap
            - circuit_info: Circuit specific data

            These arguments are produced in ff1_interact.FF1_Interact.request_telemetry

        Returns:
            - metadata: Dictionary of data required to produce and style a plot
                - fig
                - ax
                - lines
                - corners (corner markers)
        """

        fig, ax = plt.subplots(4, 1, figsize=(10, 8))   # Initialise subplots
        metadata = {}   # Create dictionary to return for customisation

        # Plot the data and save the lines object for future customisation
        metadata["lines"] = Plotter.plot_lines(fig, ax, car_data)

        # Corner markers added here (vertical lines), and annotations
        metadata["corners"] = Plotter.add_corner_markers(ax, circuit_info)

        # Adding labels
        ylabels = ["Speed (km/h)", "Throttle (%)", "Brake (%)", "nGear"]
        xlabel = "Distance (m)"
        Plotter.add_labels(ax, ylabels, xlabel)

        # Formatting axes (adding tickers, removing borders, etc)
        Plotter.format_axes(ax, car_data)

        # Add fig and ax to metadata so plots can be styled later
        metadata['fig'], metadata['ax'] = fig, ax 

        return metadata

    def plot_lines(fig, ax, car_data):
        """
        Plots the basic lines for the telemetry data in subplots

        Args:
            - fig: Automatically generated when plt.subplots is called
            - ax: Automatically generated when plt.subplots is called
            - car_data: Telemetry data for the driver from their fastest lap

        Returns:
            - lines: dictionary of plots
        """

        lines = {}
        lines["Speed"]      = ax[0].plot(car_data["Distance"], car_data["Speed"], linewidth = 1.5)[0]
        lines["Throttle"]   = ax[1].plot(car_data["Distance"], car_data["Throttle"], linewidth = 1.5)[0]
        lines["Brake"]      = ax[2].plot(car_data["Distance"], car_data["Brake"], linewidth = 1.5)[0]
        lines["nGear"]      = ax[3].plot(car_data["Distance"], car_data["nGear"], linewidth = 1.5)[0]

        return lines

    def add_corner_markers(ax, circuit_info):
        """
        Adds the lines marking corners on the plot and the text labelling them.

        Args:
            - ax: Automatically generated when plt.subplots is called
            - circuit_info: Circuit specific data

        Returns:
            - corner_data: List of text objects produced in matplotlib
        """

        for distance in circuit_info.corners["Distance"]:
            for axis in ax:
                axis.axvline(
                    x=distance, 
                    color="grey", 
                    alpha=1, 
                    linewidth=0.7
                )

        corner_data = []
        for _, corner in circuit_info.corners.iterrows():
            txt = f"{corner['Number']}" # Define text for corner numbers
            corner_nums =  ax[0].text(corner["Distance"], 1.1, txt, # Place text on plot
                va ="top", 
                ha ="center", 
                fontsize = 8, 
                color = "black", 
                transform = ax[0].get_xaxis_transform()
            )

            corner_data.append(corner_nums) # Add Text object to list for future customisations

        return corner_data
    
    def add_labels(ax, ylabels, xlabel):
        """
        Adds labels to the axes of the subplots

        Args:
            - ax: Automatically generated when plt.subplots is called
            - ylabels: List(str)
            - xlabel: str

        Returns:
            None
        """
        for i, label in enumerate(ylabels):
            ax[i].set_ylabel(label)
        
        ax[i].set_xlabel(xlabel)

        return

    def format_axes(ax, car_data):
        """
        Formats the axes of the plots

        Args:
            - ax: Automatically generated when plt.subplots is called
            - car_data: Telemetry data for the driver from their fastest lap

        Returns:
            None
        """

        x_min, x_max = car_data["Distance"].min(), car_data["Distance"].max()   # Find bounds of data
        for i, axis in enumerate(ax):
            axis.grid(True, linestyle="--", alpha=0.3)  # Add grid (dashed lines)
            axis.set_xlim(x_min, x_max)                 # Remove empty space from sides of plots
            if i < len(ax) - 1: # Get rid of ticks from all graphs but the last
                axis.set_xticks([])        
                axis.set_xticklabels([])   
                axis.spines['bottom'].set_visible(False)

        return

    @staticmethod
    def styling(metadata, theme):
        """
        Customises plot given pre-designed themes

        Args:
            - metadata: Data of baseline plot that is to be styled, retrieved from Plotter.plotting
            - theme: str, user's choice

        Returns:
            None
        """

        try:
            style_manager = StyleManager(metadata)
            themes = {
                "cyberpunk": style_manager.make_cyberpunk,
                "barbie": style_manager.make_barbie
                # TODO: Add more themes
            }
        except Exception as e:
            raise RuntimeError

        try:
            themes[theme]()
        except KeyError as e:
            print(f"Error {e}")
            
        return
    
