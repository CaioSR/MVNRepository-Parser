from MVNScrapper import MVNScrapper
from Addons import Addons
import os
import time
import threading
import configparser
import tkinter as tk
import tkinter.filedialog

class Home:
    def __init__(self, root):
        self._root = root
        self._root.title("Deps Ahoy")

        description_frame = tk.Frame(self._root)
        description_frame.grid(row=0, column=1)

        description_label = tk.Label(description_frame, text="""      Deps Ahoy is a parser for online stored projects.
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
  format accepted by Gephi (which is a visualization tool)
  by clicking on the Add Ids option after a search is already
  finished, should you choose to do so.""", font='arial 10', justify=tk.LEFT)
        description_label.pack(padx=5,pady=5)

        buttons_frame = tk.Frame(self._root)
        buttons_frame.grid(row=0, column=0, sticky=tk.N)
        new_op_button = tk.Button(buttons_frame, anchor='nw', width=20, text="New operation", command=lambda : self._openNewOperationWindow())
        new_op_button.grid(row=0, column=0, padx=5, pady=5)
        load_op_button = tk.Button(buttons_frame, anchor='nw', width=20, text="Load operation", command=lambda : self._loadOperation())
        load_op_button.grid(row=1, column=0, padx=5, pady=5)
        merge_button = tk.Button(buttons_frame, anchor='nw', width=20, text="Merge files", command=lambda : self._openMergeWindow())
        merge_button.grid(row=2, column=0, padx=5, pady=5)
        addId_button = tk.Button(buttons_frame, anchor='nw', width=20, text="Add IDs", command=lambda : self._addId())
        addId_button.grid(row=3, column=0, padx=5, pady=5)

    def _openNewOperationWindow(self):
        self._newOpWindow = NewOperationWindow(self._root)

    def _loadOperation(self):
        opDirectory = tk.filedialog.askdirectory(initialdir = "./", title="Select desired operation progress management folder")
        #askopenfilename(filetypes=[("python files","*.py"),("all files", "*.*")])
        folders = opDirectory.split('/')
        config = configparser.ConfigParser()
        config.read(opDirectory+'/config.ini')
        repo = config.get('Operation Atributes', 'repository')
        project_url = config.get('Operation Atributes', 'project_link')
        max_depth = int(config.get('Operation Atributes', 'maximum_depth'))
        final_dir = config.get('Operation Atributes', 'end_directory')
        progress_dir = '/'.join(folders[:-1])

        ScrapperCaller.callScrapper(project_url, max_depth, progress_dir, final_dir, repo)

    def _openMergeWindow(self):
        self._mergeWindow = MergeOperationWindow(self._root)

    def _addId(self):
        self._addIdWindow = AddIdOperationWindow(self._root)

class NewOperationWindow:
    _available_repos = ['MVNRepository']

    def __init__(self, parent):
        self._parent = parent
        self._parent.withdraw()
        self._root = tk.Toplevel(self._parent)
        self._root.title("Deps Ahoy")

        repository_input = tk.StringVar()
        repository_input.set('MVNRepository')

        repository_confirm_label = tk.Label(self._root, anchor='e', width=20, text="Repository: ")
        repository_confirm_label.grid(row=0, column=0, padx=5, pady=5)
        repository_input_menu = tk.OptionMenu(self._root, repository_input, *self._available_repos)
        repository_input_menu.grid(row=0, column=1, sticky='w', padx=5, pady=5)

        depth_confirm_label = tk.Label(self._root, anchor='e', width=20, text="Maximum depth search: ")
        depth_confirm_label.grid(row=1, column=0, padx=5, pady=5)
        depth_input = tk.StringVar()
        depth_input_box = tk.Entry(self._root, width=10, textvariable=depth_input)
        depth_input_box.grid(row=1, column=1, sticky='w', padx=5, pady=5)

        project_confirm_label = tk.Label(self._root, anchor='e', width=20, text="Project link with version: ")
        project_confirm_label.grid(row=2, column=0, padx=5, pady=5)
        project_input = tk.StringVar()
        project_input_box = tk.Entry(self._root, width=50, textvariable=project_input)
        project_input_box.grid(row=2, column=1, sticky='w', padx=5, pady=5)

        progress_file_dir = tk.Label(self._root, anchor='e', width=20, text="Management directory: ")
        progress_file_dir.grid(row=3, column=0, padx=5, pady=5)
        progress_dir_input = tk.StringVar(value = os.getcwd().replace('\\', '/') + '/test_files/prog-manag/')
        progress_dir_input = tk.Entry(self._root, width=50, textvariable=progress_dir_input)
        progress_dir_input.grid(row=3, column=1, sticky='w', padx=5, pady=5)
        progress_dir_choose = tk.Button(self._root, width=3, text="...", command=lambda : self._chooseDirectory())
        progress_dir_choose.grid(row=3, column=2, sticky='w', padx=5, pady=5)

        final_file_dir = tk.Label(self._root, anchor='e', width=20, text="Final directory: ")
        final_file_dir.grid(row=4, column=0, padx=5, pady=5)
        final_dir_input = tk.StringVar(value = os.getcwd().replace('\\', '/') + '/test_files/final/')
        final_dir_input = tk.Entry(self._root, width=50, textvariable=final_dir_input)
        final_dir_input.grid(row=4, column=1, sticky='w', padx=5, pady=5)
        final_dir_choose = tk.Button(self._root, width=3, text="...", command=lambda : self._chooseDirectory())
        final_dir_choose.grid(row=4, column=2, sticky='w', padx=5, pady=5)

        previous_screen_button = tk.Button(self._root, width=20, text="Return to home", command=lambda : self._closeWindow())
        previous_screen_button.grid(row=5, column=0, sticky='w', padx=5, pady=5)

        confirm_button = tk.Button(self._root, width=20, text="Begin Parse", command=lambda : ScrapperCaller.callScrapper(project_input.get(), 
                                                                                            int(depth_input.get()),
                                                                                            progress_dir_input.get(),
                                                                                            final_dir_input.get(),
                                                                                            repository_input.get()))
        confirm_button.grid(row=5, column=1, sticky='e', padx=5, pady=5)

    def _chooseDirectory(self):
        chosenDirectory = tk.filedialog.askdirectory(initialdir="./", title="Choose directory to save")

    def _closeWindow(self):
        self._root.destroy()
        self._parent.deiconify()

