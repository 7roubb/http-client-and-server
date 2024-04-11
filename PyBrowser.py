import sys , json
from PyQt5.QtCore import QUrl ,QDateTime
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QToolBar, QAction, QLineEdit, QTextEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView,QWebEngineProfile
from PyQt5.QtWebEngineCore import QWebEngineCookieStore



import requests
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.setWindowTitle('PyBrowser')  
        self.setWindowTitle('PyBrowser')
        


        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        rest_client_btn = QAction('REST Client', self)
        rest_client_btn.triggered.connect(self.open_rest_client)
        toolbar.addAction(rest_client_btn)
        
    
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        toolbar.addWidget(self.url_bar)
        
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)
        
        back_btn = QAction('<', self)
        back_btn.triggered.connect(lambda: self.current_browser().back())
        toolbar.addAction(back_btn)
        
        forward_btn = QAction('>', self)
        forward_btn.triggered.connect(lambda: self.current_browser().forward())
        toolbar.addAction(forward_btn)
        
        reload_btn = QAction('⟳', self)
        reload_btn.triggered.connect(lambda: self.current_browser().reload())
        toolbar.addAction(reload_btn)
        
        home_btn = QAction('⌂', self)
        home_btn.triggered.connect(self.navigate_home)
        toolbar.addAction(home_btn)
        
        add_tab_btn = QAction('+', self)
        add_tab_btn.triggered.connect(lambda: self.add_tab(QUrl('https://google.com'), 'New Tab'))
        toolbar.addAction(add_tab_btn)
        
        get_the_cookie = QAction('Get Cookie', self)
        get_the_cookie.triggered.connect(self.get_cookie)
        toolbar.addAction(get_the_cookie)
        
        
        
        
        
        self.add_tab(QUrl('https://google.com'), 'Home')
        
        
        self.profile = QWebEngineProfile.defaultProfile()
        self.profile.setCachePath("./cache") 
        self.profile.setPersistentStoragePath("./storage")
        self.profile.setHttpCacheType(QWebEngineProfile.DiskHttpCache)
      
      

      
    def get_cookie(self):
        url = self.url_bar.text()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        r = requests.get(url)
        if r.status_code == 200:
            cookies = r.cookies.get_dict()
            print (cookies)
       
    
    
    
    def add_tab(self, url=None, label='New Tab'):
        if url is None:
            url = QUrl('https://google.com')
        browser = QWebEngineView()
        browser.setUrl(url)
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
        browser.titleChanged.connect(lambda title, browser=browser: self.tabs.setTabText(self.tabs.indexOf(browser), title))
        browser.urlChanged.connect(lambda url, browser=browser: self.update_url(url) if self.tabs.currentWidget() == browser else None)
    def close_tab(self, index):
        if self.tabs.count() < 2:
            self.close()
        else:
            widget = self.tabs.widget(index)
            widget.deleteLater()
            self.tabs.removeTab(index)
    def navigate_home(self):
        self.current_browser().setUrl(QUrl('https://www.google.com'))
    def navigate_to_url(self):
        url = QUrl(self.url_bar.text())
        if url.scheme() == '':
            url.setScheme('https')
        self.current_browser().setUrl(url)

    def update_url(self, q):
        self.url_bar.setText(q.toString())

    def current_browser(self):
        return self.tabs.currentWidget()

    def open_rest_client(self):
        url = self.url_bar.text()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        response = requests.get(url)
        self.add_response_tab(response)

    def add_response_tab(self, response):
        
        def format_http_headers(headers):
            formatted_headers = ""
            for key, value in headers.items():
                formatted_headers += f"{key}: {value}\r\n"
            return formatted_headers
        
        
        response_text = f"Status Code: {response.status_code}\n\nHeaders:\n{format_http_headers(response.headers)}\n\nBody:\n{response.text}"
        text_edit = QTextEdit()
        text_edit.setText(response_text)
        i = self.tabs.addTab(text_edit, "REST Response")
        self.tabs.setCurrentIndex(i)
        
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApplication.setApplicationName('Project')
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())
