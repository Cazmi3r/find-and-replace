import customtkinter   
from tkinter import END
import util
from pathlib import Path

#TODO I should also make it so the template and output files are specified in the config file.
class ReplaceFrame(customtkinter.CTkFrame):
    def __init__(self, master, values):
        super().__init__(master)
        self.text_box_arry = []
        self.values = values

        for i, value in enumerate(self.values):

            label = customtkinter.CTkLabel(self, text=value)
            label.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="n")

            entry = customtkinter.CTkEntry(self)
            entry.grid(row=i, column=1, padx=10, pady=(10, 0), sticky="n")
            
            self.text_box_arry.append((label, entry))
    
    def get(self) -> dict:
        output = {}
        for touple in self.text_box_arry:
            # Puts curly braces around the key so it can be found in template
            replace_key = f'\u007b{touple[0].cget("text")}\u007d'

            replace_value = touple[1].get()
            replace_value = replace_value.strip()

            output[replace_key] = replace_value
        print(output)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.home_folder = Path.home() / "find_and_replace"
        self.home_folder.mkdir(parents=True, exist_ok=True)

        self.config_folder = self.home_folder / "config"
        self.config_folder.mkdir(parents=True, exist_ok=True)

        self.config_files = self.get_config_files()
        self.file_path = ""
        self.output_path = ""
        self.values_to_replace = {}
        self.values_to_replace_frame = None

        self.title("Find and Replace")
        #self.geometry("400x500")
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)


        self.label = customtkinter.CTkLabel(self, text="Please select a Config!", fg_color="transparent")
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky="ewn", columnspan=2)
        
        self.config_optionmenu = customtkinter.CTkOptionMenu(self, values=self.config_files, command=self.optionmenu_callback)
        self.config_optionmenu.grid(row=1, column=0, padx=10, pady=10, sticky="ewn", columnspan=2)

        self.submit_button = customtkinter.CTkButton(self, text="Submit", command=self.submit_button_callback)
        self.submit_button.grid(row=3, column=0, padx=10, pady=10, sticky="ews", columnspan=2)

        self.optionmenu_callback(self.config_optionmenu.get())
    
        
    def submit_button_callback(self):
        self.values_to_replace = self.values_to_replace_frame.get()
        print(self.values_to_replace)

    def optionmenu_callback(self, choice):
        if self.values_to_replace_frame is not None:
            self.values_to_replace_frame.grid_forget()
        self.init_values_to_replace()
        self.values_to_replace_frame = ReplaceFrame(self, values=self.values_to_replace)
        self.values_to_replace_frame.grid(row=2, column=0, padx=10, pady=1, sticky="ewn")

    #TODO abstract out 'self.config_folder'
    def get_config_files(self):
        output = []
        for file in list(self.config_folder.glob("*.toml")):
            output.append(file.stem)
        return output
    
    def get_current_config(self) -> dict:
        file = Path(self.config_optionmenu.get() + ".toml")
        config = util.load_config(self.config_folder / file)
        return config
    
    def init_values_to_replace(self):
        self.values_to_replace = {}
        config = self.get_current_config()
        for value in config["values_to_replace"]:
            self.values_to_replace[value] = ""        

app = App()
app.mainloop()