import tkinter as tk
from mvnScrapper import MVNscrapper
import configparser
import os
import time

class Home:
    def __init__(self, root):
        self.root = tk.Tk()
        self.root.title("Deps Ahoy")

        description_frame = tk.Frame(self.root)
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
  format accepted by Gephi (which is a visualization tool),
  when starting a new operation or after one is already
  finished, should you choose to do so.""", font='arial 10', justify=tk.LEFT)
        description_label.pack(padx=5,pady=5)

        buttons_frame = tk.Frame(self.root)
        buttons_frame.grid(row=0, column=0, sticky=tk.N)
        new_op_button = tk.Button(buttons_frame, anchor='nw', width=20, text="New operation", command=lambda : self._open_new_operation_window())
        new_op_button.grid(row=0, column=0, padx=5, pady=5)
        load_op_button = tk.Button(buttons_frame, anchor='nw', width=20, text="Load operation", command=lambda : self._load_operation())
        load_op_button.grid(row=1, column=0, padx=5, pady=5)
        alter_file_button = tk.Button(buttons_frame, anchor='nw', width=20, text="Alter files")
        alter_file_button.grid(row=2, column=0, padx=5, pady=5)

    def _open_new_operation_window(self):
        newOp = NewOperation(self._finalize)
        pass

    def _load_operation(self):
        opDirectory = tk.filedialog.askdirectory(initialdir = "./", title = "Select desired operation progress management folder")
        #askopenfilename(filetypes=[("python files","*.py"),("all files", "*.*")])
        folders = opDirectory.split('/')
        config = configparser.ConfigParser()
        config.read(opDirectory+'/config.ini')
        repo = config.get('Operation Atributes', 'repository')
        project_url = config.get('Operation Atributes', 'project link')
        max_depth = int(config.get('Operation Atributes', 'maximum depth'))
        final_dir = config.get('Operation Atributes', 'end directory')
        progress_dir = '/'.join(folders[:-1])

        self._finalize(project_url, max_depth, progress_dir, final_dir, repo = repo)

    def _finalize(self, project_url, max_depth, prog_dir, final_dir, repo = None):
        # self.setAttributes(project, max_depth, prog_dir, final_dir, repo)
        # self.printAll()
        if repo == 'MVNRepository':
            scrapper = MVNscrapper(project_url, max_depth, final_dir, prog_dir)
        scrapper.scrapper()


class NewOperation:
    _repo = None
    _available_repo = ['MVNRepository']

    def __init__(self, _finalize):
        self.root = tk.Tk()
        self.root.title("Deps Ahoy")

        self.repository_input = tk.StringVar()
        self.repository_input.set('MVNRepository')
        self.repo = self.repository_input.get()

        repository_confirm_label = tk.Label(self.root, anchor='e', width=20, text="Repository: ")
        repository_confirm_label.grid(row=0, column=0, padx=5, pady=5)
        repository_input_menu = tk.OptionMenu(self.root, self.repository_input, *self._available_repo)
        repository_input_menu.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        self.repository_input.trace('w', self._setRepo) #observer

        depth_confirm_label = tk.Label(self.root, anchor='e', width=20, text="Maximum depth search: ")
        depth_confirm_label.grid(row=1, column=0, padx=5, pady=5)
        depth_input = tk.StringVar()
        depth_input_box = tk.Entry(self.root, width=10, textvariable=depth_input)
        depth_input_box.grid(row=1, column=1, sticky='w', padx=5, pady=5)

        project_confirm_label = tk.Label(self.root, anchor='e', width=20, text="Project link with version: ")
        project_confirm_label.grid(row=2, column=0, padx=5, pady=5)
        project_input = tk.StringVar()
        project_input_box = tk.Entry(self.root, width=50, textvariable=project_input)
        project_input_box.grid(row=2, column=1, sticky='w', padx=5, pady=5)

        progress_file_dir = tk.Label(self.root, anchor='e', width=20, text="Progress files directory: ")
        progress_file_dir.grid(row=3, column=0, padx=5, pady=5)
        progress_dir_input = tk.StringVar(value = os.getcwd().replace('\\', '/') + '/prog-manag/')
        progress_dir_input = tk.Entry(self.root, width=50, textvariable=progress_dir_input)
        progress_dir_input.grid(row=3, column=1, sticky='w', padx=5, pady=5)

        final_file_dir = tk.Label(self.root, anchor='e', width=20, text="Progress files directory: ")
        final_file_dir.grid(row=4, column=0, padx=5, pady=5)
        final_dir_input = tk.StringVar(value = os.getcwd().replace('\\', '/') + '/final/')
        final_dir_input = tk.Entry(self.root, width=50, textvariable=final_dir_input)
        final_dir_input.grid(row=4, column=1, sticky='w', padx=5, pady=5)

        previous_screen_button = tk.Button(self.root, width=20, text="Return to home", command=lambda : self.home())
        previous_screen_button.grid(row=5, column=0, sticky='w', padx=5, pady=5)

        confirm_button = tk.Button(self.root, width=20, text="Begin Parse", command=lambda : home._finalize(project_input.get(), int(depth_input.get()), progress_dir_input.get(), final_dir_input.get(), repo = self._repo))
        confirm_button.grid(row=5, column=1, sticky='e', padx=5, pady=5)

    def _setRepo(self, *args):
        self._repo = self.repository_input.get()

    # def setAttributes(self, project, depth, progress, final, repo = None):
    #     if repo:
    #         self.repo = repo
    #     self.project_link = project
    #     self.max_depth = depth
    #     self.progress_dir = progress
    #     self.final_dir = final



    # def printAll(self):
    #     print('Repository: ',self.repo)
    #     print('Project:', self.project_link)
    #     print('Maximum Depth Search: ', self.max_depth)
    #     print('Directory to progress files: ', self.progress_dir)
    #     print('Directory to final files: ', self.final_dir)

if __name__ == '__main__':
    root = tk.Tk()
    deps = Home(root)
    root.mainloop()