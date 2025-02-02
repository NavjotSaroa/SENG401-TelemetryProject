from matplotlib import pyplot as plt
from ff1_interact import FF1_Interact
from styling import StyleManager

class Plotter():
    @staticmethod
    def plotting(car_data, car_info):
        """
        Produces basic plot given car_data, and car_info
        """
        metadata = {} # For things to return for customisation
        metadata["fig"], metadata["ax"] = plt.subplots(4, 1, figsize=(10, 8))
        
        # Plot the data and save the lines object for future customisation
        metadata["lines"] = {}
        metadata["lines"]["Speed"]      = metadata["ax"][0].plot(car_data["Distance"], car_data["Speed"], linewidth = 1.5)[0]
        metadata["lines"]["Throttle"]   = metadata["ax"][1].plot(car_data["Distance"], car_data["Throttle"], linewidth = 1.5)[0]
        metadata["lines"]["Brake"]      = metadata["ax"][2].plot(car_data["Distance"], car_data["Brake"], linewidth = 1.5)[0]
        metadata["lines"]["nGear"]      = metadata["ax"][3].plot(car_data["Distance"], car_data["nGear"], linewidth = 1.5)[0]

        # Corner markers added here (vertical lines)
        for distance in car_info.corners["Distance"]:
            for axis in metadata["ax"]:
                axis.axvline(
                    x=distance, 
                    color="grey", 
                    alpha=1, 
                    linewidth=0.7
                )

        # Add corner annotations below the bottom plot and save them
        metadata["corners"] = []
        for _, corner in car_info.corners.iterrows():
            txt = f"{corner['Number']}"
            corner_nums =  metadata["ax"][0].text(corner["Distance"], 1.1, txt, 
                va ="top", 
                ha ="center", 
                fontsize = 8, 
                color = "black", 
                transform = metadata["ax"][0].get_xaxis_transform()
            )

            metadata["corners"].append(corner_nums)

        # Adding labels, final customisations
        metadata["ax"][0].set_ylabel("Speed (km/h)")
        metadata["ax"][1].set_ylabel("Throttle (%)")
        metadata["ax"][2].set_ylabel("Brake (%)")
        metadata["ax"][3].set_ylabel("nGear")
        metadata["ax"][3].set_xlabel("Distance (m)") 

        x_min, x_max = car_data["Distance"].min(), car_data["Distance"].max()
        for i, axis in enumerate(metadata["ax"]):
            axis.grid(True, linestyle="--", alpha=0.3)
            axis.set_xlim(x_min, x_max)
            if i < len(metadata["ax"]) - 1: # Get rid of ticks from all graphs but the last
                axis.set_xticks([])        
                axis.set_xticklabels([])   
                axis.spines['bottom'].set_visible(False) 

        return metadata
    
    def styling(metadata, theme):
        """
        Customises plot given pre-designed themes
        """
        style_manager = StyleManager(metadata)
        themes = {
            "cyberpunk": style_manager.make_cyberpunk,
            "barbie": style_manager.make_barbie
            # TODO: Add more themes
        }

        try:
            themes[theme]()
        except KeyError as e:
            print(f"Error {e}")
            return 

if __name__ == "__main__":
    session2020 = FF1_Interact.request_telemetry(2018, 'Monaco', 44)
    md= Plotter.plotting(session2020[0], session2020[1])
    print(md, type(md))

    Plotter.styling(md, 'cyberpunk')
    plt.show()