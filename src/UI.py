from tkinter import *
import MVNparser
import os

class Interface:
    ui = None
    repo = None
    project_link = None
    version = None
    max_depth = None
    progress_dir = None
    final_dir = None
    description = """
    Deps Ahoy is a parser for online stored
  projects. This operation will extract
  dependencies for the selected project, it's
  dependencies and projects that use the selected
  project. The result will be two files that
  compose a direct oriented graph in which the
  nodes are the projects and the links are the
  dependencies relations (one file for nodes, and
  one file for links). The operation may take a
  while depending on how deep you choose to parse.
    This tool does not construct the graph
  vizualization. You must import the files
  generated to a vizualization tool of your
  choise. You'll have the option to adapt the
  resulting files to a format accepeted by Gephi
  (which is a powerful vizualition tool),  when
  starting a new operation or after one is
  already finished, should you choose to do so."""


    available_repo = ['MVNRepository', 'Central Maven']

    def __init__(self):
        self.home()

    def home(self):
        try:
            self.ui.destroy()
        except:
            pass

        self.ui = Tk()
        self.ui.title("Deps Ahoy")

        description_frame = Frame(self.ui)
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

        # description_text = Text(description_frame, height=20, width=50, pady=20)
        # description_text.insert(INSERT,self.description)
        # description_text.config(state='disabled', wrap='word')
        # description_text.pack(padx=5, pady=5)


        buttons_frame = Frame(self.ui)
        buttons_frame.grid(row=0, column=0, sticky=N)
        new_op_button = Button(buttons_frame, anchor='nw', width=20, text="New operation", command=lambda : self.iniateNewOP())
        new_op_button.grid(row=0, column=0, padx=5, pady=5)
        load_op_button = Button(buttons_frame, anchor='nw', width=20, text="Load operation")
        load_op_button.grid(row=1, column=0, padx=5, pady=5)
        alter_file_button = Button(buttons_frame, anchor='nw', width=20, text="Alter files")
        alter_file_button.grid(row=2, column=0, padx=5, pady=5)

        self.ui.mainloop()


    def iniateNewOP(self):
        self.ui.destroy()
        self.ui = Tk()
        self.ui.title("Deps Ahoy")

        self.repository_input = StringVar()
        self.repository_input.set('MVNRepository')
        self.repo = self.repository_input.get()

        repository_confirm_label = Label(self.ui, anchor='e', width=20, text="Repository: ")
        repository_confirm_label.grid(row=0, column=0, padx=5, pady=5)
        repository_input_menu = OptionMenu(self.ui, self.repository_input, *self.available_repo)
        repository_input_menu.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        self.repository_input.trace('w', self.setRepo) #observer

        depth_confirm_label = Label(self.ui, anchor='e', width=20, text="Maximum depth search: ")
        depth_confirm_label.grid(row=1, column=0, padx=5, pady=5)
        depth_input = StringVar()
        depth_input_box = Entry(self.ui, width=10, textvariable=depth_input)
        depth_input_box.grid(row=1, column=1, sticky='w', padx=5, pady=5)

        project_confirm_label = Label(self.ui, anchor='e', width=20, text="Project link with version: ")
        project_confirm_label.grid(row=2, column=0, padx=5, pady=5)
        project_input = StringVar()
        project_input_box = Entry(self.ui, width=50, textvariable=project_input)
        project_input_box.grid(row=2, column=1, sticky='w', padx=5, pady=5)

        progress_file_dir = Label(self.ui, anchor='e', width=20, text="Progress files directory: ")
        progress_file_dir.grid(row=3, column=0, padx=5, pady=5)
        #progress_dir_input = StringVar(value = os.getcwd() + '/prog-manag/')
        progress_dir_input = StringVar(value = 'D:/path/to/current/directory/prog-manag/')
        #progress_dir_input = progress_dir_input.replace('\\', '/')
        progress_dir_input = Entry(self.ui, width=50, textvariable=progress_dir_input)
        progress_dir_input.grid(row=3, column=1, sticky='w', padx=5, pady=5)

        final_file_dir = Label(self.ui, anchor='e', width=20, text="Progress files directory: ")
        final_file_dir.grid(row=4, column=0, padx=5, pady=5)
        #final_dir_input = StringVar(value = os.getcwd() + '/final/')
        final_dir_input = StringVar(value = 'D:/path/to/current/directory/final/')
        #final_dir_input = final_dir_input.replace('\\', '/')
        final_dir_input = Entry(self.ui, width=50, textvariable=final_dir_input)
        final_dir_input.grid(row=4, column=1, sticky='w', padx=5, pady=5)

        previous_screen_button = Button(self.ui, width=20, text="Return to home", command=lambda : self.home())
        previous_screen_button.grid(row=5, column=0, sticky='w', padx=5, pady=5)

        confirm_button = Button(self.ui, width=20, text="Begin Parse", command=lambda : self.finalize(project_input, depth_input, progress_dir_input, final_dir_input))
        confirm_button.grid(row=5, column=1, sticky='e', padx=5, pady=5)

        self.ui.mainloop()

    def setRepo(self, *args):
        self.repo = self.repository_input.get()

    def setProject(self, project):
        self.project_link = project

    def setVersion(self, version):
        self.version = version

    def setMaxDepth(self, depth):
        self.max_depth = int(depth)

    def setProgressDir(self, prog_dir):
        self.progress_dir = prog_dir

    def setFinalDir(self, final_dir):
        self.final_dir = final_dir

    def initiateOP(self):
        parse = MVNparser.MVNrepo(self.project_link, self.max_depth, self.final_dir, self.progress_dir)

    def finalize(self, project, depth, prog_dir, final_dir):
        self.setProject(project.get())
        self.setMaxDepth(depth.get())
        self.setProgressDir(prog_dir.get())
        self.setFinalDir(final_dir.get())
        self.printAll()
        self.ui.destroy()
        self.initiateOP()

    def printAll(self):
        print('Repository: ',self.repo)
        print('Project:', self.project_link)
        print('Maximum Depth Search: ', self.max_depth)
        print('Directory to progress files: ', self.progress_dir)
        print('Directory to final files: ', self.final_dir)

    def retrievePrevious(self):
        pass
