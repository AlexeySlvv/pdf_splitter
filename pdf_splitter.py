from tkinter import messagebox
from PyPDF2 import PdfFileReader, PdfFileWriter
import tkinter

class MainWindow(tkinter.Frame):
  def __init__(self, parent) -> None:
    super(MainWindow, self).__init__(parent)
    self.parent = parent
    self.grid(row=0, column=0, sticky=tkinter.NSEW)
    self.init_ui()

  def init_ui(self) -> None:
    from tkinter import Button, Label, Spinbox

    button_input = Button(self, text='Open pdf', command=self.set_input)
    button_input.focus_set()
    self.label_input = Label(self, relief=tkinter.SUNKEN)
    button_output = Button(self, text='Saving directory', command=self.set_output)
    self.label_output = Label(self, relief=tkinter.SUNKEN)
    label_from = Label(self, text='From page', relief=tkinter.GROOVE)
    self.spinbox_from = Spinbox(self)
    label_to = Label(self, text='To page', relief=tkinter.GROOVE)
    self.spinbox_to = Spinbox(self)
    button_do = Button(self, text='Split pdf', command=self.do)
    self.label_do = Label(self, relief=tkinter.GROOVE)
    button_quit = Button(self, text='Quit', command=self.quit)
    
    button_input.grid(row=0, column=0, padx=3, pady=3, sticky=tkinter.NSEW)
    self.label_input.grid(row=0, column=1, columnspan=3, padx=3, pady=3, sticky=tkinter.NSEW)
    button_output.grid(row=1, column=0, padx=3, pady=3, sticky=tkinter.NSEW)
    self.label_output.grid(row=1, column=1, columnspan=3, padx=3, pady=3, sticky=tkinter.NSEW)
    label_from.grid(row=2, column=0, padx=3, pady=3, sticky=tkinter.NSEW)
    self.spinbox_from.grid(row=2, column=1, padx=3, pady=3, sticky=tkinter.NSEW)
    label_to.grid(row=2, column=2, padx=3, pady=3, sticky=tkinter.NSEW)
    self.spinbox_to.grid(row=2, column=3, padx=3, pady=3, sticky=tkinter.NSEW)
    button_do.grid(row=3, column=0, padx=3, pady=3, sticky=tkinter.NSEW)
    self.label_do.grid(row=3, column=1, columnspan=3, padx=3, pady=3, sticky=tkinter.NSEW)
    button_quit.grid(row=4, column=3, padx=3, pady=3, sticky=tkinter.E)

    self.columnconfigure(0, weight=0)
    self.columnconfigure(1, weight=2)
    self.columnconfigure(2, weight=1)
    self.columnconfigure(3, weight=2)

  def set_input(self) -> None:
    from tkinter import filedialog as fd
    self.label_input['text'] = fd.askopenfilename(filetypes=[('pdf files', '*.pdf')])
    if self.label_input['text']:
      self.inputpdf = PdfFileReader(open(self.label_input['text'], "rb"))
      num_pages = self.inputpdf.getNumPages()
      self.label_do['text'] = f'total {num_pages} pages'
      self.spinbox_from['to'] = self.spinbox_to['to'] = num_pages
      self.spinbox_from['from_'] = self.spinbox_to['from_'] = 1

  def set_output(self) -> None:
    from tkinter import filedialog as fd    
    self.label_output['text'] = fd.askdirectory()

  def do(self):
    from tkinter.messagebox import showinfo
    from os.path import basename

    pdf_in, dir_out = self.label_input['text'], self.label_output['text']
    if not pdf_in or not dir_out:
      showinfo(title='To images', message='No input or output')
      return None

    outputpdf = PdfFileWriter()
    start, end = int(self.spinbox_from.get()), int(self.spinbox_to.get())
    for page_num in range(start-1, end):      
      outputpdf.addPage(self.inputpdf.getPage(page_num))
      self.label_do['text'] = f'Page {page_num}'
      self.update()

    with open(f"{self.label_output['text']}/{basename(pdf_in)}_{start}-{end}.pdf", "wb") as outputStream:
      self.label_do['text'] = 'Saving to file'
      self.update()
      outputpdf.write(outputStream)

    showinfo(title='Split pdf', message='Done')

  def quit(self, event=None) -> None:
    self.parent.destroy()

if __name__ == '__main__':
  app = tkinter.Tk()
  app.title('Split pdf')
  app.minsize(width=300, height=150)
  app.resizable(True,False)
  app.eval('tk::PlaceWindow . center')
  app.rowconfigure(0, weight=1)
  app.columnconfigure(0, weight=1)
  mw = MainWindow(app)
  app.protocol('WM_DELETE_WINDOW', mw.quit)
  app.mainloop()
