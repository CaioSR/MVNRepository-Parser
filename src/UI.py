from tkinter import *
from tkinter import filedialog
from mvnScrapper import MVNscrapper
import configparser
import os
import time

class Interface:
    repo = None
    project_link = None
    max_depth = None
    progress_dir = None
    final_dir = None

    available_repo = ['MVNRepository']

    def __init__(self):
        self.home()

    def home(self, ui = None):
        try:
            ui.destroy()
        except:
            pass

        ui = Tk()
        ui.title("Deps Ahoy")

        description_frame = Frame(ui)
        description_frame.grid(row=0, column=1)

        description_label = Label(description_frame, text="""      Deps Ahoy is a parser for online stored projects.
  This operation will extract dependencies from the selected
  project, from its dependencies, and from projects that
  use the selected project.

      The result will be two files that compose a direct
  oriented graph in which the nodes are the projects and
  the links are the dependencies relations (one file for
  nodes, and one file for links). The operation may take a
  long time depending on how deep you choose to parse.

      This tool does not display the graph. You must import
  the files generated to a visualization tool of your choice.
  You'll have the option to adapt the resulting files to a
  format accepted by Gephi (which is a visualization tool),
  when starting a new operation or after one is already
  finished, should you choose to do so.""", font='arial 10', justify=LEFT)
        description_label.pack(padx=5,pady=5)

        buttons_frame = Frame(ui)
        buttons_frame.grid(row=0, column=0, sticky=N)
        new_op_button = Button(buttons_frame, anchor='nw', width=20, text="New operation", command=lambda : self.iniateNewOP(ui))
        new_op_button.grid(row=0, column=0, padx=5, pady=5)
        load_op_button = Button(buttons_frame, anchor='nw', width=20, text="Load operation", command=lambda : self.loadOP(ui))
        load_op_button.grid(row=1, column=0, padx=5, pady=5)
        alter_file_button = Button(buttons_frame, anchor='nw', width=20, text="Alter files")
        alter_file_button.grid(row=2, column=0, padx=5, pady=5)

        ui.mainloop()

    def iniateNewOP(self, ui):
        ui.destroy()
        ui = Tk()
        ui.title("Deps Ahoy")

        self.repository_input = StringVar()
        self.repository_input.set('MVNRepository')
        self.repo = self.repository_input.get()

        repository_confirm_label = Label(ui, anchor='e', width=20, text="Repository: ")
        repository_confirm_label.grid(row=0, column=0, padx=5, pady=5)
        repository_input_menu = OptionMenu(ui, self.repository_input, *self.available_repo)
        repository_input_menu.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        self.repository_input.trace('w', self.setRepo) #observer

        depth_confirm_label = Label(ui, anchor='e', width=20, text="Maximum depth search: ")
        depth_confirm_label.grid(row=1, column=0, padx=5, pady=5)
        depth_input = StringVar()
        depth_input_box = Entry(ui, width=10, textvariable=depth_input)
        depth_input_box.grid(row=1, column=1, sticky='w', padx=5, pady=5)

        project_confirm_label = Label(ui, anchor='e', width=20, text="Project link with version: ")
        project_confirm_label.grid(row=2, column=0, padx=5, pady=5)
        project_input = StringVar()
        project_input_box = Entry(ui, width=50, textvariable=project_input)
        project_input_box.grid(row=2, column=1, sticky='w', padx=5, pady=5)

        progress_file_dir = Label(ui, anchor='e', width=20, text="Progress files directory: ")
        progress_file_dir.grid(row=3, column=0, padx=5, pady=5)
        progress_dir_input = StringVar(value = os.getcwd().replace('\\', '/') + '/prog-manag/')
        progress_dir_input = Entry(ui, width=50, textvariable=progress_dir_input)
        progress_dir_input.grid(row=3, column=1, sticky='w', padx=5, pady=5)

        final_file_dir = Label(ui, anchor='e', width=20, text="Progress files directory: ")
        final_file_dir.grid(row=4, column=0, padx=5, pady=5)
        final_dir_input = StringVar(value = os.getcwd().replace('\\', '/') + '/final/')
        final_dir_input = Entry(ui, width=50, textvariable=final_dir_input)
        final_dir_input.grid(row=4, column=1, sticky='w', padx=5, pady=5)

        previous_screen_button = Button(ui, width=20, text="Return to home", command=lambda : self.home(ui))
        previous_screen_button.grid(row=5, column=0, sticky='w', padx=5, pady=5)

        confirm_button = Button(ui, width=20, text="Begin Parse", command=lambda : self.finalize(ui, project_input, depth_input, progress_dir_input, final_dir_input))
        confirm_button.grid(row=5, column=1, sticky='e', padx=5, pady=5)

        ui.mainloop()

    def loadOP(self, ui):
        opDirectory = filedialog.askdirectory(initialdir = "./", title = "Select desired operation progress management folder")
        #askopenfilename(filetypes=[("python files","*.py"),("all files", "*.*")])
        folders = opDirectory.split('/')
        config = configparser.ConfigParser()
        config.read(opDirectory+'/config.ini')
        self.repo = config.get('Operation Atributes', 'repository')
        self.project_link = config.get('Operation Atributes', 'project link')
        self.max_depth = int(config.get('Operation Atributes', 'maximum depth'))
        self.final_dir = config.get('Operation Atributes', 'end directory')
        self.progress_dir = folders[:-1]
        if self.repo == 'MVNRepository':
            scrapper = MVNscrapper(self.project_link, self.max_depth, self.final_dir, self.progress_dir)
        
        self.initiateOP(scrapper)

    def setRepo(self, *args):
        self.repo = self.repository_input.get()

    def setAttributes(self, project, depth, progress, final):
        self.project_link = project.get()
        self.max_depth = int(depth.get())
        self.progress_dir = progress.get()
        self.final_dir = final.get()

    def initiateOP(self, scrapper):
        scrapper.scrapper()

    def finalize(self, ui, project, depth, prog_dir, final_dir):
        self.setAttributes(project, depth, prog_dir, final_dir)
        ui.destroy()
        self.printAll()
        if self.repo == 'MVNRepository':
            scrapper = MVNscrapper(self.project_link, self.max_depth, self.final_dir, self.progress_dir)
        self.initiateOP(scrapper)

    def printAll(self):
        print('Repository: ',self.repo)
        print('Project:', self.project_link)
        print('Maximum Depth Search: ', self.max_depth)
        print('Directory to progress files: ', self.progress_dir)
        print('Directory to final files: ', self.final_dir)
