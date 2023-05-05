
# importing libraries
import urllib.request
from PyQt5.QtWidgets import *
import sys
 
class GeeksforGeeks(QWidget):
 
    def __init__(self):
        super().__init__()
 
        # calling a defined method to initialize UI
        self.init_UI()
 
    # method for creating UI widgets
    def init_UI(self):
 
        # creating progress bar
        self.progressBar = QProgressBar(self)
 
        # setting its size
        self.progressBar.setGeometry(25, 45, 210, 30)
 
        # creating push button to start download
        self.button = QPushButton('Start', self)
 
        # assigning position to button
        self.button.move(50, 100)
 
        # assigning activity to push button
        self.button.clicked.connect(self.Download)
 
        # setting window geometry
        self.setGeometry(310, 310, 280, 170)
 
        # setting window action
        self.setWindowTitle("GeeksforGeeks")
 
        # showing all the widgets
        self.show()
 
    # when push button is pressed, this method is called
    def Handle_Progress(self, blocknum, blocksize, totalsize):
 
        ## calculate the progress
        readed_data = blocknum * blocksize
 
        if totalsize > 0:
            download_percentage = readed_data * 100 / totalsize
            self.progressBar.setValue(download_percentage)
            QApplication.processEvents()
 
    # method to download any file using urllib
    def Download(self):
 
        # specify the url of the file which is to be downloaded
        down_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRm9uP3TWzw7bpBylkhVv4J41flU1A1cAlnkg&usqp=CAU' # specify download url here
 
        # specify save location where the file is to be saved
        save_loc = './GeeksforGeeks.png'
 
        # Downloading using urllib
        opener = urllib.request.URLopener()
        opener.addheader('User-Agent', '*')
        filename, headers = opener.retrieve(down_url, save_loc,self.Handle_Progress)
       # urllib.request.urlretrieve(down_url,save_loc, self.Handle_Progress)
 
 
# main method to call our app
if __name__ == '__main__':
 
    # create app
    App = QApplication(sys.argv)
 
    # create the instance of our window
    window = GeeksforGeeks()
 
    # start the app
    sys.exit(App.exec())
