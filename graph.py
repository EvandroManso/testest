import numpy as np
import pandas as pd
# import holoviews as hv
#from holoviews import opts
# hv.extension('bokeh')
from bokeh.plotting import figure, output_file, show
from bokeh.models import LinearAxis, Range1d, DataRange1d, HoverTool
from datetime import timedelta


class graph:
    def __init__(self, df,
                 shadow = [],
                 title = None,  header = None, 
                 axis = None,   style = None, 
                 overlimit = .05,
                 plot_width = 950,
                 leg_pos = "top_left",
                 show = True, #combinar ocm output_file
                 par = False,
                 out_file = "grafico",
                 out_path = "C:\\Users\\pietro.consonni\\OneDrive - TAVOLA\\codes\\generic\\"):
        """ Print a standard graph
        Parameters
        ----------
        df: series utilizadas nos graficos, primeira serie corresponde ao eixo X
        header (list): nome das séries nas legendas (x, y1, y2, y3...) 
        axis (list): associa as series aos possivel eixo (yleft = 1, yright = 2) 
        style (list): criar uns 10 padroes de linha (até mais extremamente genericos) || default coluna i padrao i || pode-se fazer um codigo tipo L1 linha estilo 1, B4 é barra estilo 4
        overlimit: espaço de folga na lateral do grafico
        leg_pos: default bottom_right
        grid_thick: default 0.5 (espaçamento quadradinhos)
        """

        #TODO: inserir verificações [ len(axis) = len(df[:,0]) ]
        #interpolacao para tratar informacoes faltantes no df
        df = df.interpolate(method = 'linear')      

        self.shadow_ind = False
        if shadow != [] and len(shadow) == 2 and df.shape[1] > 2:
            self.shadow_ind = True
            cols = df.columns[shadow]
            self.y_shad = df[cols]
            df = df.drop(columns=cols)

        self.x_var = df.index.values
        self.y_df = df    
        
        if par != False:
            # self.x_var = self.x_var.astype(str)
            df_12h = [el+timedelta(hours=12) for el in pd.Series(self.x_var)] #atrasa 12h os dados

            xaxis = [x for pair in zip(self.x_var, df_12h) for x in pair] #cria um novo eixo x, copiando o anterior, acrescentando 12h as cópias 
            xaxis=np.array(xaxis) #converter em array para não quebrar no x_var.shape
            self.x_var=xaxis
            
            dados1 = list(sum(zip(self.y_df.iloc[:,0], [None]*len(self.y_df.iloc[:,0])), ())) #transforma [1,2,3] em [1,0,2,0,3,0]
            dados2 = list(sum(zip([None]*len(df.iloc[:,0]), self.y_df.iloc[:,1]), ())) #transforma [4,5,6] em [0,4,0,5,0,6]
            dados=pd.DataFrame({"serie1":dados1, "serie2": dados2})
            self.y_df = dados
            

            # p = figure(width=1000, x_axis_type='datetime')
            # p.vbar(x=xaxis, top=dados1, width=86400000/2.05, fill_color="red", line_color="red")
            # p.vbar(x=xaxis, top=dados2, width=86400000/2.05, fill_color="blue", line_color="blue")       
        
        hovertool = HoverTool(
            tooltips = [('date', '$x{%F}'),
                        ('value', '$y')],
            formatters = {'$x': 'datetime'})
        args = {'x_axis_type': 'datetime', 
                'plot_width': plot_width, 
                'plot_height': 400,
                'tools': [hovertool, 'pan', 'wheel_zoom', 'box_zoom','reset', 'crosshair', 'save'],
                'toolbar_location': "below"}
        if title is not None: args['title'] = title
        self.n_data_points = round(plot_width / 5)
        
        if self.x_var.shape[0] > self.n_data_points:
            start = self.x_var[-self.n_data_points]
            end = self.x_var[-1]
            delta = (end - start)*.05
            args['x_range'] = DataRange1d(
                start = start, end = end + delta)  
            
        self.p = figure(**args)
    

        if header is not None and len(header) < df.shape[1]:
            sub_header = {}
            nms = self.y_df.columns.values
            for i, el in enumerate(header):
                sub_header[nms[i]] = header[i]
                
            df.rename(columns = sub_header, inplace = True)

        if axis == None:    self.axis = [1]*(self.y_df.shape[1])
        else:  
            dif = self.y_df.shape[1] - len(axis)
            self.axis = axis + [1]*dif

        if style == None:   self.style = ['']*(self.y_df.shape[1])   
        else:      
            dif = self.y_df.shape[1] - len(style)
            self.style = style + ['']*dif

        if show:
            self.out_file = out_path + out_file + ".html"
            output_file(self.out_file)

        self.overlimit = overlimit
        self.leg_pos = leg_pos
        self.palette = ['goldenrod', 'black', 'gray', 'olive', 'royalblue', 
                        'darkred', 'lightseagreen', 'palevioletred', 'orangered']

    def plot(self):
        p = self.p
        df = self.y_df
        axis = self.axis
        x = self.x_var
        over = self.overlimit
        leg_pos  = self.leg_pos
        color = self.palette
        style = self.style
        
        #nms = header
        nms = df.columns.values
        nms1 = nms[[i for i, x in enumerate(axis) if x==1]]
        nms2 = nms[[i for i, x in enumerate(axis) if x==2]]

        #Defining left axis
        adj_zoom = round(self.n_data_points*2/3)

        up_b1 = np.ceil(df[nms1].iloc[-adj_zoom:,:].max().max())
        low_b1 = np.floor(df[nms1].iloc[-adj_zoom:,:].min().min())

        adj_u1 = adj_l1 = 1
        if up_b1 < 0:  adj_u1 = -1
        if low_b1 < 0: adj_l1 = -1
        p.y_range = Range1d(start = adj_l1*abs(low_b1)*(1-over),
                            end = adj_u1*abs(up_b1)*(1+over))      

        if len(nms2) != 0:
            nms1_new = {}
            for n in nms1:
                nms1_new[n] = n + " (left)"
            df.rename(columns = nms1_new, inplace = True)
           
            up_b2 = np.ceil(df[nms2].iloc[-adj_zoom:,:].max().max())
            low_b2 = np.floor(df[nms2].iloc[-adj_zoom:,:].min().min())

            adj_u2 = adj_l2 = 1
            if up_b2 < 0:  adj_u2 = -1
            if low_b2 < 0: adj_l2 = -1

            y2 = "y_secundario"   
            p.extra_y_ranges = { 
            y2: Range1d(start = adj_l2*abs(low_b2)*(1-over),
                        end = adj_u2*abs(up_b2)*(1+over),) }
            
            p.add_layout(LinearAxis(y_range_name=y2), "right")
        
        p.xgrid.grid_line_color = p.ygrid.grid_line_color = 'grey'
        p.xgrid.grid_line_alpha = p.ygrid.grid_line_alpha = .25       

        header = df.columns.values
        for i, el in enumerate(df):
            args = {'x': x, 'y': df[el], 'legend_label': header[i], 'color': color[i]}
            # O erro abaixo aparece quando os argumentos não tem o tamanhao correto
            #IndexError: list index out of range
            if axis[i] == 2: 
                args['y_range_name'] = y2
        
            if style[i] == 'dd':
                args['line_dash'] = 'dashed'
                args['line_width'] = 2
                args['line_dash_offset'] = 1
                p.line(**args)
            
            elif style[i] == 'bb':
                del args['y']
                args['x'] = list(x)[::10]
                args['top'] = list(df[el])[::1] #TODO: EDITEI AQUI
                # print (list(df[el])[::1])
                args['bottom'] = 0
                args['width'] = 2*10**8 #TODO: EDITEI AQUI
                p.vbar(**args)
                
            elif style[i] == 'lc':
                p.line (**args)
                args['color'] = 'black'
                p.circle(**args)
                
            else:
                args['line_width'] = 1.5
                p.line(**args)
                
        if self.shadow_ind:
            shadow_args = {'x': x, 
                           'y1': self.y_shad.iloc[:,0],
                           'y2': self.y_shad.iloc[:,1],
                           'fill_alpha': .5,
                           'fill_color': 'silver',
                           'legend_label': ''}

            p.varea(**shadow_args)
            
        p.legend.location = leg_pos
        # show(p)
        self.pic=p
        