class MergeOperationWindow:
    def __init__(self, parent):
        self._parent = parent
        self._parent.withdraw()
        self._root = tk.Toplevel(self._parent)
        instructions = tk.Label(self._root, text="""Choose the directory that contains the projects with the files generated at the end of the search procedure.
        Each project folder must have the Nodes.csv, Links.csv and Config.ini files.
        This will merge each Nodes.csv and Links.csv file, and create a new directory with the 'merge' prefix.
        These 'merged' folders will be ignored by the tool.
        For now, the projects must have been scrapped from the same repository.""")
        instructions.grid(row=0, columnspan=2, padx=5, pady=5)

        previous_screen_button = tk.Button(self._root, text="Return to home", command=lambda : self._closeWindow())
        previous_screen_button.grid(row=1, column=0, sticky='w', padx=5, pady=5)

        choose_directory = tk.Button(self._root, text="Choose directory", command=lambda : self._mergeArtifacts())
        choose_directory.grid(row=1, column=1, sticky='e', padx=5, pady=5)

    def _mergeArtifacts(self):
        mgDirectory = tk.filedialog.askdirectory(initialdir = "./", title="Select the folder that contains the projects to merge")
        dirs = []
        for (_, dirnames, _) in os.walk(mgDirectory):
            dirs.extend(dirnames)
            break

        directories = []
        for dir in dirs:
            if 'merged' not in dir:
                directories.append(dir)
        
        print(directories)

        mgThread = threading.Thread(target=Addons.merge, args=(mgDirectory,directories))
        mgThread.daemon = True
        mgThread.start()
        print('Merging...')

        self._closeWindow()

    def _closeWindow(self):
        self._root.destroy()
        self._parent.deiconify()

class AddIdOperationWindow:
    def __init__(self, parent):
        self._parent = parent
        self._parent.withdraw()
        self._root = tk.Toplevel(self._parent)

        instructions = tk.Label(self._root, text="""Choose the directory that contains of the desired project
to add the Ids to the Nodes and replace the artifacts names
        to their respective Ids in the Links file""")
        instructions.grid(row=0, columnspan=2, padx=5,pady=5)

        previous_screen_button = tk.Button(self._root, text="Return to home", command=lambda : self._closeWindow())
        previous_screen_button.grid(row=1, column=0, sticky='w', padx=5, pady=5)

        choose_directory = tk.Button(self._root, text="Choose directory", command=lambda : self._addId())
        choose_directory.grid(row=1, column=1, sticky='e', padx=5, pady=5)

    def _addId(self):
        idDirectory = tk.filedialog.askdirectory(initialdir = "./", title="Select the folder to add id to Nodes and Links files")
        idThread = threading.Thread(target=Addons.addId, args=(idDirectory,))
        idThread.daemon = True
        idThread.start()
        print('Adding ids...')

        self._closeWindow()
    
    def _closeWindow(self):
        self._root.destroy()
        self._parent.deiconify()

class ScrapperCaller:

    @staticmethod
    def callScrapper(project_url, max_depth, prog_dir, final_dir, repo):
        if repo == 'MVNRepository':
            scrapper = MVNScrapper()
        opThread = threading.Thread(target=scrapper.scrapper, args=(project_url, max_depth, final_dir, prog_dir))
        opThread.daemon = True
        opThread.start()
