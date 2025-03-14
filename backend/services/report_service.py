import subprocess
import os

class UnregisteredUserPDFMaker:
    def __init__(self, output_file):
        self.output_file = output_file  # Must be a .tex file
        self.driver_name = None  # Placeholder value
        self.summary_text = None

    def generate_latex_content(self):
        """Generates base LaTeX content for unregistered users."""
        return """
        \\documentclass{{article}}
        \\usepackage{{graphicx}}
        \\usepackage{{lipsum}}

        \\begin{{document}}

        % Title with dynamic driver name
        \\title{{{}}}
        \\maketitle

        % Placeholder for first image or blank space if missing
        \\section{{Telemetry Visualization}}
        \\begin{{figure}}[h]
            \\centering
            \\IfFileExists{{image1.png}}{{
                \\includegraphics[width=0.8\\textwidth]{{image1.png}}
                \\caption{{Speed vs Distance Plot}}
                \\label{{fig:speed_plot}}
            }}{{
                \\vspace{{5cm}}  % Blank space if image is missing
            }}
        \\end{{figure}}

        {}  % Extra images for registered users

        % Placeholder for injected text or lorem ipsum if missing
        \\section{{Analysis Summary}}
        {}

        \\end{{document}}
        """.format(self.get_title(), self.get_additional_images(), self.summary_text if self.summary_text else '\\lipsum[1]')

    def get_title(self):
        """Returns the base title for unregistered users."""
        return f"Analysis of {self.driver_name}'s Telemetry Data"

    def get_additional_images(self):
        """Returns an empty string for unregistered users (no extra images)."""
        return f""

    def generate_pdf(self, driver_name, summary_text):
        """Generates the LaTeX file and compiles it into a PDF."""
        self.driver_name = driver_name
        self.summary_text = summary_text
        tex_file = self.output_file.replace(".pdf", ".tex")

        # Write LaTeX content to file
        with open(tex_file, "w") as file:
            file.write(self.generate_latex_content())

        print(f"LaTeX file '{tex_file}' created successfully.")

        # Compile LaTeX to PDF
        subprocess.run(["pdflatex", tex_file], check=True)
        print("PDF generated successfully.")

        # Clean up extra files
        self.cleanup_latex_files(tex_file)

    def cleanup_latex_files(self, tex_file):
        """Removes auxiliary LaTeX files after compilation."""
        base_name = tex_file.replace(".tex", "")
        extensions_to_remove = [".aux", ".log", ".out", ".tex"]

        for ext in extensions_to_remove:
            file_path = base_name + ext
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")


class RegisteredUserPDFMaker(UnregisteredUserPDFMaker):
    def get_title(self):
        """Modifies the title for registered users."""
        return f"Analysis of {self.driver_name}'s Telemetry Data Compared to You"

    def get_additional_images(self):
        """Adds a second image for registered users."""
        return f"""
        % Placeholder for second image or blank space if missing
        \\begin{{figure}}[h]
            \\centering
            \\IfFileExists{{image2.png}}{{
                \\includegraphics[width=0.8\\textwidth]{{image2.png}}
                \\caption{{Throttle and Brake Data}}
                \\label{{fig:throttle_brake}}
            }}{{
                \\vspace{{5cm}}  % Blank space if image is missing
            }}
        \\end{{figure}}
        """
