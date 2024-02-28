import streamlit as st
import pandas as pd
import plotly
import plotly.graph_objects as go
import datetime
import streamlit as st
import datetime
import os
import json
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
import openseespy.opensees as ops
import opsvis as opsv
import matplotlib.pyplot as plt
import altair as alt
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
st.set_page_config(            #Streamlit page configuration 
    page_title="GTU-Analysıs",
    page_icon=":construction_worker:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': (
            "DEVELOPED BY:\n"
            "- Bülent Akbaş\n"
            "- Ahmet Anıl Dindar\n"
            "- Burak Can Kasap\n"
            "- Muhammed Sevinçtekin\n"
            "- Ahmet Doğan\n"
            "- Ahmet Eren Durmuş\n"
            "- Alp Eren Yiğitoğlu\n"
            "- Batuhan Bozkurt\n"
            "- Esmanur Al\n"
            "- Furkan Albayrak\n"
            "- Gamze Aktaş\n"
            "- İrem Tekin"
        )
    }
)
st.write("Hello World")
st.write(datetime.datetime.now())
st.sidebar.image("https://www.gtu.edu.tr/Files/basin_ve_halkla_iliskiler/kurumsal_kimlik/raster_logolar/GTU_LOGO_600X384_JPG_EN.jpg")
st.sidebar.header("Civil Engineering Department")
st.sidebar.markdown("V0.1")
ops.wipe()  #required to open a new model
ops.model('basic', '-ndm', 2, '-ndf', 3)
if "data_node" not in st.session_state:

    st.session_state.data_node =pd.DataFrame([{"Node Number": 0, "Node x": 0.0, "Node y": 0.0}])

if "graph_state_node" not in st.session_state:

    st.session_state.graph_state_node = go.Figure()

if "data_element" not in st.session_state:

    st.session_state.data_element =pd.DataFrame([{"First Node Number": 0, "Second Node Number": 0, "Element Number":0, "Section":None}])
                        
if "data_section" not in st.session_state:
    st.session_state.data_section = pd.DataFrame([{'Section Name': '', 'Width(m)': 0.0, 'Height(m)': 0.0, 'Area(m^2)': 0.0, 'Moment of İnertia(m^4)': 0.0}])      


if "data_support" not in st.session_state:

    st.session_state.data_support =pd.DataFrame({'Node Number': [None], 'X direction': [False], 'Y direction': [False], 'Moment': [False], 'Remove': [False]})

selected_page = st.sidebar.selectbox("Options", ["Main Page", "Open", "New", "Template"])

if "graph_state_support" not in st.session_state:

    st.session_state.graph_state_support = go.Figure()

if "data_load_node" not in st.session_state:

    st.session_state.data_load_node =pd.DataFrame([{'Node Number':1 , 'Px':0 , 'Py':0 , 'Mz':0 }])

if "data_load_element" not in st.session_state:

    st.session_state.data_load_element =pd.DataFrame([{'Element Number': 1 , 'Wx': 0, 'Wy': 0}])

if "data_material" not in st.session_state:

    st.session_state.data_material = [1]


if selected_page == "Main Page":
    st.title(':gray[Welcome to GTU_Analysis] :flag-tr:')
    st.markdown("<p style='font-size: 24px;'>&#x1F477; &mdash;GTU_Analysis is a structure analysis program &mdash; &#x1F477;</p>", unsafe_allow_html=True)
    st.image("https://i.pinimg.com/564x/cc/0c/67/cc0c6741d191dd3f59620033279c71b6.jpg", width=700) 


if selected_page == "Open":
    st.write("OPEN PAGE")



