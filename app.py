import customtkinter   
from tkinter import END
import util
from pathlib import Path

class ReplaceFrame(customtkinter.CTkFrame):
    def __init__(self, master, values):
        super().__init__(master)
        self.text_box_arry = []
        self.values = values

        for i, value in enumerate(self.values):

            label = customtkinter.CTkLabel(self, text=value)
            label.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="n")

            entry = customtkinter.CTkEntry(self, width=250)
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
        return output

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.home_folder = Path.home() / "find_and_replace"
        self.home_folder.mkdir(parents=True, exist_ok=True)

        self.config_folder = self.home_folder / "config"
        self.config_folder.mkdir(parents=True, exist_ok=True)

        self.template_folder = self.home_folder / "template"
        self.template_folder.mkdir(parents=True, exist_ok=True)

        self.config_files = []
        self.set_config_files()

        self.current_config = {}
        self.values_to_replace = {}
        self.values_to_replace_frame = None
        self.template_files = []
        
        self.title("Find and Replace")
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.label = customtkinter.CTkLabel(self, text="Please select a config and fill out your varibles", fg_color="transparent")
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky="ewn", columnspan=2)
        
        self.config_optionmenu = customtkinter.CTkOptionMenu(self, values=self.config_files, command=self.optionmenu_callback)
        self.config_optionmenu.grid(row=1, column=0, padx=10, pady=10, sticky="ewn", columnspan=2)

        self.submit_button = customtkinter.CTkButton(self, text="Submit", command=self.submit_button_callback)
        self.submit_button.grid(row=3, column=0, padx=10, pady=10, sticky="ews", columnspan=2)

        self.optionmenu_callback(self.config_optionmenu.get())

    def generate_output_files(self):
        for template in self.template_files:
            output_file = Path(template)
            input_file = self.template_folder / self.get_current_Config_name() /output_file.name
            input_string = util.read_str_from_file(input_file)
            output_string = util.replace_all(input_string, self.values_to_replace)
            util.create_empty_file(output_file)
            util.write_string_to_file(output_file, output_string)

    def get_template_files(self):
        self.template_files = self.current_config["templates"]
        print(f"-----Template Files-----\n{self.template_files}")

    def submit_button_callback(self):
        self.values_to_replace = self.values_to_replace_frame.get()
        print(f"-----Values to Replace------\n{self.values_to_replace}")
        self.generate_output_files()

    def optionmenu_callback(self, choice):
        if self.values_to_replace_frame is not None:
            self.values_to_replace_frame.grid_forget()

        self.set_current_config()
        self.init_values_to_replace()
        self.get_template_files()
        self.values_to_replace_frame = ReplaceFrame(self, values=self.values_to_replace)
        self.values_to_replace_frame.grid(row=2, column=0, padx=10, pady=1, sticky="ewn")

    def set_config_files(self):
        for file in list(self.config_folder.glob("*.toml")):
            self.config_files.append(file.stem)
        
    def set_current_config(self):
        file = Path(self.config_optionmenu.get() + ".toml")
        self.current_config = util.load_config(self.config_folder / file)
    
    def get_current_Config_name(self):
        return self.config_optionmenu.get()
    
    def init_values_to_replace(self):
        self.values_to_replace = {}
        self.set_current_config()
        for value in self.current_config["values_to_replace"]:
            self.values_to_replace[value] = ""        

app = App()
app.mainloop()