# if __name__ == '__main__':
#     # Reproducible example:
#     x_column = "x"
#     y_column1 = "y1"
#     y_column2 = "y2"
#     y_column3 = "y3"
#     n = [x_column, y_column1, y_column2, y_column3]
    
#     df = pd.DataFrame()
#     b = list(range(0,30,3)) + list(range(30,80)) + list(range(80,160,2))
#     df[x_column] = range(0, 100)
    
#     df[y_column1] = np.linspace(-100, 100, 100)
#     df[y_column2] = b
#     df[y_column3] = range(400,200,-2)
    
#     df.iloc[2,3] = np.nan
#     a = graph(df = df, header=n, axis= [1,1,2,2], style = ["lc", "dd", "lc","dd"])
#     a.plot()
#     a.show()
# df = pd.read_excel ("R:/EVANDRO/Python/Pietro/" + "dados3.xlsx", sheet_name="Sheet1", header=0)
#df = xlrd.open_workbook("dados3.xlsx", sheet_name="Sheet1")
df = pd.read_excel ("dados3.xlsx", sheet_name="Sheet1", header=0, engine='openpyxl')
# df.iloc[:,0] = df.iloc[:,0].astype(str)
df=df.set_index("datas")

a= graph(df,par=True, style=["bb", "bb"], out_path = "R:/Evandro/Python/")
a.plot()

#dados1 = list(sum(zip(df[:,0], [None]*len(df.iloc[:,0])), ()))
