import asyncio, io
import panel as pn
import numpy as np

from scipy import sparse
from scipy.sparse.linalg import spsolve

from js import Bokeh, console, document
from bokeh.plotting import figure

def diff_sparse(v, n=1):
    '''
    caculate n-th discrete difference of sparse matrix
    ---
    v:      sparse matrix, (L, L)
    n:      number of times values are differences, default 1
    ---
    return  n-th differences, (L, L-n)
    '''
    while n > 0:
        v = v.tocsr()[:,1:] - v.tocsr()[:,:-1]
        n -= 1
    return v

class workPanel():
    def __init__(self):
        # file upload
        pn.extension(design='material', notifications=True)
        self.notifications = pn.state.notifications
        #pn.state.notifications.info('start', duration=2000)
        self.file_input = pn.widgets.FileInput(accept='.csv', width=180, multiple=False)
        self.button_upload = pn.widgets.Button(name='Upload', button_type='primary', width=100)
        self.button_clear = pn.widgets.Button(name='Clear', button_type='primary', width=100)
        pn.Row(self.file_input, self.button_upload, self.button_clear, height=75).servable(target='fileinput')
        self.p = figure(width=600, height=400, output_backend='webgl')
        pn.pane.Bokeh(self.p).servable(target='datafig')
        self.button_upload.on_click(self.process_file)
        self.button_clear.on_click(self.clear_file)
        # data smooth
        self.smooth_parameter = pn.widgets.FloatInput(name='smooth factor', value=1e11)
        self.order = pn.widgets.IntInput(name='differential order', value=2, start=2, end=5)
        self.button_smooth = pn.widgets.Button(name='Smooth', button_type='primary', width=100)
        pn.Row(self.smooth_parameter, self.order, self.button_smooth, height=75).servable(target='parameters')
        self.button_smooth.on_click(self.smooth_data)
        self.smoothed = False
        self.data = None

    def process_file(self, event):
        if self.file_input.value is not None:
            document.getElementById('result').innerHTML = ""
            self.data = np.genfromtxt(io.BytesIO(self.file_input.value), delimiter=',', encoding='utf8')
            self.p.line(x=np.arange(len(self.data)),y=self.data, line_color='gray')
            console.log('updated!')
            #self.notifications.info('file has been loaded.', duration=2000)
        else:
            #self.notifications.warning('upload your file first!', duration=2000)
            pass
            

    def clear_file(self, event):
        self.data = None
        self.p.renderers = []
        document.getElementById('result').innerHTML = ""

    def smooth_data(self, event):
        if self.smoothed:
            self.p.renderers = []
            self.p.line(x=np.arange(len(self.data)),y=self.data, line_color='gray')
        if self.data is None:
            #self.notifications.warning('upload your file first!', duration=2000)
            #document.getElementById('result').innerHTML = "Upload your data first!"
            return
        document.getElementById('result').innerHTML = ""
        console.log('smooth start!')
        #self.notifications.info('smoothing start!', duration=3000)
        self.smooth_method()

    def smooth_method(self):
        '''
        penalized least squares (PLS) expect mode
        @ E. T. Whittaker, Proc. Edinburgh Math. Soc., 41(1923), 63-75.
        @ P. H. C. Eilers, Anal. Chem. 75(2003), 3631-3636.
        ---
        l:          parameter for smoothness
        w:          weight array of data
        n:          order for smoothness, default 2
        ---
        return
        z:          smoothed line
        '''
        l, n = self.smooth_parameter.value, self.order.value
        L = len(self.data)
        w = np.ones_like(self.data)        
        D = diff_sparse(sparse.eye(L), n)
        D = l * D.dot(D.transpose())
        W = sparse.spdiags(w, 0, L, L)
        Z = W + D
        z = spsolve(Z, w*self.data)
        console.log('smooth end!')
        self.p.line(x=np.arange(len(z)), y=z, line_color='darkorange')
        np.savetxt("smoother_data.csv", z)
        pn.Row(pn.widgets.FileDownload(file="smoother_data.csv", button_type='success', width=200), height=80).servable(target='result')
        console.log('smooth complete!')
        #self.notifications.success('smoothing complete!', duration=3000)
        self.smoothed = True

worker = workPanel()