if selected_page == "New":
    st.sidebar.subheader("New")
    
    selected_new_page = st.sidebar.radio("", ["Model", "Analysis", "Results"])
    
    
    if selected_new_page == "Model":
        tab_node, tab_material, tab_section, tab_element,tab_support,tab_load,tab_results = st.tabs(
            ["Node", "Material", 'Section',"Element",'Support Conditions',"Loads","Last Model"]
        )

        with tab_node:
            col_part1, col_part2 = st.columns(2)
            with col_part1:

                
                
                st.header("Node Table")

                
                button_save_data = st.button("Save and Sketch")

                
                if not button_save_data:

                    edited_df = st.data_editor(st.session_state.data_node, num_rows="dynamic")

                
                if button_save_data:
                    
                    df_node = st.data_editor(st.session_state.data_node, num_rows="dynamic")
                    st.session_state.data_node =df_node.copy()
                    st.success("Data saved successfully!")
                    
             
            with col_part2:
                
                if button_save_data:
                
                    i=0   
                    list_node_2=[]
                    Node_x_axis=[]
                    Node_y_axis=[]
                    Node_name= []
                    nodes={}

                    while i<len(st.session_state.data_node.index):
                       
                        list_node_1=list(st.session_state.data_node.iloc[i])
                        list_node_2.append(list_node_1)

                        Node_name = [int(node) if not pd.isna(node) else 0 for node in Node_name]
                        Node_adi = f"Node {i+1}"
                        nodes[Node_adi] = (list_node_2[i][0],list_node_2[i][1],list_node_2[i][2])
                        
                        Node_x_axis.append(list_node_2[i][1])
                        Node_y_axis.append(list_node_2[i][2])
                        Node_name.append(list_node_2[i][0])
                        
                        i+=1

                        if i==len(st.session_state.data_node):

                            # to describe node for plot
                            x= Node_x_axis
                            y= Node_y_axis

                            Node_name = [int(node) if not pd.isna(node) else 0 for node in Node_name]
            
                            scatter = go.Scatter(
                                x=x, y=y, mode='markers+text',
                                text=Node_name, 
                                marker=dict(color='red'),
                                textposition='bottom left',
                                showlegend=False,
                                )

                            
                            #st.session_state.graph_state_node.data = []
                            #print(st.session_state.graph_state_node.data,"bu ne")
                            st.session_state.graph_state_node.add_trace(scatter)
                
                
                st.plotly_chart(st.session_state.graph_state_node)
   
          
        with tab_material:
            E=st.selectbox('Enter Modulus of Elasticity in MPa',
                       ('Concrete','Steel','Other'))
            if E=='Concrete':
                E=30*(10**3)
                st.write('Modulus of elasticity is ',E,'MPa')
                st.session_state.data_material = [E]

            elif E=='Steel':
                E=210*(10**3)
                st.write('Modulus of elasticity is ',E,'MPa')
                st.session_state.data_material = [E]

            elif E=='Other':
                E=st.number_input('Enter modulus of Elasticity in MPa.') 
                st.write('Modulus of elasticity is ',E,'MPa')
                st.session_state.data_material = [E]
        
        with tab_section:


            def calculate_area(length, width):
                return length * width

            def calculate_moment_of_inertia(length, width):
                return (length * width**3) / 12

            st.title("Section Table")           

            df_section = st.data_editor(st.session_state.data_section,
                                column_config={'Area': st.column_config.Column(disabled=True), 'Moment of İnertia':st.column_config.Column(disabled=True) },
                                num_rows="dynamic")

            def _save_button_():
                df_section['Area(m^2)'] = df_section.apply(lambda row: calculate_area(row['Width(m)'], row['Height(m)']), axis=1)
                df_section['Moment of İnertia(m^4)'] = df_section.apply(lambda row: calculate_moment_of_inertia(row['Width(m)'], row['Height(m)']), axis=1)
                st.session_state.data_section = df_section.copy()

            save_button = st.button("Save", on_click=_save_button_)

            if save_button:
                st.success("Data saved successfully!")

        with tab_element:
            col_part1, col_part2 = st.columns(2)
            with col_part1:
                   
                df_element = st.data_editor(st.session_state.data_element
                                            , 
                                            column_config={
                                                "Section": st.column_config.SelectboxColumn(
                                                    "Section",
                                                    help="The category of the app",
                                                    width="medium",
                                                    options=df_section['Section Name'].tolist(),
                                                    required=True)
                                            },
                                            hide_index=True, num_rows="dynamic")
                def _element_finish_(): 
                    st.session_state.data_element = df_element.copy()

                element_finish_button = st.button("finish", on_click= _element_finish_)

                with col_part2:
                    if element_finish_button:
                        a=0
                        list4=[]
                        while a<len(st.session_state.data_element.index):
                            list3=list(st.session_state.data_element.iloc[a])
                            list4.append(list3)
                            a+=1
                
                        
                        if st.session_state.data_element.isna().sum().sum()>0:  #if there is no any NAN values ,the elements can be plotted,if not it cannot be plotted 
                            st.write('You have to fill the table to define the elements.')
                        else:
                            i=0
                            list_node_2=[]
                            Node_x_axis=[]
                            Node_y_axis=[]
                            Node_name= []
                            nodes={}

                            while i<len(st.session_state.data_node.index):
                        
                                list_node_1=list(st.session_state.data_node.iloc[i])
                                list_node_2.append(list_node_1)

                                Node_name = [int(node) if not pd.isna(node) else 0 for node in Node_name]
                                Node_adi = f"Node {i+1}"
                                nodes[Node_adi] = (list_node_2[i][0],list_node_2[i][1],list_node_2[i][2])
                                
                                Node_x_axis.append(list_node_2[i][1])
                                Node_y_axis.append(list_node_2[i][2])
                                Node_name.append(list_node_2[i][0])
                        
                                i+=1

                            for b in list4:
                                x_axis1=[]
                                y_axis1=[] 

                                Node_adi = f"Node {int(b[0])}"
                                x_axis1.append(nodes[Node_adi][1])
                                y_axis1.append(nodes[Node_adi][2])

                                Node_adi = f"Node {int(b[1])}"
                                x_axis1.append(nodes[Node_adi][1])
                                y_axis1.append(nodes[Node_adi][2])

                                

                                x=x_axis1
                                y=y_axis1 
                                #name=f'Element {b[2]}'
                                #element_name =f'Element {int(b[2])}'

                                scatter_line = go.Scatter(
                                    x=x_axis1, y=y_axis1, mode='lines+text',
                                    line=dict(color='black'),
                                    showlegend=False
                                            
                                    )
                                
                                scatter_nodes = go.Scatter(
                                    x=x, y=y, mode='markers+text',
                                    marker=dict(color='red'),
                                    showlegend=False
                                    )
                            
                        
                                st.session_state.graph_state_node.add_trace(scatter_line)
                                #st.session_state.graph_state_element.add_trace(scatter_nodes)
                                
                    st.plotly_chart(st.session_state.graph_state_node)
            
        with tab_support:
                col_part1, col_part2 = st.columns(2)

                with col_part1:
                    st.header('Support Table')
                    df_support = st.data_editor(st.session_state.data_support, column_config={
                    'Node Number': st.column_config.SelectboxColumn(options=st.session_state.data_node['Node Number'].tolist(), required=True),
                    'X direction': st.column_config.CheckboxColumn('X direction',default=False,required="True"),
                    'Y direction': st.column_config.CheckboxColumn('Y direction',default=False,required="True"),
                    'Moment': st.column_config.CheckboxColumn('Moment',default=False,required="True"),
                    'Remove': st.column_config.CheckboxColumn('Remove',default=False,required="True")
                    }, hide_index=True, num_rows="dynamic")
                
                
                def _finish_():
                    st.session_state.data_support = df_support.copy()
                    for index,row in st.session_state.data_support.iterrows():
                        node_number = int(row['Node Number'])
                        x_direction = 1 if int(row['X direction'])== True else 0  # True ise 1, False ise 0
                        y_direction = 1 if int(row['Y direction'])== True else 0  # True ise 1, False ise 0
                        moment = 1 if int(row['Moment'])==True else 0  # True ise 1, False ise 0
                        Remove = 1 if int(row['Remove'])==True else 0  # True ise 1, False ise 0
                        indexx= st.session_state.data_node.to_dict(orient='list')['Node Number'].index(node_number)
                        x_axis_sup = st.session_state.data_node.to_dict(orient='list')['Node x'][indexx]      
                        y_axis_sup = st.session_state.data_node.to_dict(orient='list')['Node y'][indexx]
            
                        if x_direction==1 and y_direction==1 and moment==0 and Remove==0:
                            scatter_triangle = go.Scatter(
                                    x=[x_axis_sup], y=[y_axis_sup], 
                                    mode='markers',
                                    marker=dict(
                                            symbol='triangle-up',
                                            size=10,
                                            color='LightSkyBlue'),
                                    showlegend=False          
                                    )
                            st.session_state.graph_state_node.add_trace(scatter_triangle)                           

                        elif x_direction==1 and y_direction==1 and moment==1 and Remove==0:
                            scatter_square = go.Scatter(
                                    x=[x_axis_sup], y=[y_axis_sup], 
                                    mode='markers',
                                    marker=dict(
                                            symbol='square',
                                            size=10,
                                            color='LightSkyBlue'),
                                    #line=dict(color='black'),
                                    showlegend=False          
                                    )
                            st.session_state.graph_state_node.add_trace(scatter_square)
                            


                        elif x_direction==0 and y_direction==1 and moment==0 and Remove==0:
                            scatter_triangle_y = go.Scatter(
                                    x=[x_axis_sup], y=[y_axis_sup], 
                                    mode='markers',
                                    marker=dict(
                                            symbol='triangle-up',
                                            size=10,
                                            color='MediumPurple',
                                            line=dict(color='LightSkyBlue',width=2)),
                                    showlegend=False          
                                    )
                            st.session_state.graph_state_node.add_trace(scatter_triangle_y)
                                

                        elif x_direction==1 and y_direction==0 and moment==0 and Remove==0:
                            
                            scatter_triangle_x = go.Scatter(
                                    x=[x_axis_sup], y=[y_axis_sup], 
                                    mode='markers',
                                    marker=dict(
                                            symbol='triangle-right',
                                            size=10,
                                            color='MediumPurple',
                                            line=dict(color='LightSkyBlue',width=2)),
                                    showlegend=False          
                                    )
                            st.session_state.graph_state_node.add_trace(scatter_triangle_x)
                            
                            
                        elif Remove==1:
                            scatter_triangle_index = None
                            for i, trace in enumerate(st.session_state.graph_state_node.data):
                                if 'marker' in trace and 'symbol' in trace['marker'] and trace['marker']['symbol'] == 'triangle-up':
                                    scatter_triangle_index = i
                                    break
                                
                            # scatter_triangle'ı kaldırma
                            if scatter_triangle_index is not None:
                                graph_data_list = list(st.session_state.graph_state_node.data)
                                graph_data_list.pop(scatter_triangle_index)
                                
                                st.session_state.graph_state_node.data = graph_data_list
                            
                            scatter_square_index = None
                            for i, trace in enumerate(st.session_state.graph_state_node.data):
                                if 'marker' in trace and 'symbol' in trace['marker'] and trace['marker']['symbol'] == 'square':
                                    scatter_square_index = i
                                    break

                            # scatter_triangle'ı kaldırma
                            if scatter_square_index is not None:
                                graph_data_list = list(st.session_state.graph_state_node.data)
                                graph_data_list.pop(scatter_square_index)
                
                                st.session_state.graph_state_node.data = graph_data_list
                            
                            scatter_triangle_y_index = None
                            for i, trace in enumerate(st.session_state.graph_state_node.data):
                                if 'marker' in trace and 'symbol' in trace['marker'] and trace['marker']['symbol'] == 'triangle-up'and trace['marker']['color']== 'MediumPurple':
                                    scatter_triangle_y_index = i
                                    break

                            # scatter_triangle'ı kaldırma
                            if scatter_triangle_y_index is not None:
                                graph_data_list = list(st.session_state.graph_state_node.data)
                                graph_data_list.pop(scatter_triangle_y_index)
                                
                                st.session_state.graph_state_node.data = graph_data_list

                            scatter_triangle_x_index = None
                            for i, trace in enumerate(st.session_state.graph_state_node.data):
                                if 'marker' in trace and 'symbol' in trace['marker'] and trace['marker']['symbol'] == 'triangle-right':
                                    scatter_triangle_x_index = i
                                    break

                            # scatter_triangle'ı kaldırma
                            if scatter_triangle_x_index is not None:
                                graph_data_list = list(st.session_state.graph_state_node.data)
                                graph_data_list.pop(scatter_triangle_x_index)
                                
                                st.session_state.graph_state_node.data = graph_data_list

                        else:
                            st.write("Please, Check your selection.")
                            
                    
                
                with col_part2:
                    st.plotly_chart(st.session_state.graph_state_node)
                    finish= st.button('Finish', on_click=_finish_)
                    if finish:
                        st.success("OK :)")
                    
        with tab_load:
            col_part1, col_part2,col_part3 = st.columns(3)

            with col_part1:
                df_load_node = st.data_editor(st.session_state.data_load_node,column_config={
                    'Node Number': st.column_config.SelectboxColumn(options=st.session_state.data_node['Node Number'].tolist(), required=True)}, num_rows="dynamic")
                
            
            
            with col_part2:

                df_load_element = st.data_editor(st.session_state.data_load_element,column_config={
                    'Element Number': st.column_config.SelectboxColumn(options=st.session_state.data_element['Element Number'].tolist(), required=True)}, num_rows="dynamic")                      
            

                with col_part3:

                    def _load_():
                        st.session_state.data_load_element = df_load_element.copy()
                        st.session_state.data_load_node = df_load_node.copy()
                    
                    Determine =st.button('Determine',on_click= _load_ )

                    if Determine:
                        
                        def _ops_():
                            ops.wipe()  #required to open a new model
                            ops.model('basic', '-ndm', 2, '-ndf', 3)
                            Ew={}
                            #st.session_state.data_node =df_node.copy()
                            i=0
                            for index, row in st.session_state.data_node.iterrows():
                                node_number = int(row['Node Number'])
                                indexx= st.session_state.data_node.to_dict(orient='list')['Node Number'].index(node_number)
                                x_axis_node = st.session_state.data_node.to_dict(orient='list')['Node x'][indexx]      
                                y_axis_node = st.session_state.data_node.to_dict(orient='list')['Node y'][indexx]
                                ops.node(i+1,x_axis_node,y_axis_node)
                                i+=1
                            
                            ops.geomTransf('Linear', 1)
                            #st.session_state.data_element = df_element.copy()
                            E = st.session_state.data_material
                            for index,row in st.session_state.data_element.iterrows():
                                first_node = int(row['First Node Number'])
                                second_node = int(row['Second Node Number'])
                                element_num = int(row['Element Number'])
                                section_elm = (row['Section'])
                                indexx= st.session_state.data_section.to_dict(orient='list')['Section Name'].index(section_elm)
                                A = st.session_state.data_section.to_dict(orient='list')['Area(m^2)'][indexx]      
                                I = st.session_state.data_section.to_dict(orient='list')['Moment of İnertia(m^4)'][indexx]
                                
                                ops.element('elasticBeamColumn',element_num,first_node,second_node,A,E[0],I,1)
                            
                            #st.session_state.data_support = df_support.copy()
                            for index, row in st.session_state.data_support.iterrows():
                                node_number = int(row['Node Number'])
                                x_direction = int(row['X direction'])
                                y_direction = int(row['Y direction'])
                                moment = int(row['Moment'])
                                ops.fix(node_number,x_direction,y_direction,moment)
                            
                            ops.timeSeries('Constant', 1)
                            ops.pattern('Plain', 1, 1)

                            for index, row in st.session_state.data_load_element.iterrows():
                                Ew[int(row['Element Number'])]=['-beamUniform',float(row['Wy']),float(row['Wx'])]
                                print(Ew)

                            for etag in Ew:
                                ops.eleLoad('-ele', etag, '-type', Ew[etag][0], Ew[etag][1],Ew[etag][2])
                
                            for index, row in st.session_state.data_load_node.iterrows():
                                ops.load(int(row['Node Number']),float(row['Px']),float(row['Py']),float(row['Mz']))
                            
                            ops.constraints('Transformation')
                            ops.numberer('RCM')
                            ops.system('BandGeneral')
                            ops.test('NormDispIncr', 1.0e-6, 6, 2)
                            ops.algorithm('Linear')
                            ops.integrator('LoadControl', 1)
                            ops.analysis('Static')
                            ops.analyze(1)
                            
                        
                        _ops_()
                        opsv.plot_loads_2d()        
                        st.pyplot(plt.gcf())
                        st.success("Ok :)")

        with tab_results:
            st.write('Do you want to see the final model?')
            st.write('You should press the (See Model) button if you want. :)')

            buttons = st.button('See Model')


            if buttons:
                
                st.plotly_chart(st.session_state.graph_state_node)

                col_part1,col_part2,col_part3,col_part4,col_part5=st.columns(5)
            
                with col_part1:
                    st.header('Node Table')
                    df_node = AgGrid(st.session_state.data_node)
                with col_part2:        
                    st.header('Element Table')
                    df_element = AgGrid(st.session_state.data_element)
                with col_part3:
                    st.header('Support Table')
                    df_support = AgGrid(st.session_state.data_support)
                with col_part4:
                    st.header('Node Load Table')
                    df_load_node = AgGrid(st.session_state.data_load_node)
                with col_part5:
                    st.header('Element Load Table')
                    df_load_element = AgGrid(st.session_state.data_load_element)      



              
    if selected_new_page == "Analysis":
            
            

            Analyze = st.button("Analyze")
            
            if Analyze:
                def _ops_():
                    ops.wipe()  #required to open a new model
                    ops.model('basic', '-ndm', 2, '-ndf', 3)
                    Ew={}
                    #st.session_state.data_node =df_node.copy()
                    i=0
                    for index, row in st.session_state.data_node.iterrows():
                        node_number = int(row['Node Number'])
                        indexx= st.session_state.data_node.to_dict(orient='list')['Node Number'].index(node_number)
                        x_axis_node = st.session_state.data_node.to_dict(orient='list')['Node x'][indexx]      
                        y_axis_node = st.session_state.data_node.to_dict(orient='list')['Node y'][indexx]
                        ops.node(i+1,x_axis_node,y_axis_node)
                        i+=1
                    
                    ops.geomTransf('Linear', 1)
                    #st.session_state.data_element = df_element.copy()
                    E = st.session_state.data_material
                    for index,row in st.session_state.data_element.iterrows():
                        first_node = int(row['First Node Number'])
                        second_node = int(row['Second Node Number'])
                        element_num = int(row['Element Number'])
                        section_elm = (row['Section'])
                        indexx= st.session_state.data_section.to_dict(orient='list')['Section Name'].index(section_elm)
                        A = st.session_state.data_section.to_dict(orient='list')['Area(m^2)'][indexx]      
                        I = st.session_state.data_section.to_dict(orient='list')['Moment of İnertia(m^4)'][indexx]
                        
                        ops.element('elasticBeamColumn',element_num,first_node,second_node,A,E[0],I,1)
                    
                    #st.session_state.data_support = df_support.copy()
                    for index, row in st.session_state.data_support.iterrows():
                        node_number = int(row['Node Number'])
                        x_direction = int(row['X direction'])
                        y_direction = int(row['Y direction'])
                        moment = int(row['Moment'])
                        ops.fix(node_number,x_direction,y_direction,moment)
                    
                    ops.timeSeries('Constant', 1)
                    ops.pattern('Plain', 1, 1)

                    for index, row in st.session_state.data_load_element.iterrows():
                        Ew[int(row['Element Number'])]=['-beamUniform',float(row['Wy']),float(row['Wx'])]
                        print(Ew)

                    for etag in Ew:
                        ops.eleLoad('-ele', etag, '-type', Ew[etag][0], Ew[etag][1],Ew[etag][2])
        
                    for index, row in st.session_state.data_load_node.iterrows():
                        ops.load(int(row['Node Number']),float(row['Px']),float(row['Py']),float(row['Mz']))
                    
                    ops.constraints('Transformation')
                    ops.numberer('RCM')
                    ops.system('BandGeneral')
                    ops.test('NormDispIncr', 1.0e-6, 6, 2)
                    ops.algorithm('Linear')
                    ops.integrator('LoadControl', 1)
                    ops.analysis('Static')
                    ops.analyze(1)
                

                _ops_()

                sfacN, sfacV, sfacM = 5.e-3, 5.e-3, 5.e-3  #scale factors
                
                col_part1, col_part2,col_part3 = st.columns(3)

                with col_part1:
                    opsv.section_force_diagram_2d('N', sfacN)
                    plt.title('Axial force distribution')
                    st.pyplot(plt.gcf())
                    
                    with col_part2:
                        opsv.section_force_diagram_2d('T', sfacV)
                        plt.title('Shear force distribution')
                        st.pyplot(plt.gcf())
                        
                        with col_part3:
                            opsv.section_force_diagram_2d('M', sfacM)
                            plt.title('Bending moment distribution')
                            st.pyplot(plt.gcf())    

                exit()
