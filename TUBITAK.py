import streamlit as st
import pandas as pd
import datetime
import plotly
import plotly.graph_objects as go
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
import matplotlib.patches as patches
import altair as alt
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import plotly.figure_factory as ff
import plotly.express as px

from math import asin, sqrt


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
            "- Burak Can KasapS\n"
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
st.write(datetime.datetime.now())
st.sidebar.image("https://www.gtu.edu.tr/Files/basin_ve_halkla_iliskiler/kurumsal_kimlik/raster_logolar/GTU_LOGO_600X384_JPG_EN.jpg")
st.sidebar.header("Civil Engineering Department")
st.sidebar.markdown("V0.1")
ops.wipe()  #required to open a new model
ops.model('basic', '-ndm', 2, '-ndf', 3)

if "data_node" not in st.session_state:

    st.session_state.data_node =pd.DataFrame([{"Node Number": 0, "Node x": 0.0, "Node y": 0.0}])

if "data_node_3d" not in st.session_state:
   
    st.session_state.data_node_3d =pd.DataFrame([{"Node Number": 0, "Node x": 0.0, "Node y": 0.0, "Node z": 0.0}])

if "graph_state_node" not in st.session_state:

    st.session_state.graph_state_node = go.Figure()

if "graph_state_node_3d" not in st.session_state:

    st.session_state.graph_state_node_3d = go.Figure()

if "data_element" not in st.session_state:

    st.session_state.data_element =pd.DataFrame([{"First Node Number": 0, "Second Node Number": 0, "Element Number":0, "Section":None , 'Story Level':None,"Element Length (m)": 0 , "Weight (kN)": 0 }])

if "df_element" not in st.session_state:

    st.session_state.df_element =pd.DataFrame([{"First Node Number": 0, "Second Node Number": 0, "Element Number":0, "Section":None ,'Story Level':None, "Element Length (m)": 0 , "Weight (kN)": 0 }])

if "df_element_length" not in st.session_state:
    
    st.session_state.df_element_length=pd.DataFrame([{"First Node Number": 0, "Second Node Number": 0, "Element Number":0, "Section":None , 'Story Level':None,"Element Length (m)": 0 , "Weight (kN)": 0,"Node Number": 0, "Node x": 0.0, "Node y": 0.0, 'First_x_node':0,'Second_x_node':0,'First_y_node':0,'Second_y_node':0 }])
if "data_section" not in st.session_state:
    
    st.session_state.data_section = pd.DataFrame([{'Section Name': '', 'Material': '' , 'Section Type':'' , 'Width(m)': 0.0, 'Height(m)': 0.0, 'Modulus of Elastisity (MPa)' : 0.0 , 'Spesific Weight (kN/m^3)' : 0.0  ,'Area(m^2)': 0.0, 'I(2-2)(m^4)': 0.0, 'I(3-3)(m^4)': 0.0,'J(m^4)': 0.0 ,'G(MPa)':0.0, 'Self Weight (kN/m)': 0.0 }])      

if "data_support" not in st.session_state:

    st.session_state.data_support =pd.DataFrame({'Support Node Number': [None], 'X direction': [False], 'Y direction': [False], 'Moment': [False], 'Remove': [False]})

if "data_support_3d" not in st.session_state:
   
    st.session_state.data_support_3d =pd.DataFrame({'Support Node Number': [None], 'X translation': [False], 'Y translation': [False], 'Z translation': [False], 'Rotation about x': [False], 'Rotation about y': [False], 'Rotation about z': [False] ,'Remove': [False]})
                
if "graph_state_support" not in st.session_state:

    st.session_state.graph_state_support = go.Figure()

if "data_load_node" not in st.session_state:

    st.session_state.data_load_node =pd.DataFrame([{'Load Node Number':1 , 'Px':0 , 'Py':0 , 'Mz':0,'Load Type(Point)':'Live' }])
if "data_load_node_3d" not in st.session_state:

    st.session_state.data_load_node_3d =pd.DataFrame([{'Node Number':1 , 'Px':0 , 'Py':0 ,'Pz':0 , 'Mx':0,'My':0,'Mz':0,'Load Type':'Live' }])

if "data_load_element" not in st.session_state:

    st.session_state.data_load_element =pd.DataFrame([{'Load Element Number': 1 , 'Wx': 0, 'Wy': 0,'Load Type(Distributed)':'Live'}])
if "data_load_element_3d" not in st.session_state:

    st.session_state.data_load_element_3d =pd.DataFrame([{'Element Number': 1 , 'Wx': 0, 'Wy': 0,'Wz': 0,'Load Type':'Live'}])


if "data_material" not in st.session_state:

    st.session_state.data_material = [1]

if "data_load_combination" not in st.session_state:
    
    st.session_state.data_load_combination= pd.DataFrame([{'Combination':'','Dead':0.0,'Live':0.0,'Wind':0.0 ,'Snow':0.0 , 'Earthquake':0.0}])

if "data_period" not in st.session_state:

    st.session_state.data_period =pd.DataFrame([{'Mode Number': 1 ,'Period':0}])





                                                        

selected_page = st.sidebar.selectbox("Options", ["Main Page", "Open", "New", "Template"])
if selected_page == "Main Page":
    st.title(':gray[Welcome to GTU_Analysis] :flag-tr:')
    st.markdown("<p style='font-size: 24px;'>&#x1F477; &mdash;GTU_Analysis is a structure analysis program &mdash; &#x1F477;</p>", unsafe_allow_html=True)
    st.image("https://i.pinimg.com/564x/cc/0c/67/cc0c6741d191dd3f59620033279c71b6.jpg", width=700) 


if selected_page == "Open":
    st.write("OPEN PAGE")

    fileUploaded_json = st.file_uploader("Select your input file", type="json")
    

    if fileUploaded_json is not None:
        
        string =fileUploaded_json.getvalue().decode("utf-8")
        a= json.loads(string)
        df_dict = json.loads(a)

        df_dict_node= {key: value for key, value in df_dict.items() if key in ["Node Number","Node x" , "Node y" ]}
        df_dict_node_3d = {key: value for key, value in df_dict.items() if key in ["Node Number(3d)" , "Node x(3d)", "Node y(3d)", "Node z(3d)"]}
        df_dict_section= {key: value for key, value in df_dict.items() if key in ['Section Name', 'Material', 'Section Type', 'Width(m)', 'Height(m)', 'Modulus of Elastisity (MPa)', 'Spesific Weight (kN/m^3)','Area(m^2)', 'I(2-2)(m^4)', 'I(3-3)(m^4)', 'Self Weight (kN/m)']}
        df_dict_data_element= {key: value for key, value in df_dict.items() if key in ["First Node Number", "Second Node Number", "Element Number", "Section", 'Story Level',"Element Length (m)", "Weight (kN)"]}
        #df_dict_df_element = {key: value for key, value in df_dict.items() if key in ["First Node Number", "Second Node Number", "Element Number", "Section", 'Story Level', "Element Length (m)", "Weight (kN)"]}
        df_dict_df_element_length ={key: value for key, value in df_dict.items() if key in ['First_x_node','Second_x_node','First_y_node','Second_y_node']}
        df_dict_support_3d= {key: value for key, value in df_dict.items() if key in['Support Node Number(3d)', 'X translation(3d)', 'Y translation(3d)', 'Z translation(3d)', 'Rotation about x(3d)', 'Rotation about y(3d)', 'Rotation about z(3d)','Remove(3d)']}
        df_dict_support = {key: value for key, value in df_dict.items() if key in ['Support Node Number', 'X direction', 'Y direction', 'Moment', 'Remove']}
        df_dict_load_node = {key: value for key, value in df_dict.items() if key in ['Load Node Number','Px', 'Py', 'Mz', 'Load Type(Point)']}
        df_dict_load_element = {key: value for key, value in df_dict.items() if key in ['Load Element Number','Wx', 'Wy','Load Type(Distributed)']}
        df_dict_load_combination ={key: value for key, value in df_dict.items() if key in ['Combination','Dead','Live','Wind','Snow', 'Earthquake']}
        df_dict_data_period= {key: value for key, value in df_dict.items() if key in ['Mode Number','Period']}
        df_dict_df_element_length.update(df_dict_data_element)
        #df_dict_df_element_length.update(df_dict_node)
        print(df_dict_df_element_length,"1")
        datFrame_element_length=pd.DataFrame(df_dict_df_element_length)
        df_datFrame_element_length= datFrame_element_length.dropna()
        print(datFrame_element_length, "bakmak lazım")
        datFrame_element=pd.DataFrame(df_dict_data_element)
        df_datFrame_element = datFrame_element.dropna()
        print( df_datFrame_element,"ss")

        if "data_node_open" not in st.session_state:

            st.session_state.data_node_open =pd.DataFrame.from_dict(df_dict_node)
       
        if "data_node_3d_open" not in st.session_state:
            st.session_state.data_node_3d_open =pd.DataFrame.from_dict(df_dict_node_3d)

        if "graph_state_node_open" not in st.session_state:

            st.session_state.graph_state_node_open = go.Figure()
       
        if "graph_state_node_3d_open" not in st.session_state:

            st.session_state.graph_state_node_3d_open = go.Figure()

        if "data_element_open" not in st.session_state:

            st.session_state.data_element_open = df_datFrame_element
       
        if "df_element_open" not in st.session_state:

            st.session_state.df_element_open = df_datFrame_element
      
        if "df_element_length_open" not in st.session_state:
            
            st.session_state.df_element_length_open= pd.DataFrame.from_dict(df_dict_df_element_length)
                                
        if "data_section_open" not in st.session_state:
            st.session_state.data_section_open = pd.DataFrame.from_dict(df_dict_section)

        if "data_support_open" not in st.session_state:

            st.session_state.data_support_open =pd.DataFrame.from_dict(df_dict_support)
        
        if "data_support_3d_open" not in st.session_state:
            st.session_state.data_support_3d_open =pd.DataFrame.from_dict(df_dict_support_3d)

                            
        if "graph_state_support_open" not in st.session_state:

            st.session_state.graph_state_support_open =  go.Figure()

        if "data_load_node_open" not in st.session_state:

            st.session_state.data_load_node_open =pd.DataFrame.from_dict(df_dict_load_node)

        if "data_load_element_open" not in st.session_state:

            st.session_state.data_load_element_open =pd.DataFrame.from_dict(df_dict_load_element)

        if "data_material_open" not in st.session_state:

            st.session_state.data_material_open = [1]

        if "data_load_combination_open" not in st.session_state:
            
            st.session_state.data_load_combination_open= pd.DataFrame.from_dict(df_dict_load_combination)
        if "data_period_open" not in st.session_state:

            st.session_state.data_period_open =pd.DataFrame.from_dict(df_dict_data_period)

        tab_model,tab_results=st.tabs(["Model", "Results"])
        def _json_download_():
            df_dict={}
            df_dict_node= st.session_state.data_node_open.to_dict(orient='list')
            df_dict_node_3d= st.session_state.data_node_3d_open.to_dict(orient='list')
            df_dict_section=st.session_state.data_section_open.to_dict(orient='list')
            df_dict_data_element=st.session_state.data_element_open.to_dict(orient='list')
            df_dict_df_element=st.session_state.df_element_open.to_dict(orient='list')
            df_dict_df_element_length=st.session_state.df_element_length_open.to_dict(orient='list')
            df_dict_support = st.session_state.data_support_open.to_dict(orient='list')
            df_dict_support_3d = st.session_state.data_support_3d_open.to_dict(orient='list')
            df_dict_load_node =  st.session_state.data_load_node_open.to_dict(orient='list')
            df_dict_load_element = st.session_state.data_load_element_open.to_dict(orient='list')
            df_dict_load_combination = st.session_state.data_load_combination_open.to_dict(orient='list')
            df_dict_data_period =st.session_state.data_period_open.to_dict(orient='list')
            df_dict.update(df_dict_node)
            df_dict.update(df_dict_node_3d)
            df_dict.update(df_dict_section)
            df_dict.update(df_dict_data_element)
            df_dict.update(df_dict_df_element)
            df_dict.update(df_dict_df_element_length)
            df_dict.update(df_dict_support)
            df_dict.update(df_dict_support_3d)
            df_dict.update(df_dict_load_node)
            df_dict.update(df_dict_load_element)
            df_dict.update(df_dict_load_combination)
            df_dict.update(df_dict_data_period)
            print(df_dict,"bbbbb")
            
            Json_data = json.dumps(df_dict)
            with open('Data.json', 'w') as file:
                json.dump(Json_data, file)
            st.success("File downloaded.")

        Download_json = st.sidebar.button("Download as A json File", on_click=_json_download_)
       
        with tab_model:
        
            tab_node, tab_section, tab_element,tab_support,tab_load,tab_loadcomb,tab_lastmodel = st.tabs(
                ["Node", 'Section',"Element",'Support Conditions',"Loads",'Load Combinations',"Last Model"]  )
            
            with tab_node:
                col_part1, col_part2 = st.columns(2)
                with col_part1:
                    option=st.selectbox(
                        'Select your dimension.',('2D','3D')

                    )

                    st.header("Node Table")

                    
                    button_save_data = st.button("Save and Sketch")

                    if option=='2D':

                        if not button_save_data:
                            edited_df = st.data_editor(st.session_state.data_node_open, hide_index=True, num_rows="dynamic")
                    
                        if button_save_data:
                        
                            df_node = st.data_editor(st.session_state.data_node_open,hide_index=True, num_rows="dynamic")
                            st.session_state.data_node_open =df_node.copy()
                            st.success("Data saved successfully!")

                    else:
                        if not button_save_data:
                            edited_df = st.data_editor(st.session_state.data_node_3d_open,hide_index=True, num_rows="dynamic")
                    
                        if button_save_data:
                        
                            df_node = st.data_editor(st.session_state.data_node_3d_open,hide_index=True, num_rows="dynamic")
                            st.session_state.data_node_3d_open =df_node.copy()
                            st.success("Data saved successfully!")

                with col_part2:
                    if option=='2D': 
                        if button_save_data:
                        
                            i=0   
                            list_node_2=[]
                            Node_x_axis=[]
                            Node_y_axis=[]
                            Node_name= []
                            nodes={}

                            while i<len(st.session_state.data_node_open.index):
                            
                                list_node_1=list(st.session_state.data_node_open.iloc[i])
                                list_node_2.append(list_node_1)

                                Node_name = [int(node) if not pd.isna(node) else 0 for node in Node_name]
                                Node_adi = f"Node {i+1}"
                                nodes[Node_adi] = (list_node_2[i][0],list_node_2[i][1],list_node_2[i][2])
                                
                                Node_x_axis.append(list_node_2[i][1])
                                Node_y_axis.append(list_node_2[i][2])
                                Node_name.append(list_node_2[i][0])
                                
                                i+=1

                                if i==len(st.session_state.data_node_open):
                                    if any(isinstance(trace, go.Scatter) for trace in st.session_state.graph_state_node_open.data):
                                    # Scatter grafiğini sil
                                        st.session_state.graph_state_node_open.data = [trace for trace in st.session_state.graph_state_node_open.data if not isinstance(trace, go.Scatter)]

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
                                    st.session_state.graph_state_node_open.add_trace(scatter)
                        
                        
                        st.plotly_chart(st.session_state.graph_state_node_open)
                    else:
                        if button_save_data:
                        
                            i=0   
                            list_node_2=[]
                            Node_x_axis=[]
                            Node_y_axis=[]
                            Node_z_axis=[]
                            Node_name= []
                            nodes={}

                            while i<len(st.session_state.data_node_3d_open.index):
                            
                                list_node_1=list(st.session_state.data_node_3d_open.iloc[i])
                                list_node_2.append(list_node_1)

                                Node_name = [int(node) if not pd.isna(node) else 0 for node in Node_name]
                                Node_adi = f"Node {i+1}"
                                nodes[Node_adi] = (list_node_2[i][0],list_node_2[i][1],list_node_2[i][2],list_node_2[i][3])
                                
                                Node_x_axis.append(list_node_2[i][1])
                                Node_y_axis.append(list_node_2[i][2])
                                Node_z_axis.append(list_node_2[i][3])
                                Node_name.append(list_node_2[i][0])
                                
                                i+=1

                                if i==len(st.session_state.data_node_3d_open):
                                    if any(isinstance(trace, go.Scatter) for trace in st.session_state.graph_state_node_3d_open.data):
                                    # Scatter grafiğini sil
                                        st.session_state.graph_state_node_3d_open.data = [trace for trace in st.session_state.graph_state_node_3d_open.data if not isinstance(trace, go.Scatter)]

                                    # to describe node for plot
                                    x= Node_x_axis
                                    y= Node_y_axis
                                    z=Node_z_axis

                                    Node_name = [int(node) if not pd.isna(node) else 0 for node in Node_name]
                    
                                    scatter = go.Scatter3d(
                                        x=x, y=y, z=z, mode='markers+text',
                                        text=Node_name, 
                                        marker=dict(color='red'),
                                        textposition='bottom left',
                                        showlegend=False,
                                        )

                                    
                                    #st.session_state.graph_state_node.data = []
                                    #print(st.session_state.graph_state_node.data,"bu ne")
                                    st.session_state.graph_state_node_3d_open.add_trace(scatter)
                        
                        
                        st.plotly_chart(st.session_state.graph_state_node_3d_open)
            
            with tab_section:
                col_part1, col_part2 = st.columns(spec=[0.78,0.22])

                with col_part1:
                    

                    st.write("You must input ;\n"
                "- Section Name\n"
                "- Material\n"
                "- Section Type\n"
                "- Width (m)\n"
                "- Length (m)\n"
                "- Modulus of Elasticity(MPa)\n\n"
                "Don't worry, the other values will be calculated automatically \n"
                ":)) " )

                    def calculate_area(length, width):
                        return length * width

                    def calculate_moment_of_inertia22(b,h):
                        return (h*(b**3)) / 12
                    
                    def calculate_moment_of_inertia33(b,h):
                        return (b * (h**3)) / 12
                    
                    def moe(modulus_of_elastisity):
                        return modulus_of_elastisity*1
                    
                    
                    st.title("Section Table")           

                    df_section = st.data_editor(st.session_state.data_section_open,
                                        column_config={'Material': st.column_config.SelectboxColumn(options= ['Concrete']),
                                                    'Area': st.column_config.Column(disabled=True),
                                                    'Moment of İnertia':st.column_config.Column(disabled=True),
                                                    'Section Type': st.column_config.SelectboxColumn(options= ['Column','Beam']),
                                                    'Self Weight (kN/m)':st.column_config.Column(disabled=True) },
                                        num_rows="dynamic")


                    def sw(material):
                        if material == 'Concrete':
                            return 25
                        else:
                            return 0 
                        

                    def calculate_self_weight (specific_weight, area, section_type):
                        if section_type == 'Column':
                            return specific_weight * area
                        elif section_type == 'Beam':
                            return specific_weight*area
                        
                            
                

                

                def _save_button_():
                    df_section['Area(m^2)'] = df_section.apply(lambda row: calculate_area(row['Width(m)'], row['Height(m)']), axis=1)
                    df_section['I(2-2)(m^4)'] = df_section.apply(lambda row: calculate_moment_of_inertia22(row['Width(m)'], row['Height(m)']), axis=1)
                    df_section['I(3-3)(m^4)'] = df_section.apply(lambda row: calculate_moment_of_inertia33(row['Width(m)'], row['Height(m)']), axis=1)
                    df_section['Modulus of Elastisity (MPa)'] = df_section.apply(lambda row: moe(row['Modulus of Elastisity (MPa)']), axis=1)
                    df_section['Spesific Weight (kN/m^3)'] = df_section.apply(lambda row: sw(row['Material']), axis=1)
                    df_section['Self Weight (kN/m)'] = df_section.apply(lambda row: calculate_self_weight( row['Spesific Weight (kN/m^3)'], row['Area(m^2)'], row['Section Type']), axis=1)

                    st.session_state.data_section_open = df_section.copy()

            

                save_button = st.button("Save", on_click=_save_button_)

                if save_button:
                    st.success("Data saved successfully!")
                with col_part2:
                    # Define the width (b) and height (h) of the rectangle
                    b = 10  # Width
                    h = 5   # Height

                    # Create a figure and a set of subplots
                    fig, ax = plt.subplots()

                    # Draw the rectangle
                    rectangle = plt.Rectangle((0, 0), b, h, fill=None, edgecolor='blue')
                    ax.add_patch(rectangle)

                    # Set the x and y axis limits
                    plt.xlim(-1, b + 1)
                    plt.ylim(-1, h + 1)

                    # Remove axis numbers and ticks
                    ax.set_xticks([])
                    ax.set_yticks([])
                    ax.set_xticklabels([])
                    ax.set_yticklabels([])

                    # Label the width and height outside the rectangle
                    plt.text(b / 2, -0.5, 'Width (b)', ha='center', va='center')
                    plt.text(-0.5, h / 2, 'Height (h)', ha='center', va='center', rotation='vertical')

                    # Add coordinate system at the center of the rectangle
                    center_x = b / 2
                    center_y = h / 2

                    # Draw x and y axis lines at the center of the rectangle
                    ax.arrow(center_x, center_y, b/2 - 0.5, 0, head_width=0.2, head_length=0.5, fc='black', ec='black')
                    ax.arrow(center_x, center_y, 0, h/2 - 0.5, head_width=0.2, head_length=0.5, fc='black', ec='black')


                    # Label the axes at the center
                    plt.text(center_x + b/2 - 0.5, center_y - 0.5, '3-3', ha='center', va='center')
                    plt.text(center_x - 0.5, center_y + h/2 - 0.5, '2-2', ha='center', va='center')

                    # Set labels for the axes (if needed, adjust as per your requirement)
                    plt.xlabel('')
                    plt.ylabel('')

                    # Display the plot
                    plt.gca().set_aspect('equal', adjustable='box')
                    plt.grid(False)  # Turn off the grid

                    st.pyplot(fig)
        
            with tab_element:
                col_part1, col_part2 = st.columns(2)
                with col_part1:
                    listofstories=list(range(0,51))
                    st.write('Please construct the elements from left to right and from top to bottom.')
                    st.session_state.df_element_open = st.data_editor(st.session_state.data_element_open
                                                , 
                                                column_config={
                                                    "Section": st.column_config.SelectboxColumn(
                                                        "Section",
                                                        help="The category of the app",
                                                        width="medium",
                                                        options=df_section['Section Name'].tolist(),
                                                        required=True) ,
                                                        'Story Level':st.column_config.SelectboxColumn(
                                                        "Story Level",
                                                        help="The category of the app",
                                                        width="medium",
                                                        options=listofstories,
                                                        required=True),
                                                        "Element Length (m)":st.column_config.Column(disabled=True),
                                                        "Weight (kN)":st.column_config.Column(disabled=True)
                                                },
                                                hide_index=True, num_rows="dynamic")
                    if option=='2D':
                        st.session_state.df_element_length_open = pd.concat([st.session_state.df_element_open, st.session_state.data_node_open], ignore_index=True)
                        
                        st.session_state.df_element_length_open['First_x_node'] = st.session_state.df_element_open['First Node Number'].map(st.session_state.data_node_open.set_index('Node Number')['Node x']) #adding x and y coordinate information of df_All dataframe
                        st.session_state.df_element_length_open['Second_x_node'] = st.session_state.df_element_open['Second Node Number'].map(st.session_state.data_node_open.set_index('Node Number')['Node x'])
                        st.session_state.df_element_length_open['First_y_node'] = st.session_state.df_element_open['First Node Number'].map(st.session_state.data_node_open.set_index('Node Number')['Node y'])
                        st.session_state.df_element_length_open['Second_y_node'] = st.session_state.df_element_open['Second Node Number'].map(st.session_state.data_node_open.set_index('Node Number')['Node y'])
                        st.session_state.df_element_length_open.drop(columns=['Node Number','Node x','Node y'],inplace=True)
                        
                        def element_length(x0,x1,y0,y1):
                                
                            return ((x0-x1)**2 + (y0-y1)**2)**0.5
                        
                        def weight(rho , length):
                            return rho*length
                        

                        def _element_finish_():
                            
                            st.session_state.df_element_open["Element Length (m)"] =st.session_state.df_element_length_open.apply(lambda row: element_length(row['First_x_node'], row['Second_x_node'], row['First_y_node'] , row['Second_y_node'] ), axis=1)
                            
                            
                            i=0
                            
                            df_weight = pd.DataFrame([{'Length':0.0, 'Self Weight' :0.0}])
                            
                            
                            while i < len(st.session_state.df_element_open["Element Number"]):
                                section_name = st.session_state.df_element_open["Section"][i]
                                
                                a=0

                                while a < len(st.session_state.data_section_open["Section Name"]):
                                    if st.session_state.data_section_open["Section Name"][a] == section_name:
                                        self_weight = st.session_state.data_section_open["Self Weight (kN/m)"][a]
                                        df_weight.loc[i] = {'Length': 0.0, 'Self Weight': self_weight}
                                        
                                    a += 1
                                
                                i += 1
                            
                            df_weight['Length'] =st.session_state.df_element_open["Element Length (m)"]           
                            st.session_state.df_element_open["Weight (kN)"] = df_weight.apply(lambda row: weight(row['Length'], row['Self Weight'] ), axis=1)
                            st.session_state.data_element_open = st.session_state.df_element_open.copy()
                            

                        element_finish_button = st.button("finish", on_click= _element_finish_)
                        
                        
                        
                        
                        # finding story and floor numbers to find period
                        beamlength=[]
                        columnlength=[]
                       
                    
                        for index, row in st.session_state.df_element_length_open.iterrows():
                            if row['First_y_node']==row['Second_y_node']:
                                beamlength.append(row['Element Length (m)'])
                            if row['First_x_node']==row['Second_x_node']:
                                columnlength.append(row['Element Length (m)'])

                        print(columnlength,'col length')
                        storynumber= len(st.session_state.df_element_length_open[st.session_state.df_element_length_open['First_x_node'] == st.session_state.df_element_length_open['Second_x_node']].groupby('First_y_node').size())
                        baynumber= len(st.session_state.df_element_length_open[st.session_state.df_element_length_open['First_y_node'] ==st.session_state. df_element_length_open['Second_y_node']].groupby('First_x_node').size())
                     
                        
                        
                        with col_part2:
                            if element_finish_button:
                                a=0
                                list4=[]
                                while a<len(st.session_state.data_element_open.index):
                                    list3=list(st.session_state.data_element_open.iloc[a])
                                    list4.append(list3)
                                    a+=1
                        
                                
                                if st.session_state.data_element_open.isna().sum().sum()>0:  #if there is no any NAN values ,the elements can be plotted,if not it cannot be plotted 
                                    st.write('You have to fill the table to define the elements.')
                                else:
                                    i=0
                                    list_node_2=[]
                                    Node_x_axis=[]
                                    Node_y_axis=[]
                                    Node_name= []
                                    nodes={}

                                    while i<len(st.session_state.data_node_open.index):
                                
                                        list_node_1=list(st.session_state.data_node_open.iloc[i])
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
                                    
                                
                                        st.session_state.graph_state_node_open.add_trace(scatter_line)
                                        #st.session_state.graph_state_element.add_trace(scatter_nodes)
                                        
                            st.plotly_chart(st.session_state.graph_state_node_open)


                    else:
                        st.session_state.df_element_length_open = pd.concat([st.session_state.df_element_open, st.session_state.data_node_3d_open], ignore_index=True)
                        
                        st.session_state.df_element_length_open['First_x_node'] = st.session_state.df_element_open['First Node Number'].map(st.session_state.data_node_3d_open.set_index('Node Number')['Node x']) #adding x,z and y coordinate information of df_All dataframe
                        st.session_state.df_element_length_open['Second_x_node'] = st.session_state.df_element_open['Second Node Number'].map(st.session_state.data_node_3d_open.set_index('Node Number')['Node x'])
                        st.session_state.df_element_length_open['First_y_node'] = st.session_state.df_element_open['First Node Number'].map(st.session_state.data_node_3d_open.set_index('Node Number')['Node y'])
                        st.session_state.df_element_length_open['Second_y_node'] = st.session_state.df_element_open['Second Node Number'].map(st.session_state.data_node_3d_open.set_index('Node Number')['Node y'])
                        st.session_state.df_element_length_open['First_z_node'] = st.session_state.df_element_open['First Node Number'].map(st.session_state.data_node_3d_open.set_index('Node Number')['Node z'])
                        st.session_state.df_element_length_open['Second_z_node'] = st.session_state.df_element_open['Second Node Number'].map(st.session_state.data_node_3d_open.set_index('Node Number')['Node z'])
                        
                        def element_length(x0,x1,y0,y1,z0,z1):
                                
                            return ((x0-x1)**2 + (y0-y1)**2+(z0-z1)**2)**0.5
                        
                        def weight(rho , length):
                            return rho*length
                        

                        def _element_finish_():
                            
                            st.session_state.df_element_open["Element Length (m)"] =st.session_state.df_element_length_open.apply(lambda row: element_length(row['First_x_node'], row['Second_x_node'], row['First_y_node'] , row['Second_y_node'],row['First_z_node'], row['Second_z_node'] ), axis=1)
                            
                            
                            i=0
                            
                            df_weight = pd.DataFrame([{'Length':0.0, 'Self Weight' :0.0}])
                            
                            
                            while i < len(st.session_state.df_element_open["Element Number"]):
                                section_name = st.session_state.df_element_open["Section"][i]
                                
                                a=0

                                while a < len(st.session_state.data_section_open["Section Name"]):
                                    if st.session_state.data_section_open["Section Name"][a] == section_name:
                                        self_weight = st.session_state.data_section_open["Self Weight (kN/m)"][a]
                                        df_weight.loc[i] = {'Length': 0.0, 'Self Weight': self_weight}
                                        
                                    a += 1
                                
                                i += 1
                            
                            df_weight['Length'] =st.session_state.df_element_open["Element Length (m)"]           
                            st.session_state.df_element_open["Weight (kN)"] = df_weight.apply(lambda row: weight(row['Length'], row['Self Weight'] ), axis=1)
                            st.session_state.data_element_open = st.session_state.df_element_open.copy()
                            

                        element_finish_button = st.button("finish", on_click= _element_finish_)
                        
                        
                        
                        
                        # finding story and floor numbers to find period
                        beamlength=[]
                        columnlength=[]
                    
                        for index, row in st.session_state.df_element_length_open.iterrows():
                            if row['First_y_node']==row['Second_y_node']:
                                beamlength.append(row['Element Length (m)'])
                            if row['First_x_node']==row['Second_x_node']:
                                columnlength.append(row['Element Length (m)'])
                        storynumber= len(st.session_state.df_element_length_open[st.session_state.df_element_length_open['First_x_node'] == st.session_state.df_element_length_open['Second_x_node']].groupby('First_y_node').size())
                        baynumber= len(st.session_state.df_element_length_open[st.session_state.df_element_length_open['First_y_node'] ==st.session_state. df_element_length_open['Second_y_node']].groupby('First_x_node').size())
                        print(baynumber,"açıklık")
                        print(storynumber,"kat")

                        
                        with col_part2:
                            
                            if element_finish_button:
                                a=0
                                list4=[]
                                while a<len(st.session_state.data_element_open.index):
                                    list3=list(st.session_state.data_element_open.iloc[a])
                                    list4.append(list3)
                                    a+=1
                        
                                
                                if st.session_state.data_element_open.isna().sum().sum()>0:  #if there is no any NAN values ,the elements can be plotted,if not it cannot be plotted 
                                    st.write('You have to fill the table to define the elements.')
                                else:
                                    i=0
                                    list_node_2=[]
                                    Node_x_axis=[]
                                    Node_y_axis=[]
                                    Node_z_axis=[]
                                    Node_name= []
                                    nodes={}

                                    while i<len(st.session_state.data_node_3d_open.index):
                                
                                        list_node_1=list(st.session_state.data_node_3d_open.iloc[i])
                                        list_node_2.append(list_node_1)

                                        Node_name = [int(node) if not pd.isna(node) else 0 for node in Node_name]
                                        Node_adi = f"Node {i+1}"
                                        nodes[Node_adi] = (list_node_2[i][0],list_node_2[i][1],list_node_2[i][2],list_node_2[i][3])
                                        
                                        Node_x_axis.append(list_node_2[i][1])
                                        Node_y_axis.append(list_node_2[i][2])
                                        Node_z_axis.append(list_node_2[i][3])
                                        Node_name.append(list_node_2[i][0])
                                
                                        i+=1

                                    for b in list4:
                                        x_axis1=[]
                                        y_axis1=[]
                                        z_axis1=[]

                                        Node_adi = f"Node {int(b[0])}"
                                        x_axis1.append(nodes[Node_adi][1])
                                        y_axis1.append(nodes[Node_adi][2])
                                        z_axis1.append(nodes[Node_adi][3])

                                        Node_adi = f"Node {int(b[1])}"
                                        x_axis1.append(nodes[Node_adi][1])
                                        y_axis1.append(nodes[Node_adi][2])
                                        z_axis1.append(nodes[Node_adi][3])

                                        Node_adi = f"Node {int(b[2])}"
                                        x_axis1.append(nodes[Node_adi][1])
                                        y_axis1.append(nodes[Node_adi][2])
                                        z_axis1.append(nodes[Node_adi][3])

                                        

                                        x=x_axis1
                                        y=y_axis1
                                        z=z_axis1 
                                        #name=f'Element {b[2]}'
                                        #element_name =f'Element {int(b[2])}'

                                        scatter_line = go.Scatter3d(
                                            x=x_axis1, y=y_axis1,z=z_axis1, mode='lines+text',
                                            line=dict(color='black'),
                                            showlegend=False
                                                    
                                            )
                                        
                                        scatter_nodes = go.Scatter3d(
                                            x=x, y=y,z=z, mode='markers+text',
                                            marker=dict(color='red'),
                                            showlegend=False
                                            )
                                        
                                
                                
                                        st.session_state.graph_state_node_open.add_trace(scatter_line)
                                    
                                        
                            st.plotly_chart(st.session_state.graph_state_node_open)

            with tab_support:
                col_part1, col_part2 = st.columns(2)

                with col_part1:
                    if option=='2D':
                        st.header('Support Table')
                        df_support = st.data_editor(st.session_state.data_support_open, column_config={
                        'Support Node Number': st.column_config.SelectboxColumn(options=st.session_state.data_node['Node Number'].tolist(), required=True),
                        'X direction': st.column_config.CheckboxColumn('X direction',default=False,required="True"),
                        'Y direction': st.column_config.CheckboxColumn('Y direction',default=False,required="True"),
                        'Moment': st.column_config.CheckboxColumn('Moment',default=False,required="True"),
                        'Remove': st.column_config.CheckboxColumn('Remove',default=False,required="True")
                        }, hide_index=True, num_rows="dynamic")
                
                     
                        def _finish_():
                            st.session_state.data_support_open = df_support.copy()
                            for index,row in st.session_state.data_support_open.iterrows():
                                node_number = int(row['Support Node Number'])
                                x_direction = 1 if int(row['X direction'])== True else 0  # True ise 1, False ise 0
                                y_direction = 1 if int(row['Y direction'])== True else 0  # True ise 1, False ise 0
                                moment = 1 if int(row['Moment'])==True else 0  # True ise 1, False ise 0
                                Remove = 1 if int(row['Remove'])==True else 0  # True ise 1, False ise 0
                                indexx= st.session_state.data_node_open.to_dict(orient='list')['Node Number'].index(node_number)
                                x_axis_sup = st.session_state.data_node_open.to_dict(orient='list')['Node x'][indexx]      
                                y_axis_sup = st.session_state.data_node_open.to_dict(orient='list')['Node y'][indexx]
                    
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
                                    st.session_state.graph_state_node_open.add_trace(scatter_triangle)                           

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
                                    st.session_state.graph_state_node_open.add_trace(scatter_square)
                                    


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
                                    st.session_state.graph_state_node_open.add_trace(scatter_triangle_y)
                                        

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
                                    st.session_state.graph_state_node_open.add_trace(scatter_triangle_x)
                                    
                                    
                                elif Remove==1:
                                    scatter_triangle_index = None
                                    for i, trace in enumerate(st.session_state.graph_state_node_open.data):
                                        if 'marker' in trace and 'symbol' in trace['marker'] and trace['marker']['symbol'] == 'triangle-up':
                                            scatter_triangle_index = i
                                            break
                                        
                                    # scatter_triangle'ı kaldırma
                                    if scatter_triangle_index is not None:
                                        graph_data_list = list(st.session_state.graph_state_node_open.data)
                                        graph_data_list.pop(scatter_triangle_index)
                                        
                                        st.session_state.graph_state_node_open.data = graph_data_list
                                    
                                    scatter_square_index = None
                                    for i, trace in enumerate(st.session_state.graph_state_node_open.data):
                                        if 'marker' in trace and 'symbol' in trace['marker'] and trace['marker']['symbol'] == 'square':
                                            scatter_square_index = i
                                            break

                                    # scatter_triangle'ı kaldırma
                                    if scatter_square_index is not None:
                                        graph_data_list = list(st.session_state.graph_state_node_open.data)
                                        graph_data_list.pop(scatter_square_index)
                        
                                        st.session_state.graph_state_node_open.data = graph_data_list
                                    
                                    scatter_triangle_y_index = None
                                    for i, trace in enumerate(st.session_state.graph_state_node_open.data):
                                        if 'marker' in trace and 'symbol' in trace['marker'] and trace['marker']['symbol'] == 'triangle-up'and trace['marker']['color']== 'MediumPurple':
                                            scatter_triangle_y_index = i
                                            break

                                    # scatter_triangle'ı kaldırma
                                    if scatter_triangle_y_index is not None:
                                        graph_data_list = list(st.session_state.graph_state_node_open.data)
                                        graph_data_list.pop(scatter_triangle_y_index)
                                        
                                        st.session_state.graph_state_node_open.data = graph_data_list

                                    scatter_triangle_x_index = None
                                    for i, trace in enumerate(st.session_state.graph_state_node_open.data):
                                        if 'marker' in trace and 'symbol' in trace['marker'] and trace['marker']['symbol'] == 'triangle-right':
                                            scatter_triangle_x_index = i
                                            break

                                    # scatter_triangle'ı kaldırma
                                    if scatter_triangle_x_index is not None:
                                        graph_data_list = list(st.session_state.graph_state_node_open.data)
                                        graph_data_list.pop(scatter_triangle_x_index)
                                        
                                        st.session_state.graph_state_node_open.data = graph_data_list

                                else:
                                    st.write("Please, Check your selection.")
                    #################3d support graifiğinde x,y,z de tutulu pin ve xyz de tutulu fixed support için doğru çiziyor,diğerleri sonra bakılacak.

                    else:
                        df_support = st.data_editor(st.session_state.data_support_3d_open, column_config={
                        'Support Node Number': st.column_config.SelectboxColumn(options=st.session_state.data_node_3d_open['Node Number'].tolist(), required=True),
                        'X translation(3d)': st.column_config.CheckboxColumn('X translation(3d)',default=False,required="True"),
                        'Y translation(3d)': st.column_config.CheckboxColumn('Y translation(3d)',default=False,required="True"),
                        'Z translation(3d)': st.column_config.CheckboxColumn('Z translation(3d)',default=False,required="True"),
                        'Rotation about x(3d)': st.column_config.CheckboxColumn('Rotation about x(3d)',default=False,required="True"),
                        'Rotation about y(3d)': st.column_config.CheckboxColumn('Rotation about y(3d)',default=False,required="True"),
                        'Rotation about z(3d)': st.column_config.CheckboxColumn('Rotation about z(3d)',default=False,required="True"),
                        'Remove(3d)': st.column_config.CheckboxColumn('Remove(3d)',default=False,required="True")
                        }, hide_index=True, num_rows="dynamic")

                        def _finish_():
            
                            st.session_state.data_support_3d_open = df_support.copy()
                            for index,row in st.session_state.data_support_3d_open.iterrows():
                                node_number = int(row['Support Node Number(3d)'])
                                x_direction = 1 if int(row['X translation(3d)'])== True else 0  # True ise 1, False ise 0
                                y_direction = 1 if int(row['Y translation(3d)'])== True else 0  # True ise 1, False ise 0
                                z_direction = 1 if int(row['Z translation(3d)'])== True else 0
                                moment_x = 1 if int(row['Rotation about x(3d)'])==True else 0  # True ise 1, False ise 0
                                moment_y = 1 if int(row['Rotation about y(3d)'])==True else 0  # True ise 1, False ise 0
                                moment_z = 1 if int(row['Rotation about z(3d)'])==True else 0  # True ise 1, False ise 0
                                Remove = 1 if int(row['Remove(3d)'])==True else 0  # True ise 1, False ise 0
                                indexx= st.session_state.data_node_3d_open.to_dict(orient='list')['Node Number'].index(node_number)
                                x_axis_sup = st.session_state.data_node_3d_open.to_dict(orient='list')['Node x'][indexx]      
                                y_axis_sup = st.session_state.data_node_3d_open.to_dict(orient='list')['Node y'][indexx]
                                z_axis_sup = st.session_state.data_node_3d_open.to_dict(orient='list')['Node z'][indexx]
                    
                                if x_direction==1 and y_direction==1 and z_direction==1 and moment_x==0 and moment_y==0 and moment_z==0 and Remove==0:
                                    scatter_triangle = go.Scatter3d(
                                            x=[x_axis_sup], y=[y_axis_sup],z=[z_axis_sup], 
                                            mode='markers',
                                            marker=dict(
                                                    symbol='cross',
                                                    size=10,
                                                    color='LightSkyBlue'),
                                            showlegend=False          
                                            )
                                    st.session_state.graph_state_node_open.add_trace(scatter_triangle)                           

                                elif x_direction==1 and y_direction==1 and z_direction==1 and moment_x==1 and moment_y==1 and moment_z==1 and Remove==0:
                                    scatter_square = go.Scatter3d(
                                            x=[x_axis_sup], y=[y_axis_sup],z=[z_axis_sup],
                                            mode='markers',
                                            marker=dict(
                                                    symbol='square',
                                                    size=10,
                                                    color='LightSkyBlue'),
                                            #line=dict(color='black'),
                                            showlegend=False          
                                            )
                                    st.session_state.graph_state_node_open.add_trace(scatter_square)
                                    


                                elif x_direction==0 and y_direction==1 and z_direction==0 and moment_x==0 and moment_y==0 and moment_z==0 and Remove==0:
                                    scatter_triangle_y = go.Scatter3d(
                                            x=[x_axis_sup], y=[y_axis_sup],z=[z_axis_sup],
                                            mode='markers',
                                            marker=dict(
                                                    symbol='cross',
                                                    size=10,
                                                    color='MediumPurple',
                                                    line=dict(color='LightSkyBlue',width=2)),
                                            showlegend=False          
                                            )
                                    st.session_state.graph_state_node_open.add_trace(scatter_triangle_y)
                                        

                                elif x_direction==1 and y_direction==0 and moment_x==0 and moment_y==0 and moment_z==0 and Remove==0:
                                    
                                    scatter_triangle_x = go.Scatter3d(
                                            x=[x_axis_sup], y=[y_axis_sup],z=[z_axis_sup],
                                            mode='markers',
                                            marker=dict(
                                                    symbol='cross',
                                                    size=10,
                                                    color='MediumPurple',
                                                    line=dict(color='LightSkyBlue',width=2)),
                                            showlegend=False          
                                            )
                                    st.session_state.graph_state_node_open.add_trace(scatter_triangle_x)
                                    
                                    
                                elif Remove==1:
                                    scatter_triangle_index = None
                                    for i, trace in enumerate(st.session_state.graph_state_node_open.data):
                                        if 'marker' in trace and 'symbol' in trace['marker'] and trace['marker']['symbol'] == 'triangle-up':
                                            scatter_triangle_index = i
                                            break
                                        
                                    # scatter_triangle'ı kaldırma
                                    if scatter_triangle_index is not None:
                                        graph_data_list = list(st.session_state.graph_state_node_open.data)
                                        graph_data_list.pop(scatter_triangle_index)
                                        
                                        st.session_state.graph_state_node_open.data = graph_data_list
                                    
                                    scatter_square_index = None
                                    for i, trace in enumerate(st.session_state.graph_state_node_open.data):
                                        if 'marker' in trace and 'symbol' in trace['marker'] and trace['marker']['symbol'] == 'square':
                                            scatter_square_index = i
                                            break

                                    # scatter_triangle'ı kaldırma
                                    if scatter_square_index is not None:
                                        graph_data_list = list(st.session_state.graph_state_node_open.data)
                                        graph_data_list.pop(scatter_square_index)
                        
                                        st.session_state.graph_state_node_open.data = graph_data_list
                                    
                                    scatter_triangle_y_index = None
                                    for i, trace in enumerate(st.session_state.graph_state_node_open.data):
                                        if 'marker' in trace and 'symbol' in trace['marker'] and trace['marker']['symbol'] == 'cross'and trace['marker']['color']== 'MediumPurple':
                                            scatter_triangle_y_index = i
                                            break

                                    # scatter_triangle'ı kaldırma
                                    if scatter_triangle_y_index is not None:
                                        graph_data_list = list(st.session_state.graph_state_node_open.data)
                                        graph_data_list.pop(scatter_triangle_y_index)
                                        
                                        st.session_state.graph_state_node_open.data = graph_data_list

                                    scatter_triangle_x_index = None
                                    for i, trace in enumerate(st.session_state.graph_state_node_open.data):
                                        if 'marker' in trace and 'symbol' in trace['marker'] and trace['marker']['symbol'] == 'cross':
                                            scatter_triangle_x_index = i
                                            break

                                    # scatter_triangle'ı kaldırma
                                    if scatter_triangle_x_index is not None:
                                        graph_data_list = list(st.session_state.graph_state_node_open.data)
                                        graph_data_list.pop(scatter_triangle_x_index)
                                        
                                        st.session_state.graph_state_node_open.data = graph_data_list

                                else:
                                    st.write("Please, Check your selection.")

                    
                
                with col_part2:
                    st.plotly_chart(st.session_state.graph_state_node_open)
                    finish= st.button('Finish', on_click=_finish_)
                    if finish:
                        st.success("OK :)")     

            with tab_load:
                st.write('Please do not delete the node load even if you do not have a nodal load')
                systemweight=st.checkbox('Include System Self Weight')
                loadtype=['Dead','Live','Wind','Snow','Earhtquake','Other Loads']
                col_part1, col_part2,col_part3 = st.columns(3)

                with col_part1:
                    df_load_node = st.data_editor(st.session_state.data_load_node_open,column_config={
                        'Load Node Number': st.column_config.SelectboxColumn(options=st.session_state.data_node_open['Node Number'].tolist(), required=True),
                        'Load Type(Point)': st.column_config.SelectboxColumn(options=loadtype, required=True)}, num_rows="dynamic")     
                with col_part2:
                    df_load_element = st.data_editor(st.session_state.data_load_element_open,column_config={
                        'Load Element Number': st.column_config.SelectboxColumn(options=st.session_state.data_element_open['Element Number'].tolist(), required=True),
                    'Load Type(Distributed)': st.column_config.SelectboxColumn(options=loadtype, required=True)}
                    , num_rows="dynamic")  

                def _load_():
                    st.session_state.data_load_element_open = df_load_element.copy()
                    st.session_state.data_load_node_open = df_load_node.copy()
            
                
                with col_part3:
                    Determine =st.button('Determine',on_click= _load_ )

                    if Determine:
                            
                        fig1=st.session_state.graph_state_node_open  #drawing the last graph to add loads later. 
                        x_point=[] #Creating the lists of coordinates for point loads
                        y_point=[]
                        u_point=[]#Creating the lists of magnitudes of vectors for point loads
                        v_point=[] 
                        name_point=[]#Creating the lists of names of vectors for point loads
                        for index, row in st.session_state.data_load_node_open.iterrows():
                            
                            up=float(row['Px'])
                            vp=float(row['Py'])
                            xp=st.session_state.data_node_open.loc[st.session_state.data_node_open['Node Number']==float(row['Load Node Number']),'Node x']
                            yp=st.session_state.data_node_open.loc[st.session_state.data_node_open['Node Number']==float(row['Load Node Number']),'Node y']
                            n=str((up**2+vp**2)**0.5)  #calculation of vector magnitude
                            name_p=f"{n} kN"


                            x_point.append(xp)
                            y_point.append(yp)
                            u_point.append(up)
                            v_point.append(vp)
                            name_point.append(name_p)
                        for i in name_point:
                            fig2 = ff.create_quiver(x_point, y_point, u_point, v_point,line_color='red',scale=0.05,name=i) #creating vectors
                        
                            fig1.add_traces(data = fig2.data) #adding vectors the last graph
                        
                    
                        #To create vectors for uniform loading,it was preffered to merge element and uniform load table
                        df_all=pd.merge(st.session_state.data_load_element_open,st.session_state.data_element_open,left_on='Load Element Number',right_on='Element Number')
                        df_all['Load Element Number'] = df_all['Element Number']
                        df_all = df_all.drop(columns=['Element Number'])
                        #df_all.drop(['Section'],axis=1,inplace=True)
                        df_all['First_x_node'] = df_all['First Node Number'].map(st.session_state.data_node_open.set_index('Node Number')['Node x']) #adding x and y coordinate information of df_All dataframe
                        df_all['Second_x_node'] = df_all['Second Node Number'].map(st.session_state.data_node_open.set_index('Node Number')['Node x'])
                        df_all['First_y_node'] = df_all['First Node Number'].map(st.session_state.data_node_open.set_index('Node Number')['Node y'])
                        df_all['Second_y_node'] = df_all['Second Node Number'].map(st.session_state.data_node_open.set_index('Node Number')['Node y'])
                    
                        #Creating the lists of coordinates and vector magntiudes and their names
                        st.dataframe(df_all)            
                        u_element=[]
                        v_element=[]
                        x_element=[]
                        y_element=[]
                        uniform_name=[]
                        for index,row in df_all.iterrows():
                            a=float(row['First_x_node'])-float(row['Second_x_node'])
                            b=float(row['First_y_node'])-float(row['Second_y_node'])
                            element_length=(a**2 + b**2)**0.5
                            x_e=np.arange(float(row['First_x_node']),float(row['Second_x_node']),float(element_length/10))
                            y_e=np.arange(float(row['First_y_node']),float(row['Second_y_node']),float(element_length/10))
                            u_e=float(row['Wx'])
                            v_e=float(row['Wy'])
                            q=str(((u_e)**2+(v_e)**2)**0.5)
                            name_q=f"{q} kN/m"
                            uniform_name.append(name_q)
                            
                            if len(x_e)>0 and len(y_e)==0:
                                x_element.append(x_e)
                                y_element.append(np.full(len(x_e),float(row['First_y_node'])))
                                u_element.append(np.full(len(x_e),u_e))
                                v_element.append(np.full(len(x_e),v_e))
                                
                                
                            elif len(y_e)>0 and len(x_e)==0:
                                y_element.append(y_e)
                                x_element.append(np.full(len(y_e),float(row['First_x_node'])))
                                u_element.append(np.full(len(y_e),u_e))
                                v_element.append(np.full(len(y_e),v_e))
                            else:
                                x_element.append(x_e)
                                y_element.append(y_e)

                                u_element.append(np.full(len(x_e),u_e))
                                v_element.append(np.full(len(y_e),v_e))
                        #Creating the vectors for uniform loading
                        for i in uniform_name:

                            fig3 = ff.create_quiver(x_element, y_element, u_element, v_element,line_color='blue',scale=0.05,name=i)
                            fig1.add_traces(data = fig3.data)  #adding the last graph
                        
                        fig1.update_yaxes(range=[-1, 10]) #boundaries are set for graph because the graph makes autoscaling
                        fig1.update_xaxes(range=[-1, 20])
                        st.plotly_chart(fig1)
                        st.success("Ok :)")

                ##########INCLUDING SYSTEM WEIGHT#############3 
                _load_()
                wx_dead_loads=[]
               
                element_df=df_load_element.copy() # dead loads are not shown on load graph so element_df and node_df is created to not change any dataframe that helps to draw load graph
                node_all_loads=df_load_node.copy()
                if systemweight:
                    for index, row in st.session_state.df_element_length.iterrows():
                        if row['First_y_node']==row['Second_y_node']:
                        
                            deadload={
                                        'Load Element Number':row['Element Number'],
                                        'Wx':0,
                                        'Wy':-float(row['Weight (kN)'])/float(row['Element Length (m)']),
                                        'Load Type(Distributed)':'Dead'
                                        }
                            wx_dead_loads.append(deadload)

                        if row['First_x_node']==row['Second_x_node']:
                        
                            deadload={
                                        'Load Element Number':row['Element Number'],
                                        'Wx':float(row['Weight (kN)'])/float(row['Element Length (m)']),
                                        'Wy':0,
                                        'Load Type(Distributed)':'Dead'
                                        }
                            wx_dead_loads.append(deadload)    
                        
                    element_all_loads=pd.concat([element_df,pd.DataFrame(wx_dead_loads)],ignore_index=True)
                
                    st.dataframe(node_all_loads)
                    st.dataframe(element_all_loads)
            with tab_loadcomb:
                
                df_load_combination = st.data_editor(st.session_state.data_load_combination_open, num_rows="dynamic")        
                def load_comb():
                        st.session_state.data_load_combination_open = df_load_combination.copy()
                Determine_loadcomb= st.button('Apply', on_click=_finish_)

            with tab_lastmodel:
                st.write('Do you want to see the final model?')
                st.write('You should press the (See Model) button if you want. :)')

                buttons = st.button('See Model')


                if buttons:
                    
                    st.plotly_chart(st.session_state.graph_state_node_open)

                    col_part1,col_part2,col_part3,col_part4,col_part5=st.columns(5)
                
                    with col_part1:
                        st.header('Node Table')
                        df_node = AgGrid(st.session_state.data_node_open)
                    with col_part2:        
                        st.header('Element Table')
                        df_element = AgGrid(st.session_state.data_element_open)
                    with col_part3:
                        st.header('Support Table')
                        df_support = AgGrid(st.session_state.data_support_open)
                    with col_part4:
                        st.header('Node Load Table')
                        df_load_node = AgGrid(st.session_state.data_load_node_open)
                    with col_part5:
                        st.header('Element Load Table')

        with tab_results:

            Analyze = st.button("Analyze")
            
            if Analyze:
                def _ops_():
                    ops.wipe()  #required to open a new model
                    ops.model('basic', '-ndm', 2, '-ndf', 3)
                    Ew={}
                    #st.session_state.data_node =df_node.copy()
                    i=0
                    for index, row in st.session_state.data_node_open.iterrows():
                        node_number = int(row['Node Number'])
                        indexx= st.session_state.data_node_open.to_dict(orient='list')['Node Number'].index(node_number)
                        x_axis_node = st.session_state.data_node_open.to_dict(orient='list')['Node x'][indexx]      
                        y_axis_node = st.session_state.data_node_open.to_dict(orient='list')['Node y'][indexx]
                        ops.node(i+1,x_axis_node,y_axis_node)
                        i+=1
                    
                    ops.geomTransf('Linear', 1)
                    #st.session_state.data_element = df_element.copy()
                    E = st.session_state.data_section_open['Modulus of Elastisity (MPa)']
                    for index,row in st.session_state.data_element_open.iterrows():
                        first_node = int(row['First Node Number'])
                        second_node = int(row['Second Node Number'])
                        element_num = int(row['Element Number'])
                        section_elm = (row['Section'])
                        indexx= st.session_state.data_section_open.to_dict(orient='list')['Section Name'].index(section_elm)
                        A = st.session_state.data_section_open.to_dict(orient='list')['Area(m^2)'][indexx]      
                        I = st.session_state.data_section_open.to_dict(orient='list')['I(2-2)(m^4)'][indexx]
                        
                        M = 0.
                        massType = "-lMass"
                        
                        ops.element('elasticBeamColumn',element_num,first_node,second_node,A,E[0],I,1,'-mass', M, massType)
                    
                    #st.session_state.data_support = df_support.copy()
                    for index, row in st.session_state.data_support_open.iterrows():
                        node_number = int(row['Support Node Number'])
                        x_direction = int(row['X direction'])
                        y_direction = int(row['Y direction'])
                        moment = int(row['Moment'])
                        ops.fix(node_number,x_direction,y_direction,moment)
                    
                    ops.timeSeries('Constant', 1)
                    ops.pattern('Plain', 1, 1)
                    

                    for index, row in element_all_loads.iterrows():
                        Ew[int(row['Load Element Number'])]=['-beamUniform',float(row['Wy']),float(row['Wx'])]
                        print(Ew)

                    for etag in Ew:
                        ops.eleLoad('-ele', etag, '-type', Ew[etag][0], Ew[etag][1],Ew[etag][2])
        
                    for index, row in node_all_loads.iterrows():
                        ops.load(int(row['Load Node Number']),float(row['Px']),float(row['Py']),float(row['Mz']))
                    
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
                
                col_part1, col_part2,col_part3,col_part4,col_part5 = st.columns(5)

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

                            with col_part4:
                                numFloor=storynumber
                                numBay=baynumber
                                bayWidth=beamlength[0:baynumber:1]
                                bayWidth = [i for i in bayWidth for _ in range(2)]
                                print(columnlength)
                                storyHeights=columnlength[0::baynumber]

                                #mass for each element
                                listofbeamweights=[]
                                listofcolumnweights=[]
                                st.session_state.df_element_length_open=st.session_state.df_element_length_open.sort_values(by=['Story Level'],ascending=False) #sorting from the top story to bottom story
                                for index, row in st.session_state.df_element_length_open.iterrows():
                                    if row['First_y_node']==row['Second_y_node']:
                                        listofbeamweights.append((row['Weight (kN)'])/9.81)
                                    if row['First_x_node']==row['Second_x_node']:
                                        listofcolumnweights.append((row['Weight (kN)'])/(9.81*2))  #ton
                                col=[]# finding column masses for each story(lumped mass)
                                for i in range(0,len(listofcolumnweights),numBay+1):
                                    sumcol=sum(listofcolumnweights[i:i+numBay+1])
                                    col.append(sumcol)   
                                massxcolumn=[]
                                for i in range(0,len(col)-1):
                                    weight_1=col[i]+col[i+1]
                                    massxcolumn.append(weight_1)
                                massxcolumn.insert(0,col[0])

                                #finding beam masses for each story(lumped mass)
                                massxbeam=[]
                                for i in range(0,len(listofbeamweights),numBay):
                                    sumbeam=sum(listofbeamweights[i:i+numBay])
                                    massxbeam.append(sumbeam)
                                #summing beams and column masses for each lumped mass
                                massxstory=[sum(i) for i in zip(massxbeam, massxcolumn)]
                                massxstory=massxstory[::-1] #sorting from bottom story to top story
                                
                                ops.wipe()
                                ops.model('Basic', '-ndm', 2)

                                E = 250000
                                
                                coordTransf = "Linear"  # Linear, PDelta, Corotational
                            

                            
                                #column sections for each column 
                                
                                columntable=st.session_state.df_element_length_open
                                columntable=columntable.sort_values(by='First_x_node')
                                columntable = columntable[columntable['First_x_node'] == columntable['Second_x_node']]

                                columntable['A']=columntable['Section'].map( st.session_state.data_section_open.set_index('Section Name')['Area(m^2)'])
                                columntable['I']=columntable['Section'].map( st.session_state.data_section_open.set_index('Section Name')['I(2-2)(m^4)'])
                                columnsections=[]
                                
                                for i in range(0,len(columntable),storynumber):
                                    columntable2=columntable.iloc[i:i+storynumber]
                                    columntable2=columntable2.sort_values(by='First_y_node')
                                    columnsections+=columntable2['Section'].tolist()
                                columnsections = [columnsections[i:i+storynumber] for i in range(0, len(columnsections), storynumber)]
                                print(columnsections)
                                    
                                #beam sections for each story
                                beamtable=st.session_state.df_element_length_open.sort_values(by='First_y_node')
                                beamtable = beamtable[beamtable['First_y_node'] == beamtable['Second_y_node']]
                                beamtable['A']=beamtable['Section'].map( st.session_state.data_section_open.set_index('Section Name')['Area(m^2)'])
                                beamtable['I']=beamtable['Section'].map( st.session_state.data_section_open.set_index('Section Name')['I(2-2)(m^4)'])
                                beamsections=[]
                                for i in range(0,len(beamtable)):
                                    beamtable2=beamtable.iloc[i:i+numBay]
                                    beamtable2=beamtable2.sort_values(by='First_x_node')
                                    beamsections.extend(beamtable2['Section'].tolist())


                                section_all={}
                                for index,row in columntable.iterrows():
                                    key=row['Section']
                                    A=row['A']
                                    I=row['I']
                                    if key not in section_all:
                                        section_all[key]=[A,I]
                                for index,row in beamtable.iterrows():
                                    key=row['Section']
                                    A=row['A']
                                    I=row['I']
                                    if key not in section_all:
                                        section_all[key]=[A,I]
                                
                                
                                

                                # procedure to read
                                def ElasticBeamColumn(eleTag, iNode, jNode, sectType, E, transfTag, M, massType):
                                    found = 0

                                    prop = section_all[sectType]
                                    A = prop[0]
                                    I = prop[1]
                                    ops.element('elasticBeamColumn', eleTag, iNode, jNode, A, E, I, transfTag, '-mass', M, massType)

                                

                                # add the nodes
                                #  - floor at a time
                                yLoc = 0.
                                nodeTag = 1
                                for j in range(0, numFloor + 1):   #  NODE OLUŞTURMA

                                    xLoc = 0.
                                    for i in range(0, numBay + 1):
                                        ops.node(nodeTag, xLoc, yLoc)
                                        if yLoc==0:
                                            ops.fix(nodeTag,1,1,1)

                                        xLoc += bayWidth[i]
                                        nodeTag += 1

                                    if j < numFloor:
                                        storyHeight = storyHeights[j]

                                    yLoc += storyHeight

                                # fix first floor

                                #for index,row in st.session_state.data_node[st.session_state.data_node['Node y']==0].iterrows():
                                    #   ops.fix(int(row['Node Number']),1,1,1)
                                

                                # rigid floor constraint & masses

                                nodeTagR = baynumber+3
                                nodeTag = baynumber+2
                                a_j=0
                                
                                for j in range(1, numFloor + 1):
                                    for i in range(0, numBay + 1):

                                        if nodeTag != nodeTagR:
                                            ops.equalDOF(nodeTagR, nodeTag, 1)
                                            print(nodeTagR, nodeTag, 1)
                                        else:
                                            for a_j in massxstory:
                                                ops.mass(nodeTagR, a_j, 1.0e-10, 1.0e-10)
                                                print(nodeTagR, a_j, 1.0e-10, 1.0e-10)
                                                a_j+=1
                                                break

                                        nodeTag += 1

                                    nodeTagR += numBay + 1
                                
                                M = 0.
                                massType = "-lMass"

                                # add the columns
                                # add column element
                                ops.geomTransf(coordTransf, 1)

                                eleTag = 1

                                for j in range(0, numBay + 1):

                                    end1 = j + 1
                                    end2 = end1 + numBay + 1
                                    thisColumn = columnsections[j]

                                    for i in range(0, numFloor):
                                        secType = thisColumn[i]
                                        ElasticBeamColumn(eleTag, end1, end2, secType, E, 1, M, massType)
                                        end1 = end2
                                        end2 += numBay + 1
                                        eleTag += 1

                                # add beam elements
                                for j in range(1, numFloor + 1):
                                    end1 = (numBay + 1) * j + 1
                                    end2 = end1 + 1
                                    
                                    for i in range(0, numBay):
                                        secType = beamsections[i]
                                        ElasticBeamColumn(eleTag, end1, end2, secType, E, 1, M, massType)
                                        end1 = end2
                                        end2 = end1 + 1
                                        eleTag += 1
                            

                                
                                # calculate eigenvalues & print results
                                numEigen = len(storyHeights)+1
                                eigenValues = ops.eigen('-fullGenLapack',numEigen)
                                PI = 2 * asin(1.0)
                                ops.timeSeries('Linear', 1)
                                ops.pattern('Plain', 1, 1)
                                ops.integrator('LoadControl', 1.0)
                                ops.algorithm('Linear')
                                ops.analysis('Static')
                                ops.analyze(1)
                                periodlist=[]
                                for i in range(0,numEigen):
                                    period=2*PI/sqrt(eigenValues[i])
                                    periodlist.append(period)
                                opsv.plot_model()
                                st.pyplot(plt.gcf())
                                st.write(periodlist)
                                ops.modalProperties('-print', '-file', 'ModalReport2.txt', '-unorm')
                                ops.responseSpectrumAnalysis(1,1)
                                
                                with col_part5:

                                    modenumbers=list(range(1, numEigen+1))
                                    df_period=pd.DataFrame({
                                        'Mode Number':modenumbers,
                                        'Period':periodlist
                                    })
                                    st.session_state.data_period_open=st.data_editor(df_period,num_rows='dynamic')


                                    opsv.plot_mode_shape(1)
                                    st.pyplot(plt.gcf())
                exit()


if selected_page == "New":
    st.sidebar.subheader("New")
    tab_model,tab_results=st.tabs(["Model", "Analysis"])

    def _json_download_():
        df_dict={}
        df_dict_node= st.session_state.data_node.to_dict(orient='list')
        df_dict_node_3d= st.session_state.data_node_3d.to_dict(orient='list')
        df_dict_section=st.session_state.data_section.to_dict(orient='list')
        df_dict_data_element=st.session_state.data_element.to_dict(orient='list')
        df_dict_df_element=st.session_state.df_element.to_dict(orient='list')
        df_dict_df_element_length=st.session_state.df_element_length.to_dict(orient='list')
        df_dict_support = st.session_state.data_support.to_dict(orient='list')
        df_dict_support_3d = st.session_state.data_support_3d.to_dict(orient='list')
        df_dict_load_node =  st.session_state.data_load_node.to_dict(orient='list')
        df_dict_load_element = st.session_state.data_load_element.to_dict(orient='list')
        df_dict_load_combination = st.session_state.data_load_combination.to_dict(orient='list')
        df_dict_data_period =st.session_state.data_period.to_dict(orient='list')
        df_dict.update(df_dict_node)
        df_dict.update(df_dict_node_3d)
        df_dict.update(df_dict_section)
        df_dict.update(df_dict_data_element)
        df_dict.update(df_dict_df_element)
        df_dict.update(df_dict_df_element_length)
        df_dict.update(df_dict_support)
        df_dict.update(df_dict_support_3d)
        df_dict.update(df_dict_load_node)
        df_dict.update(df_dict_load_element)
        df_dict.update(df_dict_load_combination)
        df_dict.update(df_dict_data_period)
        print(df_dict,"bbbbb")
        
        Json_data = json.dumps(df_dict)
        with open('Data.json', 'w') as file:
            json.dump(Json_data, file)
        st.success("File downloaded.")

    Download_json = st.sidebar.button("Download as A json File", on_click=_json_download_)
    
    with tab_model:
        
        tab_node, tab_section, tab_element,tab_support,tab_load,tab_loadcomb,tab_lastmodel = st.tabs(
            ["Node", 'Section',"Element",'Support Conditions',"Loads",'Load Combinations',"Last Model"]
        )

        with tab_node:
            col_part1, col_part2 = st.columns(2)
            with col_part1:
                option=st.selectbox(
                    'Select your dimension.',('2D','3D') )

                st.header("Node Table") 
                button_save_data = st.button("Save and Sketch")

                if option=='2D':
                    if not button_save_data:
                        edited_df = st.data_editor(st.session_state.data_node, hide_index=True, num_rows="dynamic")

                    if button_save_data:
                    
                        df_node = st.data_editor(st.session_state.data_node,hide_index=True, num_rows="dynamic")
                        st.session_state.data_node =df_node.copy()
                        st.success("Data saved successfully!")

                else:
                    if not button_save_data:
                        edited_df = st.data_editor(st.session_state.data_node_3d,hide_index=True, num_rows="dynamic")
                 
                    if button_save_data:
                    
                        df_node = st.data_editor(st.session_state.data_node_3d,hide_index=True, num_rows="dynamic")
                        st.session_state.data_node_3d =df_node.copy()
                        st.success("Data saved successfully!")

            with col_part2:
                if option=='2D': 
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
                                if any(isinstance(trace, go.Scatter) for trace in st.session_state.graph_state_node.data):
                                # Scatter grafiğini sil
                                    st.session_state.graph_state_node.data = [trace for trace in st.session_state.graph_state_node.data if not isinstance(trace, go.Scatter)]

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
                else:
                    if button_save_data:
                    
                        i=0   
                        list_node_2=[]
                        Node_x_axis=[]
                        Node_y_axis=[]
                        Node_z_axis=[]
                        Node_name= []
                        nodes={}

                        while i<len(st.session_state.data_node_3d.index):
                        
                            list_node_1=list(st.session_state.data_node_3d.iloc[i])
                            list_node_2.append(list_node_1)

                            Node_name = [int(node) if not pd.isna(node) else 0 for node in Node_name]
                            Node_adi = f"Node {i+1}"
                            nodes[Node_adi] = (list_node_2[i][0],list_node_2[i][1],list_node_2[i][2],list_node_2[i][3])
                            
                            Node_x_axis.append(list_node_2[i][1])
                            Node_y_axis.append(list_node_2[i][2])
                            Node_z_axis.append(list_node_2[i][3])
                            Node_name.append(list_node_2[i][0])
                            
                            i+=1

                            if i==len(st.session_state.data_node_3d):
                                if any(isinstance(trace, go.Scatter) for trace in st.session_state.graph_state_node_3d.data):
                                # Scatter grafiğini sil
                                    st.session_state.graph_state_node_3d.data = [trace for trace in st.session_state.graph_state_node_3d.data if not isinstance(trace, go.Scatter)]

                                # to describe node for plot
                                x= Node_x_axis
                                y= Node_y_axis
                                z=Node_z_axis

                                Node_name = [int(node) if not pd.isna(node) else 0 for node in Node_name]
                
                                scatter = go.Scatter3d(
                                    x=x, y=y, z=z, mode='markers+text',
                                    text=Node_name, 
                                    marker=dict(color='red'),
                                    textposition='bottom left',
                                    showlegend=False,
                                    )

                                
                                #st.session_state.graph_state_node.data = []
                                #print(st.session_state.graph_state_node.data,"bu ne")
                                st.session_state.graph_state_node_3d.add_trace(scatter)
                    
                    
                    st.plotly_chart(st.session_state.graph_state_node_3d)

        
        with tab_section:
            col_part1, col_part2 = st.columns(spec=[0.78,0.22])

            with col_part1:
                 

                st.write("You must input ;\n"
            "- Section Name\n"
            "- Material\n"
            "- Section Type\n"
            "- Width (m)\n"
            "- Length (m)\n"
            "- Modulus of Elasticity(MPa)\n\n"
            "Don't worry, the other values will be calculated automatically \n"
            ":)) " )

                def calculate_area(length, width):
                    return length * width

                def calculate_moment_of_inertia22(b,h):
                    return (h*(b**3)) / 12
                
                def calculate_moment_of_inertia33(b,h):
                    return (b * (h**3)) / 12

                def calculate_J(b,h):
                    return (calculate_moment_of_inertia22(b,h)+calculate_moment_of_inertia33(b,h))

                
                
                
                def moe(modulus_of_elastisity):
                    return modulus_of_elastisity*1

                def calculate_G(x):
                    return (moe(x)/2)

                

                
                
                st.title("Section Table")           

                df_section = st.data_editor(st.session_state.data_section,
                                    column_config={'Material': st.column_config.SelectboxColumn(options= ['Concrete']),
                                                'Area': st.column_config.Column(disabled=True),
                                                'Moment of İnertia':st.column_config.Column(disabled=True),
                                                'Section Type': st.column_config.SelectboxColumn(options= ['Column','Beam']),
                                                'G(MPa)':st.column_config.Column(disabled=True),
                                                'J(m^4)':st.column_config.Column(disabled=True),
                                                'Self Weight (kN/m)':st.column_config.Column(disabled=True) },
                                    num_rows="dynamic")


                def sw(material):
                    if material == 'Concrete':
                        return 25
                    else:
                        return 0 
                    

                def calculate_self_weight (specific_weight, area, section_type):
                    if section_type == 'Column':
                        return specific_weight * area
                    elif section_type == 'Beam':
                        return specific_weight*area

                


            def _save_button_():
                df_section['Area(m^2)'] = df_section.apply(lambda row: calculate_area(row['Width(m)'], row['Height(m)']), axis=1)
                df_section['I(2-2)(m^4)'] = df_section.apply(lambda row: calculate_moment_of_inertia22(row['Width(m)'], row['Height(m)']), axis=1)
                df_section['I(3-3)(m^4)'] = df_section.apply(lambda row: calculate_moment_of_inertia33(row['Width(m)'], row['Height(m)']), axis=1)
                df_section['Modulus of Elastisity (MPa)'] = df_section.apply(lambda row: moe(row['Modulus of Elastisity (MPa)']), axis=1)
                df_section['J(m^4)'] = df_section.apply(lambda row: calculate_J(row['Width(m)'], row['Height(m)']), axis=1)
                df_section['G(MPa)'] = df_section.apply(lambda row: calculate_G(row['Modulus of Elastisity (MPa)']), axis=1)
                df_section['Spesific Weight (kN/m^3)'] = df_section.apply(lambda row: sw(row['Material']), axis=1)
                df_section['Self Weight (kN/m)'] = df_section.apply(lambda row: calculate_self_weight( row['Spesific Weight (kN/m^3)'], row['Area(m^2)'], row['Section Type']), axis=1)

                st.session_state.data_section = df_section.copy()

           

            save_button = st.button("Save", on_click=_save_button_)

            if save_button:
                st.success("Data saved successfully!")
            with col_part2:
                # Define the width (b) and height (h) of the rectangle
                b = 10  # Width
                h = 5   # Height

                # Create a figure and a set of subplots
                fig, ax = plt.subplots()

                # Draw the rectangle
                rectangle = plt.Rectangle((0, 0), b, h, fill=None, edgecolor='blue')
                ax.add_patch(rectangle)

                # Set the x and y axis limits
                plt.xlim(-1, b + 1)
                plt.ylim(-1, h + 1)

                # Remove axis numbers and ticks
                ax.set_xticks([])
                ax.set_yticks([])
                ax.set_xticklabels([])
                ax.set_yticklabels([])

                # Label the width and height outside the rectangle
                plt.text(b / 2, -0.5, 'Width (b)', ha='center', va='center')
                plt.text(-0.5, h / 2, 'Height (h)', ha='center', va='center', rotation='vertical')

                # Add coordinate system at the center of the rectangle
                center_x = b / 2
                center_y = h / 2

                # Draw x and y axis lines at the center of the rectangle
                ax.arrow(center_x, center_y, b/2 - 0.5, 0, head_width=0.2, head_length=0.5, fc='black', ec='black')
                ax.arrow(center_x, center_y, 0, h/2 - 0.5, head_width=0.2, head_length=0.5, fc='black', ec='black')


                # Label the axes at the center
                plt.text(center_x + b/2 - 0.5, center_y - 0.5, '3-3', ha='center', va='center')
                plt.text(center_x - 0.5, center_y + h/2 - 0.5, '2-2', ha='center', va='center')

                # Set labels for the axes (if needed, adjust as per your requirement)
                plt.xlabel('')
                plt.ylabel('')

                # Display the plot
                plt.gca().set_aspect('equal', adjustable='box')
                plt.grid(False)  # Turn off the grid

                st.pyplot(fig)
                
        with tab_element:
            with tab_element:
                col_part1, col_part2 = st.columns(2)
                with col_part1:
                    listofstories=list(range(0,51))
                    st.write('Please construct the elements from left to right and from top to bottom.')
                    st.session_state.df_element = st.data_editor(st.session_state.data_element
                                                , 
                                                column_config={
                                                    "Section": st.column_config.SelectboxColumn(
                                                        "Section",
                                                        help="The category of the app",
                                                        width="medium",
                                                        options=df_section['Section Name'].tolist(),
                                                        required=True) ,
                                                        'Story Level':st.column_config.SelectboxColumn(
                                                        "Story Level",
                                                        help="The category of the app",
                                                        width="medium",
                                                        options=listofstories,
                                                        required=True),
                                                        "Element Length (m)":st.column_config.Column(disabled=True),
                                                        "Weight (kN)":st.column_config.Column(disabled=True)
                                                },
                                                hide_index=True, num_rows="dynamic")
                    if option=='2D':
                        st.session_state.df_element_length = pd.concat([st.session_state.df_element, st.session_state.data_node], ignore_index=True)
                        
                        st.session_state.df_element_length['First_x_node'] = st.session_state.df_element['First Node Number'].map(st.session_state.data_node.set_index('Node Number')['Node x']) #adding x and y coordinate information of df_All dataframe
                        st.session_state.df_element_length['Second_x_node'] = st.session_state.df_element['Second Node Number'].map(st.session_state.data_node.set_index('Node Number')['Node x'])
                        st.session_state.df_element_length['First_y_node'] = st.session_state.df_element['First Node Number'].map(st.session_state.data_node.set_index('Node Number')['Node y'])
                        st.session_state.df_element_length['Second_y_node'] = st.session_state.df_element['Second Node Number'].map(st.session_state.data_node.set_index('Node Number')['Node y'])
                        st.session_state.df_element_length.drop(columns=['Node Number','Node x','Node y'],inplace=True)
                        
                        def element_length(x0,x1,y0,y1):
                                
                            return ((x0-x1)**2 + (y0-y1)**2)**0.5
                        
                        def weight(rho , length):
                            return rho*length
                        

                        def _element_finish_():
                            
                            st.session_state.df_element["Element Length (m)"] =st.session_state.df_element_length.apply(lambda row: element_length(row['First_x_node'], row['Second_x_node'], row['First_y_node'] , row['Second_y_node'] ), axis=1)
                            
                            
                            i=0
                            
                            df_weight = pd.DataFrame([{'Length':0.0, 'Self Weight' :0.0}])
                            
                            
                            while i < len(st.session_state.df_element["Element Number"]):
                                section_name = st.session_state.df_element["Section"][i]
                                
                                a=0

                                while a < len(st.session_state.data_section["Section Name"]):
                                    if st.session_state.data_section["Section Name"][a] == section_name:
                                        self_weight = st.session_state.data_section["Self Weight (kN/m)"][a]
                                        df_weight.loc[i] = {'Length': 0.0, 'Self Weight': self_weight}
                                        
                                    a += 1
                                
                                i += 1
                            
                            df_weight['Length'] =st.session_state.df_element["Element Length (m)"]           
                            st.session_state.df_element["Weight (kN)"] = df_weight.apply(lambda row: weight(row['Length'], row['Self Weight'] ), axis=1)
                            st.session_state.data_element = st.session_state.df_element.copy()
                            

                        element_finish_button = st.button("finish", on_click= _element_finish_)
                        
                        
                        
                        
                        # finding story and floor numbers to find period
                        beamlength=[]
                        columnlength=[]
                       
                    
                        for index, row in st.session_state.df_element_length.iterrows():
                            if row['First_y_node']==row['Second_y_node']:
                                beamlength.append(row['Element Length (m)'])
                            if row['First_x_node']==row['Second_x_node']:
                                columnlength.append(row['Element Length (m)'])
                        storynumber= len(st.session_state.df_element_length[st.session_state.df_element_length['First_x_node'] == st.session_state.df_element_length['Second_x_node']].groupby('First_y_node').size())
                        baynumber= len(st.session_state.df_element_length[st.session_state.df_element_length['First_y_node'] ==st.session_state. df_element_length['Second_y_node']].groupby('First_x_node').size())
                        print(baynumber,"açıklık")
                        print(storynumber,"kat")
                        
                        
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
                                        
                            st.plotly_chart(st.session_state.graph_state_node, key="unique_key_1")


                    else:
                        st.session_state.df_element_length = pd.concat([st.session_state.df_element, st.session_state.data_node_3d], ignore_index=True)
                        
                        st.session_state.df_element_length['First_x_node'] = st.session_state.df_element['First Node Number'].map(st.session_state.data_node_3d.set_index('Node Number')['Node x']) #adding x,z and y coordinate information of df_All dataframe
                        st.session_state.df_element_length['Second_x_node'] = st.session_state.df_element['Second Node Number'].map(st.session_state.data_node_3d.set_index('Node Number')['Node x'])
                        st.session_state.df_element_length['First_y_node'] = st.session_state.df_element['First Node Number'].map(st.session_state.data_node_3d.set_index('Node Number')['Node y'])
                        st.session_state.df_element_length['Second_y_node'] = st.session_state.df_element['Second Node Number'].map(st.session_state.data_node_3d.set_index('Node Number')['Node y'])
                        st.session_state.df_element_length['First_z_node'] = st.session_state.df_element['First Node Number'].map(st.session_state.data_node_3d.set_index('Node Number')['Node z'])
                        st.session_state.df_element_length['Second_z_node'] = st.session_state.df_element['Second Node Number'].map(st.session_state.data_node_3d.set_index('Node Number')['Node z'])
                        
                        def element_length(x0,x1,y0,y1,z0,z1):
                                
                            return ((x0-x1)**2 + (y0-y1)**2+(z0-z1)**2)**0.5
                        
                        def weight(rho , length):
                            return rho*length
                        

                        def _element_finish_():
                            
                            st.session_state.df_element["Element Length (m)"] =st.session_state.df_element_length.apply(lambda row: element_length(row['First_x_node'], row['Second_x_node'], row['First_y_node'] , row['Second_y_node'],row['First_z_node'], row['Second_z_node'] ), axis=1)
                            
                            
                            i=0
                            
                            df_weight = pd.DataFrame([{'Length':0.0, 'Self Weight' :0.0}])
                            
                            
                            while i < len(st.session_state.df_element["Element Number"]):
                                section_name = st.session_state.df_element["Section"][i]
                                
                                a=0

                                while a < len(st.session_state.data_section["Section Name"]):
                                    if st.session_state.data_section["Section Name"][a] == section_name:
                                        self_weight = st.session_state.data_section["Self Weight (kN/m)"][a]
                                        df_weight.loc[i] = {'Length': 0.0, 'Self Weight': self_weight}
                                        
                                    a += 1
                                
                                i += 1
                            
                            df_weight['Length'] =st.session_state.df_element["Element Length (m)"]           
                            st.session_state.df_element["Weight (kN)"] = df_weight.apply(lambda row: weight(row['Length'], row['Self Weight'] ), axis=1)
                            st.session_state.data_element = st.session_state.df_element.copy()
                            

                        element_finish_button = st.button("finish", on_click= _element_finish_)
                        
                        
                        
                        st.dataframe(st.session_state.df_element_length)
                     

                        
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
                                    Node_z_axis=[]
                                    Node_name= []
                                    nodes={}

                                    while i<len(st.session_state.data_node_3d.index):
                                
                                        list_node_1=list(st.session_state.data_node_3d.iloc[i])
                                        list_node_2.append(list_node_1)

                                        Node_name = [int(node) if not pd.isna(node) else 0 for node in Node_name]
                                        Node_adi = f"Node {i+1}"
                                        nodes[Node_adi] = (list_node_2[i][0],list_node_2[i][1],list_node_2[i][2],list_node_2[i][3])
                                        
                                        Node_x_axis.append(list_node_2[i][1])
                                        Node_y_axis.append(list_node_2[i][2])
                                        Node_z_axis.append(list_node_2[i][3])
                                        Node_name.append(list_node_2[i][0])
                                
                                        i+=1

                                    for b in list4:
                                        x_axis1=[]
                                        y_axis1=[]
                                        z_axis1=[]

                                        Node_adi = f"Node {int(b[0])}"
                                        x_axis1.append(nodes[Node_adi][1])
                                        y_axis1.append(nodes[Node_adi][2])
                                        z_axis1.append(nodes[Node_adi][3])

                                        Node_adi = f"Node {int(b[1])}"
                                        x_axis1.append(nodes[Node_adi][1])
                                        y_axis1.append(nodes[Node_adi][2])
                                        z_axis1.append(nodes[Node_adi][3])

                                        #Node_adi = f"Node {int(b[2])}"
                                        #x_axis1.append(nodes[Node_adi][1])
                                        #y_axis1.append(nodes[Node_adi][2])
                                        #z_axis1.append(nodes[Node_adi][3])

                                        

                                        x=x_axis1
                                        y=y_axis1
                                        z=z_axis1 
                                        #name=f'Element {b[2]}'
                                        #element_name =f'Element {int(b[2])}'

                                        scatter_line = go.Scatter3d(
                                            x=x_axis1, y=y_axis1,z=z_axis1, mode='lines+text',
                                            line=dict(color='black'),
                                            showlegend=False
                                                    
                                            )
                                        
                                        scatter_nodes = go.Scatter3d(
                                            x=x, y=y,z=z, mode='markers+text',
                                            marker=dict(color='red'),
                                            showlegend=False
                                            )
                                        
                                
                                
                                        st.session_state.graph_state_node.add_trace(scatter_line)
                                    
                                        
                            st.plotly_chart(st.session_state.graph_state_node,key="unique0")

        with tab_support:
                col_part1, col_part2 = st.columns(2)

                with col_part1:
                    if option=='2D':
                        st.header('Support Table')
                        df_support = st.data_editor(st.session_state.data_support, column_config={
                        'Support Node Number': st.column_config.SelectboxColumn(options=st.session_state.data_node['Node Number'].tolist(), required=True),
                        'X direction': st.column_config.CheckboxColumn('X direction',default=False,required="True"),
                        'Y direction': st.column_config.CheckboxColumn('Y direction',default=False,required="True"),
                        'Moment': st.column_config.CheckboxColumn('Moment',default=False,required="True"),
                        'Remove': st.column_config.CheckboxColumn('Remove',default=False,required="True")
                        }, hide_index=True, num_rows="dynamic")
                
                     
                        def _finish_():
                            st.session_state.data_support = df_support.copy()
                            for index,row in st.session_state.data_support.iterrows():
                                node_number = int(row['Support Node Number'])
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
                    #################3d support graifiğinde x,y,z de tutulu pin ve xyz de tutulu fixed support için doğru çiziyor,diğerleri sonra bakılacak.

                    else:
                        df_support = st.data_editor(st.session_state.data_support_3d, column_config={
                        'Support Node Number': st.column_config.SelectboxColumn(options=st.session_state.data_node_3d['Node Number'].tolist(), required=True),
                        'X translation': st.column_config.CheckboxColumn('X translation',default=False,required="True"),
                        'Y translation': st.column_config.CheckboxColumn('Y translation',default=False,required="True"),
                        'Z translation': st.column_config.CheckboxColumn('Z translation',default=False,required="True"),
                        'Rotation about x': st.column_config.CheckboxColumn('Rotation about x',default=False,required="True"),
                        'Rotation about y': st.column_config.CheckboxColumn('Rotation about y',default=False,required="True"),
                        'Rotation about z': st.column_config.CheckboxColumn('Rotation about z',default=False,required="True"),
                        'Remove': st.column_config.CheckboxColumn('Remove',default=False,required="True")
                        }, hide_index=True, num_rows="dynamic")

                        def _finish_():
            
                            st.session_state.data_support_3d = df_support.copy()
                            for index,row in st.session_state.data_support_3d.iterrows():
                                node_number = int(row['Support Node Number'])
                                x_direction = 1 if int(row['X translation'])== True else 0  # True ise 1, False ise 0
                                y_direction = 1 if int(row['Y translation'])== True else 0  # True ise 1, False ise 0
                                z_direction = 1 if int(row['Z translation'])== True else 0
                                moment_x = 1 if int(row['Rotation about x'])==True else 0  # True ise 1, False ise 0
                                moment_y = 1 if int(row['Rotation about y'])==True else 0  # True ise 1, False ise 0
                                moment_z = 1 if int(row['Rotation about z'])==True else 0  # True ise 1, False ise 0
                                Remove = 1 if int(row['Remove'])==True else 0  # True ise 1, False ise 0
                                indexx= st.session_state.data_node_3d.to_dict(orient='list')['Node Number'].index(node_number)
                                x_axis_sup = st.session_state.data_node_3d.to_dict(orient='list')['Node x'][indexx]      
                                y_axis_sup = st.session_state.data_node_3d.to_dict(orient='list')['Node y'][indexx]
                                z_axis_sup = st.session_state.data_node_3d.to_dict(orient='list')['Node z'][indexx]
                    
                                if x_direction==1 and y_direction==1 and z_direction==1 and moment_x==0 and moment_y==0 and moment_z==0 and Remove==0:
                                    scatter_triangle = go.Scatter3d(
                                            x=[x_axis_sup], y=[y_axis_sup],z=[z_axis_sup], 
                                            mode='markers',
                                            marker=dict(
                                                    symbol='cross',
                                                    size=10,
                                                    color='LightSkyBlue'),
                                            showlegend=False          
                                            )
                                    st.session_state.graph_state_node.add_trace(scatter_triangle)                           

                                elif x_direction==1 and y_direction==1 and z_direction==1 and moment_x==1 and moment_y==1 and moment_z==1 and Remove==0:
                                    scatter_square = go.Scatter3d(
                                            x=[x_axis_sup], y=[y_axis_sup],z=[z_axis_sup],
                                            mode='markers',
                                            marker=dict(
                                                    symbol='square',
                                                    size=10,
                                                    color='LightSkyBlue'),
                                            #line=dict(color='black'),
                                            showlegend=False          
                                            )
                                    st.session_state.graph_state_node.add_trace(scatter_square)
                                    


                                elif x_direction==0 and y_direction==1 and z_direction==0 and moment_x==0 and moment_y==0 and moment_z==0 and Remove==0:
                                    scatter_triangle_y = go.Scatter3d(
                                            x=[x_axis_sup], y=[y_axis_sup],z=[z_axis_sup],
                                            mode='markers',
                                            marker=dict(
                                                    symbol='cross',
                                                    size=10,
                                                    color='MediumPurple',
                                                    line=dict(color='LightSkyBlue',width=2)),
                                            showlegend=False          
                                            )
                                    st.session_state.graph_state_node.add_trace(scatter_triangle_y)
                                        

                                elif x_direction==1 and y_direction==0 and moment_x==0 and moment_y==0 and moment_z==0 and Remove==0:
                                    
                                    scatter_triangle_x = go.Scatter3d(
                                            x=[x_axis_sup], y=[y_axis_sup],z=[z_axis_sup],
                                            mode='markers',
                                            marker=dict(
                                                    symbol='cross',
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
                                        if 'marker' in trace and 'symbol' in trace['marker'] and trace['marker']['symbol'] == 'cross'and trace['marker']['color']== 'MediumPurple':
                                            scatter_triangle_y_index = i
                                            break

                                    # scatter_triangle'ı kaldırma
                                    if scatter_triangle_y_index is not None:
                                        graph_data_list = list(st.session_state.graph_state_node.data)
                                        graph_data_list.pop(scatter_triangle_y_index)
                                        
                                        st.session_state.graph_state_node.data = graph_data_list

                                    scatter_triangle_x_index = None
                                    for i, trace in enumerate(st.session_state.graph_state_node.data):
                                        if 'marker' in trace and 'symbol' in trace['marker'] and trace['marker']['symbol'] == 'cross':
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
                    st.plotly_chart(st.session_state.graph_state_node, key="unique_key_2")
                    finish= st.button('Finish', on_click=_finish_)
                    if finish:
                        st.success("OK :)")

        with tab_load:
            tab_staload, tab_eqload= st.tabs(
                ["Static load", 'Earthquake Load']
                )
            with tab_staload:
                st.write('Please do not delete the node load even if you do not have a nodal load')
                systemweight=st.checkbox('Include System Self Weight')
                loadtype=['Dead','Live','Wind','Snow','Earhtquake','Other Loads']
                col_part1, col_part2,col_part3 = st.columns(3)
                if option=='2D':


                    with col_part1:
                        df_load_node = st.data_editor(st.session_state.data_load_node,column_config={
                            'Load Node Number': st.column_config.SelectboxColumn(options=st.session_state.data_node['Node Number'].tolist(), required=True),
                            'Load Type(Point)': st.column_config.SelectboxColumn(options=loadtype, required=True)}, num_rows="dynamic")     
                    with col_part2:
                        df_load_element = st.data_editor(st.session_state.data_load_element,column_config={
                            'Load Element Number': st.column_config.SelectboxColumn(options=st.session_state.data_element['Element Number'].tolist(), required=True),
                        'Load Type(Distributed)': st.column_config.SelectboxColumn(options=loadtype, required=True)}
                        , num_rows="dynamic")  

                    def _load_():
                        st.session_state.data_load_element = df_load_element.copy()
                        st.session_state.data_load_node = df_load_node.copy()
                

                    with col_part3:
                        Determine =st.button('Determine',on_click= _load_ )

                        if Determine:
                                
                            fig1=st.session_state.graph_state_node  #drawing the last graph to add loads later. 
                            x_point=[] #Creating the lists of coordinates for point loads
                            y_point=[]
                            u_point=[]#Creating the lists of magnitudes of vectors for point loads
                            v_point=[] 
                            name_point=[]#Creating the lists of names of vectors for point loads
                            for index, row in st.session_state.data_load_node.iterrows():
                                
                                up=float(row['Px'])
                                vp=float(row['Py'])
                                xp=st.session_state.data_node.loc[st.session_state.data_node['Node Number']==float(row['Load Node Number']),'Node x']
                                yp=st.session_state.data_node.loc[st.session_state.data_node['Node Number']==float(row['Load Node Number']),'Node y']
                                n=str((up**2+vp**2)**0.5)  #calculation of vector magnitude
                                name_p=f"{n} kN"


                                x_point.append(xp)
                                y_point.append(yp)
                                u_point.append(up)
                                v_point.append(vp)
                                name_point.append(name_p)
                            for i in name_point:
                                fig2 = ff.create_quiver(x_point, y_point, u_point, v_point,line_color='red',scale=0.05,name=i) #creating vectors
                            
                                fig1.add_traces(data = fig2.data) #adding vectors the last graph
                            
                        
                            #To create vectors for uniform loading,it was preffered to merge element and uniform load table
                            df_all=pd.merge(st.session_state.data_load_element,st.session_state.data_element,left_on='Load Element Number',right_on='Element Number')
                            df_all['Load Element Number'] = df_all['Element Number']
                            df_all = df_all.drop(columns=['Element Number'])
                            print(df_all)
                            #df_all.drop(['Section'],axis=1,inplace=True)
                            
                            df_all['First_x_node'] = df_all['First Node Number'].map(st.session_state.data_node.set_index('Node Number')['Node x']) #adding x and y coordinate information of df_All dataframe
                            df_all['Second_x_node'] = df_all['Second Node Number'].map(st.session_state.data_node.set_index('Node Number')['Node x'])
                            df_all['First_y_node'] = df_all['First Node Number'].map(st.session_state.data_node.set_index('Node Number')['Node y'])
                            df_all['Second_y_node'] = df_all['Second Node Number'].map(st.session_state.data_node.set_index('Node Number')['Node y'])
                        
                            #Creating the lists of coordinates and vector magntiudes and their names
                            st.dataframe(df_all)            
                            u_element=[]
                            v_element=[]
                            x_element=[]
                            y_element=[]
                            uniform_name=[]
                            for index,row in df_all.iterrows():
                                a=float(row['First_x_node'])-float(row['Second_x_node'])
                                b=float(row['First_y_node'])-float(row['Second_y_node'])
                                element_length=(a**2 + b**2)**0.5
                                x_e=np.arange(float(row['First_x_node']),float(row['Second_x_node']),float(element_length/10))
                                y_e=np.arange(float(row['First_y_node']),float(row['Second_y_node']),float(element_length/10))
                                u_e=float(row['Wx'])
                                v_e=float(row['Wy'])
                                q=str(((u_e)**2+(v_e)**2)**0.5)
                                name_q=f"{q} kN/m"
                                uniform_name.append(name_q)
                                
                                if len(x_e)>0 and len(y_e)==0:
                                    x_element.append(x_e)
                                    y_element.append(np.full(len(x_e),float(row['First_y_node'])))
                                    u_element.append(np.full(len(x_e),u_e))
                                    v_element.append(np.full(len(x_e),v_e))
                                    
                                    
                                elif len(y_e)>0 and len(x_e)==0:
                                    y_element.append(y_e)
                                    x_element.append(np.full(len(y_e),float(row['First_x_node'])))
                                    u_element.append(np.full(len(y_e),u_e))
                                    v_element.append(np.full(len(y_e),v_e))
                                else:
                                    x_element.append(x_e)
                                    y_element.append(y_e)

                                    u_element.append(np.full(len(x_e),u_e))
                                    v_element.append(np.full(len(y_e),v_e))
                            #Creating the vectors for uniform loading
                            for i in uniform_name:

                                fig3 = ff.create_quiver(x_element, y_element, u_element, v_element,line_color='blue',scale=0.05,name=i)
                                fig1.add_traces(data = fig3.data)  #adding the last graph
                            
                            fig1.update_yaxes(range=[-1, 10]) #boundaries are set for graph because the graph makes autoscaling
                            fig1.update_xaxes(range=[-1, 20])
                            st.plotly_chart(fig1, key="unique11")
                            st.success("Ok:)")
                    _load_()
                    ##########INCLUDING SYSTEM WEIGHT#############3 
                    wx_dead_loads=[]
                    columnloads=[]
                    beamloads=[]
                    
                    element_df=df_load_element.copy() # dead loads are not shown on load graph so element_df and node_df is created to not change any dataframe that helps to draw load graph
                    node_df=df_load_node.copy()
                    if systemweight:
                        for index, row in st.session_state.df_element_length.iterrows():
                            if row['First_y_node']==row['Second_y_node']:
                                deadload={
                                        'Load Element Number':row['Element Number'],
                                        'Wx':0,
                                        'Wy':-float(row['Weight (kN)'])/float(row['Element Length (m)']),
                                        'Load Type(Distributed)':'Dead'
                                        }
                                beamloads.append(deadload)
                            
                            if row['First_y_node']==row['Second_y_node']:
                        
                                deadload={
                                            'Load Element Number':row['Element Number'],
                                            'Wx':0,
                                            'Wy':-float(row['Weight (kN)'])/float(row['Element Length (m)']),
                                            'Load Type(Distributed)':'Dead'
                                            }
                                wx_dead_loads.append(deadload)

                            if row['First_x_node']==row['Second_x_node']:
                        
                                deadload={
                                        'Load Element Number':row['Element Number'],
                                        'Wx':float(row['Weight (kN)'])/float(row['Element Length (m)']),
                                        'Wy':0,
                                        'Load Type(Distributed)':'Dead'
                                        }
                                wx_dead_loads.append(deadload)
                        node_all_loads= node_df.copy()
                        ele_all_loads=pd.concat([element_df,pd.DataFrame(beamloads)],ignore_index=True)       
                        element_all_loads=pd.concat([element_df,pd.DataFrame(wx_dead_loads)],ignore_index=True)
                        st.dataframe(node_all_loads)
                        st.dataframe(ele_all_loads)
                        st.dataframe(element_all_loads)


                else:
                    with col_part1:
                        df_load_node_3d = st.data_editor(st.session_state.data_load_node_3d,column_config={
                            'Node Number': st.column_config.SelectboxColumn(options=st.session_state.data_node_3d['Node Number'].tolist(), required=True),
                            'Load Type': st.column_config.SelectboxColumn(options=loadtype, required=True)}, num_rows="dynamic")     
                    with col_part2:
                        df_load_element_3d = st.data_editor(st.session_state.data_load_element_3d,column_config={
                            'Element Number': st.column_config.SelectboxColumn(options=st.session_state.data_element['Element Number'].tolist(), required=True),
                        'Load Type': st.column_config.SelectboxColumn(options=loadtype, required=True)}
                        , num_rows="dynamic")  

                    def _load_():
                        st.session_state.data_load_element_3d = df_load_element_3d.copy()
                        st.session_state.data_load_node_3d = df_load_node_3d.copy()
                    
                    with col_part3:
                        Determine =st.button('Determine',on_click= _load_ ,key=18)
                        _load_()
                        
                            
                    ##########INCLUDING SYSTEM WEIGHT#############
                    #z ekseninin gravity yonunde oldugunu dusunursek,z ekseni boyunca degısen elemanlar kolonlar ve x y boyunca degısenler beamler(Wy her zaman)
                    wx_dead_loads=[]
                
                    element_df_3d=df_load_element_3d.copy() # dead loads are not shown on load graph so element_df and node_df is created to not change any dataframe that helps to draw load graph
                    node_all_loads_3d=df_load_node_3d.copy()
                    if systemweight:
                        for index, row in st.session_state.df_element_length.iterrows():
                            if row['First_y_node']==row['Second_y_node'] and row['First_z_node']==row['Second_z_node']:
                                deadload={
                                        'Element Number':row['Element Number'],
                                        'Wx':0,
                                        'Wy':0,
                                        'Wz':-float(row['Weight (kN)'])/float(row['Element Length (m)']),
                                        'Load Type':'Dead'
                                        }
                                wx_dead_loads.append(deadload)

                            if row['First_y_node']==row['Second_y_node'] and row['First_x_node']==row['Second_x_node']:
                                deadload={
                                        'Element Number':row['Element Number'],
                                        'Wx':-float(row['Weight (kN)'])/float(row['Element Length (m)']),
                                        'Wy':0,
                                        'Wz':0,
                                        'Load Type':'Dead'
                                        }
                                wx_dead_loads.append(deadload)    

                            if row['First_x_node']==row['Second_x_node'] and row['First_z_node']==row['Second_z_node']:
                                deadload={
                                        'Element Number':row['Element Number'],
                                        'Wx':0,
                                        'Wy':0,
                                        'Wz':-float(row['Weight (kN)'])/float(row['Element Length (m)']),
                                        'Load Type':'Dead'
                                        }
                                wx_dead_loads.append(deadload)
                    
                        
                        element_all_loads_3d=pd.concat([element_df_3d,pd.DataFrame(wx_dead_loads)],ignore_index=True)
                        
                        st.dataframe(element_all_loads_3d)
                        st.dataframe(node_all_loads_3d)


                        if Determine:
                                
                           #fig1=st.session_state.graph_state_node  #drawing the last graph to add loads later. 
                            
                          #x_point=[] #Creating the lists of coordinates for point loads
                          # y_point=[]
                          # z_point=[]
                          # u_point=[]#Creating the lists of magnitudes of vectors for point loads
                          # v_point=[]
                          # w_point=[] 
                          # name_point=[]#Creating the lists of names of vectors for point loads
                          # for index, row in st.session_state.data_load_node_3d.iterrows():
                                
                               #up=float(row['Px'])
                               #vp=float(row['Py'])
                               #wp=float(row['Pz'])
                               #xp=st.session_state.data_node_3d.loc[st.session_state.data_node_3d['Node Number']==float(row['Node Number']),'Node x']
                               #yp=st.session_state.data_node_3d.loc[st.session_state.data_node_3d['Node Number']==float(row['Node Number']),'Node y']
                               #zp=yp=st.session_state.data_node_3d.loc[st.session_state.data_node_3d['Node Number']==float(row['Node Number']),'Node z']
                               #n=str((up**2+vp**2+wp**2)**0.5)  #calculation of vector magnitude
                               #name_p=f"{n} kN"


                               #x_point.append(xp)
                               #y_point.append(yp)
                               #z_point.append(zp)
                               #u_point.append(up)
                               #v_point.append(vp)
                               #w_point.append(wp)
                                

                               #name_point.append(name_p)

                           #for i in name_point:
                                #fig2 = go.cone(x_point, y_point,z_point, u_point, v_point,w_point,line_color='red',scale=0.05,name=i) #creating vectors
                               #st.write(name_point,x_point,y_point,z_point,u_point,v_point,w_point)
                               #fig1.add_trace(go.Cone(x=[x_point], y=[y_point],z=[z_point],u=[u_point], v=[v_point],w=[w_point], colorscale='Reds',sizemode="absolute",sizeref=100000,anchor='tip')) #adding vectors the last graph
                            
                        
                            #To create vectors for uniform loading,it was preffered to merge element and uniform load table
                           df_all=pd.merge(st.session_state.data_load_element_3d,st.session_state.data_element,on='Element Number')
                           df_all.drop(['Section'],axis=1,inplace=True)
                           df_all['First_x_node'] = df_all['First Node Number'].map(st.session_state.data_node_3d.set_index('Node Number')['Node x']) #adding x and y coordinate information of df_All dataframe
                           df_all['Second_x_node'] = df_all['Second Node Number'].map(st.session_state.data_node_3d.set_index('Node Number')['Node x'])
                           df_all['First_y_node'] = df_all['First Node Number'].map(st.session_state.data_node_3d.set_index('Node Number')['Node y'])
                           df_all['Second_y_node'] = df_all['Second Node Number'].map(st.session_state.data_node_3d.set_index('Node Number')['Node y'])
                           df_all['First_z_node'] = df_all['First Node Number'].map(st.session_state.data_node_3d.set_index('Node Number')['Node z']) #adding x and y coordinate information of df_All dataframe
                           df_all['Second_z_node'] = df_all['Second Node Number'].map(st.session_state.data_node_3d.set_index('Node Number')['Node z'])
                        
                            #Creating the lists of coordinates and vector magntiudes and their names
                           st.dataframe(df_all)            
                           #u_element=[]
                           #v_element=[]
                           #w_element=[]
                          # x_element=[]
                           #y_element=[]
                          # z_element=[]
                           #uniform_name=[]
                           #for index,row in df_all.iterrows():
                               #a=float(row['First_x_node'])-float(row['Second_x_node'])
                              # b=float(row['First_y_node'])-float(row['Second_y_node'])
                               #c=float(row['First_z_node'])-float(row['Second_z_node'])
                              # element_length=(a**2 + b**2+c*2)**0.5
                               #x_e=np.arange(float(row['First_x_node']),float(row['Second_x_node']),float(element_length/10))
                               #y_e=np.arange(float(row['First_y_node']),float(row['Second_y_node']),float(element_length/10))
                               #z_e=np.arange(float(row['First_z_node']),float(row['Second_z_node']),float(element_length/10))
                               #u_e=float(row['Wx'])
                               #v_e=float(row['Wy'])
                               #w_e=float(row['Wz'])
                               #q=str(((u_e)**2+(v_e)**2+(w_e)**2)**0.5)
                               #name_q=f"{q} kN/m"
                               #uniform_name.append(name_q)
                                
                               #if len(x_e)>0 and len(y_e)==0 and len(z_e)==0:
                                   #x_element.append(x_e)
                                   #y_element.append(np.full(len(x_e),float(row['First_y_node'])))
                                   #z_element.append(np.full(len(x_e),float(row['First_z_node'])))
                                   #u_element.append(np.full(len(x_e),u_e))
                                   #v_element.append(np.full(len(x_e),v_e))
                                   #w_element.append(np.full(len(x_e),w_e))
                                    
                                    
                               #elif len(y_e)>0 and len(x_e)==0 and len(z_e)==0:
                                   #y_element.append(y_e)
                                   #x_element.append(np.full(len(y_e),float(row['First_x_node'])))
                                   #z_element.append(np.full(len(y_e),float(row['First_z_node'])))
                                   #u_element.append(np.full(len(y_e),u_e))
                                   #v_element.append(np.full(len(y_e),v_e))
                                   #w_element.append(np.full(len(y_e),w_e))


                               #else:
                                   #x_element.append(x_e)
                                   #y_element.append(y_e)
                                   #z_element.append(z_e)
                                   #u_element.append(np.full(len(x_e),u_e))
                                   #v_element.append(np.full(len(y_e),v_e))
                                   #w_element.append(np.full(len(z_e),w_e))
                                

                            #Creating the vectors for uniform loading
                           #for i in uniform_name:
                                #fig1.add_trace(go.Cone(x=x_point, y=y_point,z=z_point,u=u_point, v=v_point,w=w_point, colorscale='Reds',sizemode="scaled",sizeref=0.1,name='vectors'))
                                #st.write(uniform_name,x_point,y_point,z_point,u_element,v_element,w_element)
                                

                                #fig3 = ff.create_quiver(x_element, y_element, z_element, u_element, v_element,w_element,line_color='blue',scale=0.05,name=i)
                               #fig1.add_trace(go.Cone(x=[x_point], y=[y_point],z=[z_point],u=u_element, v=v_element,w=w_element, colorscale='Reds',sizemode="absolute",sizeref=100000,anchor='tip')) #adding the last graph
                            
                            #fig1.update_yaxes(range=[-1, 10]) #boundaries are set for graph because the graph makes autoscaling
                            #fig1.update_xaxes(range=[-1, 20])
                           #fig1.update_layout(scene=dict(domain_x=[0, 1],
                   #camera_eye=dict(x=-1.57, y=1.36, z=0.58)))

                           #st.plotly_chart(fig1)
                           #st.success("Ok :)")
                        


        with tab_eqload:
            if option=='2D': 
                st.write('Please mark only one of the buttons :)')
                eqload=st.checkbox('Do you want adding EQ Load to Building?')
                noeqload= st.checkbox('If not you can continue with load combination part')   
                    
                if eqload:
                        tab_period, tab_resspect, tab_eload, tab_totalload = st.tabs(
                        ["Period", 'Response Specktrum',"Equivalent EQ Load","Total Load"]
                        )
                        with tab_period:
                            cool1,cool2,cool3 = st.columns(3)
                            

                            with cool1:
                                
                                def calc_period ():
                                    numFloor=storynumber
                                    numBay=baynumber
                                    bayWidth=beamlength[0:baynumber:1]
                                    bayWidth = [i for i in bayWidth for _ in range(2)]
                                    storyHeights=list((reversed(columnlength[0::baynumber])))
                                    print(columnlength)
                                    print(storyHeights,'storyhe')

                                    #mass for each element
                                    listofbeamweights=[]
                                    listofcolumnweights=[]
                                    
                                    st.session_state.df_element_length=st.session_state.df_element_length.sort_values(by=['Story Level'],ascending=False) #sorting from the top story to bottom story
                                   #st.dataframe(st.session_state.df_element_length)
                                    for index, row in st.session_state.df_element_length.iterrows():
                                        if row['First_y_node']==row['Second_y_node']:
                                            listofbeamweights.append((row['Weight (kN)'])/9.81)
                                        if row['First_x_node']==row['Second_x_node']:
                                            listofcolumnweights.append((row['Weight (kN)'])/(9.81*2))  #ton

                                    print(listofbeamweights,'beamweights')
                                    print(listofcolumnweights,'columnweights')# from top to bpottom
                                    col=[]# finding column masses for each story(lumped mass)
                                    for i in range(0,len(listofcolumnweights),numBay+1):
                                        sumcol=sum(listofcolumnweights[i:i+numBay+1])
                                        col.append(sumcol)   
                                    massxcolumn=[]
                                    for i in range(0,len(col)-1):
                                        weight_1=col[i]+col[i+1]
                                        massxcolumn.append(weight_1)
                                    massxcolumn.insert(0,col[0])
                                    

                                    #finding beam masses for each story(lumped mass)
                                    massxbeam=[]
                                    for i in range(0,len(listofbeamweights),numBay):
                                        sumbeam=sum(listofbeamweights[i:i+numBay])
                                        massxbeam.append(sumbeam)
                                    #summing beams and column masses for each lumped mass
                                    massxstory=[sum(i) for i in zip(massxbeam, massxcolumn)]
                                    massxstory=massxstory[::-1] #sorting from bottom story to top story
                                    print(massxstory,"story agırlık")
                                    print(massxbeam,'massxbeam')
                                    print(massxcolumn,'massxcolumn')
                                    
                                    ops.wipe()
                                    ops.model('Basic', '-ndm', 2)

                                    E = 25000000
                                    
                                    coordTransf = "Linear"  # Linear, PDelta, Corotational
                                

                                
                                    #column sections for each column 
                                    
                                    columntable=st.session_state.df_element_length
                                    columntable=columntable.sort_values(by='First_x_node')
                                    columntable = columntable[columntable['First_x_node'] == columntable['Second_x_node']]

                                    columntable['A']=columntable['Section'].map( st.session_state.data_section.set_index('Section Name')['Area(m^2)'])
                                    columntable['I']=columntable['Section'].map( st.session_state.data_section.set_index('Section Name')['I(2-2)(m^4)'])
                                    columnsections=[]
                                    
                                    for i in range(0,len(columntable),storynumber):
                                        columntable2=columntable.iloc[i:i+storynumber]
                                        columntable2=columntable2.sort_values(by='First_y_node')
                                        columnsections+=columntable2['Section'].tolist()
                                    columnsections = [columnsections[i:i+storynumber] for i in range(0, len(columnsections), storynumber)]
                                
                                    #beam sections for each story
                                    beamtable=st.session_state.df_element_length.sort_values(by='First_y_node')
                                    beamtable = beamtable[beamtable['First_y_node'] == beamtable['Second_y_node']]
                                    beamtable['A']=beamtable['Section'].map( st.session_state.data_section.set_index('Section Name')['Area(m^2)'])
                                    beamtable['I']=beamtable['Section'].map( st.session_state.data_section.set_index('Section Name')['I(3-3)(m^4)'])
                                    beamsections=[]
                                    for i in range(0,len(beamtable)):
                                        beamtable2=beamtable.iloc[i:i+numBay]
                                        beamtable2=beamtable2.sort_values(by='First_x_node')
                                        beamsections.extend(beamtable2['Section'].tolist())
                                    print(beamsections,"kiriş enkesit")

                                    section_all={}
                                    for index,row in columntable.iterrows():
                                        key=row['Section']
                                        A=row['A']
                                        I=row['I']
                                        if key not in section_all:
                                            section_all[key]=[A,I]
                                    for index,row in beamtable.iterrows():
                                        key=row['Section']
                                        A=row['A']
                                        I=row['I']
                                        if key not in section_all:
                                            section_all[key]=[A,I]
                                    

                                    # procedure to read
                                    def ElasticBeamColumn(eleTag, iNode, jNode, sectType, E, transfTag, M, massType):
                                        found = 0

                                        prop = section_all[sectType]
                                        A = prop[0]
                                        I = prop[1]
                                        ops.element('elasticBeamColumn', eleTag, iNode, jNode, A, E, I, transfTag, '-mass', M, massType)

                                    print ("nerede duruyor")

                                    # add the nodes
                                    #  - floor at a time
                                    yLoc = 0.
                                    nodeTag = 1
                                    for j in range(0, numFloor + 1):   #  NODE OLUŞTURMA

                                        xLoc = 0.
                                        for i in range(0, numBay + 1):
                                            ops.node(nodeTag, xLoc, yLoc)
                                            if yLoc==0:
                                                ops.fix(nodeTag,1,1,1)

                                            xLoc += bayWidth[i]
                                            nodeTag += 1

                                        if j < numFloor:
                                            storyHeight = storyHeights[j]

                                        yLoc += storyHeight
                                    
                                
                                    # fix first floor

                                    #for index,row in st.session_state.data_node[st.session_state.data_node['Node y']==0].iterrows():
                                        #   ops.fix(int(row['Node Number']),1,1,1)
                                    

                                    # rigid floor constraint & masses

                                    nodeTagR = baynumber+3
                                    nodeTag = baynumber+2
                                    a_j=0
                                    mass_index=0
                                    
                                    for j in range(1, numFloor + 1):
                                        for i in range(0, numBay + 1):

                                            if nodeTag != nodeTagR:
                                                ops.equalDOF(nodeTagR, nodeTag, 1)
                                                print(nodeTagR, nodeTag, 1)
                                            else:
                                                                        # `mass_index`'i kullanarak doğru değeri alıyoruz ve artırıyoruz
                                                if mass_index < len(massxstory):  # index sınırını kontrol edelim
                                                    a_j = massxstory[mass_index]
                                                    ops.mass(nodeTagR, a_j, 1.0e-10, 1.0e-10)
                                                    print(nodeTagR, a_j, 1.0e-10, 1.0e-10)
                                                    mass_index += 1  # index artırılıyor

                                            nodeTag += 1

                                        nodeTagR += numBay + 1
                                    
                                    M = 0.
                                    massType = "-lMass"

                                    # add the columns
                                    # add column element
                                    ops.geomTransf(coordTransf, 1)

                                    eleTag = 1

                                    
                                    for j in range(0,numBay + 1):

                                        end1 = j + 1
                                        end2 = end1 + numBay + 1

                                        thisColumn = columnsections[j]

                                        for i in range(0, numFloor):
                                            secType = thisColumn[i]
                                            ElasticBeamColumn(eleTag, end1, end2, secType, E, 1, M, massType)
                                            end1 = end2
                                            end2 += numBay + 1
                                            eleTag += 1

                                    # add beam elements
                                    for j in range(1, numFloor + 1):
                                        end1 = (numBay + 1) * j + 1
                                        end2 = end1 + 1
                                        
                                        for i in range(0, numBay):
                                            secType = beamsections[i]
                                            ElasticBeamColumn(eleTag, end1, end2, secType, E, 1, M, massType)
                                            end1 = end2
                                            end2 = end1 + 1
                                            eleTag += 1
                                

                                    
                                    # calculate eigenvalues & print results
                                    numEigen = len(storyHeights)+1
                                    eigenValues = ops.eigen('-fullGenLapack',numEigen)
                                    print(numEigen, "eigen number")
                                    print(eigenValues,"değerleri")
                                    PI = 2 * asin(1.0)
                                    ops.timeSeries('Linear', 1)
                                    ops.pattern('Plain', 1, 1)
                                    ops.integrator('LoadControl', 1.0)
                                    ops.algorithm('Linear')
                                    ops.analysis('Static')
                                    ops.analyze(1)
                                    periodlist=[]
                                    for i in range(0,numEigen):
                                        period=2*PI/sqrt(eigenValues[i])
                                        periodlist.append(period)
                                    
                                    opsv.plot_model()
                                    
                                   
                                            
                                        
                                    modenumbers=list(range(1, numEigen+1))
                                    df_period=pd.DataFrame({
                                                'Mode Number':modenumbers,
                                                'Period':periodlist
                                            })
                                   #st.session_state.data_period=st.data_editor(df_period,num_rows='dynamic')

                                           

                                    
                                    total_mass = sum(massxstory)

                                    with cool1:
                                            st.write(df_period)
                                            st.write(f"Structure Period: {periodlist[0]:.2f} sec")
                                        
                                            #st.session_state.data_period=st.data_editor(df_period,num_rows='dynamic')
                                            st.session_state.periodlist = periodlist
                                            st.session_state.massxstory = massxstory
                                            st.session_state.total_mass = total_mass
                                            st.session_state.beamtable = beamtable
                                            st.session_state.columntable2 = columntable2

                                show_button = st.button("Shows", on_click=calc_period)                           
                        with tab_resspect:
                            A,B,C = st.columns(3)
                            with A:
                                SDS = st.number_input ("Design Spectral Acceleration of structure for short period 'Sds':")
                                SD1 = st.number_input ("Design Spectral Acceleration of structure for 1 sec period 'Sd1':")
                                R = st.number_input ("Reduction Factor 'R':")
                                I = st.number_input ("Building Importance Coefficient 'I':")
                                D = st.number_input ("Excess Strength 'D':")
                                num_points = int(6/0.01)+1                          
                                T = np.linspace(0.0 ,6.0, num=num_points)
                                def spectrum(T, SDS, SD1):
                                    
                                    TA = 0.2 * SD1 / SDS
                                    TB = SD1 / SDS
                                    TL = 6.0

                                    Sae = np.zeros_like(T)
                                    for i in range(len(T)):
                                        if T[i] <= TA:
                                            Sae[i] = (0.4 + 0.6 * T[i] / TA) * SDS
                                        elif TA <T[i]<= TB :
                                            Sae[i] = SDS
                                        elif TB < T[i]<= TL :
                                            Sae[i] = SD1/T[i]
                                        else:
                                            Sae[i]=0    

                                    return Sae

                                def red_fac(T,R,I,D):
                                    TA = 0.2 * SD1 / SDS
                                    TB = SD1 / SDS
                                    TL = 6.0
                                    Ra = np.zeros_like(T)
                                    for i in range(len(T)):
                                        if T[i]> TB:
                                            Ra[i] = R/I
                                        elif T[i]<= TB:
                                            Ra[i] = D+ ((R/I)-D )*(T[i]/TB)
                                        else:
                                            Ra[i] = 0
                                    return Ra
                                def res_spect ():
                                    TA = 0.2 * SD1 / SDS
                                    TB = SD1 / SDS
                                    TL = 6.0
                                    Sae = spectrum(T, SDS, SD1)
                                    Ra = red_fac(T,R,I,D)
                                    SaR = (Sae/Ra)
                                    with B:
                                        spect , ay = plt.subplots()
                                        ay.plot(T, Sae, label="EQ DESIGN SPECTRUM")
                                        ay.set_xlabel('Period (T)')
                                        ay.set_ylabel('Horizontal Elastic Design Spectral Acceleration (Sae)')
                                        ay.set_title('Horizontal Elastic Design Spectrum')
                                        ay.grid(True)
                                        ay.legend()
                                        st.pyplot(spect)
                                    
                                    with C:
                                        rspect , az = plt.subplots()
                                        az.plot(T, SaR, label="EQ REDUCTION SPECTRUM")
                                        az.set_xlabel('Period (T)')
                                        az.set_ylabel('Horizontal Reduced Design Spectral Acceleration (Sae)')
                                        az.set_title('Horizontal Reduced Design Spectrum')
                                        az.grid(True)
                                        az.legend()
                                        st.pyplot(rspect)
                            plotted_button= st.button("Plot", on_click = res_spect)
                        with tab_eload:
                            coll1,coll2 = st.columns(2)
                            with coll1:
                                def eell():


                                    Sae = spectrum(T, SDS, SD1)
                                    Ra = red_fac(T,R,I,D)
                                    SaR = (Sae/Ra)
                                    index = np.argmin(np.abs(T-st.session_state.periodlist[0]))
                                    SaR_Tpx = SaR[index]

                                    Vte_X= SaR_Tpx*st.session_state.total_mass*9.81
                                
                                    with coll1:
                                        st.write(f"Tp(X): {st.session_state.periodlist[0]:.2f} sec")
                                        st.write(f"Toplam Ağırlık: {st.session_state.total_mass:.2f} ton")
                                        st.write(f"SaR (Tp(X)): {SaR_Tpx:.2f} ")
                                        st.write(f"Vte(X): {Vte_X:.2f} kN")
                                        st.session_state.Vte = Vte_X
                                        #st.write(st.session_state.massxstory)
                                call_button = st.button("Call" , on_click= eell)

                            with coll2:
                                def eell2():
                                    df_columntable2 = pd.DataFrame(st.session_state.columntable2)

                                    storynumbers = df_columntable2.sort_values(by='Story Level', ascending=True)

                                    storynumbers['Cumulative Story Height'] = storynumbers['Element Length (m)'].cumsum()

                                    storynumbers = storynumbers.sort_values(by='Story Level', ascending=False)

                                    df_weights = pd.DataFrame({'Weight': st.session_state.massxstory})

                                    df_weights['Story Level'] = storynumbers['Story Level'].values

                                    df_combined = pd.merge(storynumbers, df_weights, on='Story Level', how='left')

                                    df_EEL = df_combined[['Story Level', 'Cumulative Story Height', 'Weight']]
                                    
                                    st.session_state.df_EEL = df_EEL 
                                eel_varies = st.button("Calculate" , on_click= eell2)    

                                def calculate_moment(mass,height):
                                    
                                        return mass * height

                                def dist_mass (mass_i):
                                        totalmass = st.session_state.df_EEL['miHi'].sum()
                                        
                                        return mass_i / totalmass
                                        
                                def calc_F(ratemass):
                                        F1 = st.session_state.Vte
                                        storylev = st.session_state.df_EEL['Story Level'][0]
                                        F2 = 0.0075*storylev*F1
                                        return ratemass*(F1-F2)
                                    
                                    
                                def calc_button():
                                    st.session_state.df_EEL['miHi'] = st.session_state.df_EEL.apply(lambda row: calculate_moment(row['Weight'], row['Cumulative Story Height']), axis=1)
                                    st.session_state.df_EEL['Dist Mass'] = st.session_state.df_EEL.apply(lambda row: dist_mass(row['miHi']), axis=1)
                                    st.session_state.df_EEL['Ffi (kN)'] = st.session_state.df_EEL.apply(lambda row: calc_F(row['Dist Mass']), axis=1)
                                        
                                        
                                    
                                    st.session_state.df_EEL_new = st.session_state.df_EEL.copy()
                                    with coll2:

                                        st.write(st.session_state.df_EEL_new)
                                        #st.write(st.session_state.beamtable)
                                        
                                        df_EEL_new_sorted = st.session_state.df_EEL_new.sort_values(by="Story Level", ascending=False)

                                        
                                        beamtable_sorted = st.session_state.beamtable.sort_values(by="Story Level", ascending=True)

                                    
                                        merged_df = pd.merge(df_EEL_new_sorted, beamtable_sorted, on="Story Level", how="inner")

                                    
                                        st.session_state["merged_df"] = merged_df  
                                        #st.write(merged_df)
                                        
                                        selected_columns_df = merged_df[["First Node Number", "Ffi (kN)"]]

                                        
                                        st.session_state.selected_columns = selected_columns_df
                                        #st.write(st.session_state.selected_columns)
                                calculation_buttons = st.button('Show Tables', on_click=calc_button)

                        with tab_totalload:
                            colll1,colll2 = st.columns(2)
                            with colll1:
                                eload=st.checkbox('Add EQ Load')
                                def shows():
                                    
                                    new_rows = pd.DataFrame({
                                                    "Load Node Number": st.session_state.selected_columns["First Node Number"],  # First Node Number --> Load Node Number
                                                    "Px": st.session_state.selected_columns["Ffi (kN)"],  # Ffi(kN) --> Px
                                                    "Py": 0,  # Py değeri 0
                                                    "Mz": 0,  # Mz değeri 0SS
                                                    "Load Type(Point)": "Earthquake"  # Load Type(Point) --> Earthquake
                                                    })  
                                                
                                    updated_node_all_loads = pd.concat([node_all_loads, new_rows], ignore_index=True)
                                    
                                    if eload:
                                        with colll2:
                                            st.session_state.updated_node_all_loads = updated_node_all_loads
                                            st.write(st.session_state.updated_node_all_loads)
                                    else:
                                        with colll2:
                                            st.session_state.updated_node_all_loads = node_all_loads
                                            st.write(st.session_state.updated_node_all_loads)
                                showss_button = st.button('Show', on_click=shows)
                if noeqload:
                        
                        st.session_state.updated_node_all_loads = pd.DataFrame({
                                                    "Load Node Number": node_all_loads["Load Node Number"],  
                                                    "Px": node_all_loads["Px"], 
                                                    "Py": node_all_loads["Py"], 
                                                    "Mz": node_all_loads["Mz"],  
                                                    "Load Type(Point)":node_all_loads["Load Type(Point)"]  
                                                    })  
                        #st.write(st.session_state.updated_node_all_loads)
            else:
                st.write('Currently out of service :(')

        with tab_loadcomb:
            _load_()
                
            df_load_combination = st.data_editor(st.session_state.data_load_combination, num_rows="dynamic")
            col_part1, col_part2, col_part3 = st.columns(3)
            if option=='2D':
                with col_part1:

                    def _finished_():

                        load_types = ['Dead', 'Live', 'Wind', 'Snow', 'Earthquake']
                        combination_factors = {}
                        print('pass')

                        for index, row in df_load_combination.iterrows():
                            combination_name = row['Combination']
                            factors = {load_type: row[load_type] for load_type in load_types}
                            combination_factors[combination_name] = factors
                        print('pass2')

                    
                        if 'Combination' not in element_all_loads.columns:
                            element_all_loads['Combination'] = combination_name
                        print('pass3')

                        element_wxy_dict = {}

                        for element_number, group_element in element_all_loads.groupby('Load Element Number'):
                            element_combinations = {}
                            for _, group_combination in df_load_combination.iterrows():
                                combination_name = group_combination['Combination']
                                loadtype_wxy = {}
                                for load_type in load_types:
                                    loadtype_wxy[load_type] = {
                                        'Wx': group_element[group_element['Load Type(Distributed)'] == load_type]['Wx'].tolist(),
                                        'Wy': group_element[group_element['Load Type(Distributed)'] == load_type]['Wy'].tolist()
                                        

                                    }
                                element_combinations[combination_name] = loadtype_wxy
                            element_wxy_dict[element_number] = element_combinations

                        total_loads = []
                        total_loads_df = pd.DataFrame(columns=['Element Number', 'Combination', 'Total Wx', 'Total Wy','Total Wz'])

                        for element_number, combinations in element_wxy_dict.items():
                            for combination_name, loadtypes in combinations.items():
                                total_wx = 0.0
                                total_wy = 0.0
                                #total_wz = 0.0
                                for load_type in load_types:
                                    for wx in loadtypes[load_type]['Wx']:
                                        factor_value = combination_factors.get(combination_name, {}).get(load_type, 1.0)
                                        total_wx += wx * factor_value
                                    for wy in loadtypes[load_type]['Wy']:
                                        factor_value = combination_factors.get(combination_name, {}).get(load_type, 1.0)
                                        total_wy += wy * factor_value
                                    #for wz in loadtypes[load_type]['Total Wz']:
                                        #factor_value = combination_factors.get(combination_name, {}).get(load_type, 1.0)
                                        #total_wz += wz * factor_value    

                                total_loads.append({'Element Number': element_number, 'Combination': combination_name, 'Total Wx': total_wx, 'Total Wy': total_wy})

                        total_loads_element_df = pd.DataFrame(total_loads)
                        st.session_state.total_loads_df = total_loads_element_df
                        st.session_state.combinations = total_loads_df['Combination'].unique().tolist()
                        
                    def _finished2_():
                        

                        load_types = ['Dead', 'Live', 'Wind', 'Snow', 'Earthquake']
                        combination_factors = {}
                        print('pass')

                        for index, row in df_load_combination.iterrows():
                                combination_name = row['Combination']
                                factors = {load_type: row[load_type] for load_type in load_types}
                                combination_factors[combination_name] = factors
                        print('pass2')

                        
                        if 'Combination' not in st.session_state.updated_node_all_loads.columns:
                            st.session_state.updated_node_all_loads['Combination'] = combination_name
                        print('pass3')

                        element_wxy_dict = {}

                        for element_number, group_element in st.session_state.updated_node_all_loads.groupby('Load Node Number'):
                            element_combinations = {}
                            for _, group_combination in df_load_combination.iterrows():
                                combination_name = group_combination['Combination']
                                loadtype_wxy = {}
                                for load_type in load_types:
                                    loadtype_wxy[load_type] = {
                                        'Px': group_element[group_element['Load Type(Point)'] == load_type]['Px'].tolist(),
                                        'Py': group_element[group_element['Load Type(Point)'] == load_type]['Py'].tolist()
                                            

                                        }
                                element_combinations[combination_name] = loadtype_wxy
                            element_wxy_dict[element_number] = element_combinations

                        total_node_loads = []
                        total_node_load_df = pd.DataFrame(columns=['Node Number', 'Combination', 'Total Px', 'Total Py','Mz'])

                        for element_number, combinations in element_wxy_dict.items():
                            for combination_name, loadtypes in combinations.items():
                                total_wx = 0.0
                                total_wy = 0.0
                                #total_wz = 0.0
                                for load_type in load_types:
                                    for wx in loadtypes[load_type]['Px']:
                                        factor_value = combination_factors.get(combination_name, {}).get(load_type, 1.0)
                                        total_wx += wx * factor_value
                                    for wy in loadtypes[load_type]['Py']:
                                        factor_value = combination_factors.get(combination_name, {}).get(load_type, 1.0)
                                        total_wy += wy * factor_value
                                        #for wz in loadtypes[load_type]['Total Wz']:
                                            #factor_value = combination_factors.get(combination_name, {}).get(load_type, 1.0)
                                            #total_wz += wz * factor_value    

                                total_node_loads.append({'Node Number': element_number, 'Combination': combination_name, 'Total Px': total_wx, 'Total Py': total_wy, 'Mz':0})

                        total_node_load_df = pd.DataFrame(total_node_loads)
                        

                        st.session_state.total_node_df = total_node_load_df
                        
                    
                    def _allfinished_():
                        _finished_()
                        _finished2_()
                    finished_button = st.button("finished", on_click= _allfinished_)    
                    
                    if 'total_loads_df' in st.session_state:
                        st.session_state.combinations = st.session_state.total_loads_df['Combination'].unique().tolist()
                        with col_part2:
                            
                            st.dataframe(st.session_state.total_loads_df)
                            st.dataframe(st.session_state.total_node_df)
                            

                        with col_part3:
                
                            selected_combination = st.selectbox("Select Combination", st.session_state.combinations)
                                
                            filtered_element_df = st.session_state.total_loads_df[st.session_state.total_loads_df['Combination'] == selected_combination]

                            filtered_node_df = st.session_state.total_node_df[st.session_state.total_node_df['Combination'] == selected_combination]
                            st.write(filtered_node_df)
                            st.write(filtered_element_df)
                            def load_comb():
                                st.session_state.data_load_combination = df_load_combination.copy()
                                st.session_state.filtered_node_df = filtered_node_df
                                st.session_state.filtered_element_df = filtered_element_df    
                            
                            Determine_loadcomb= st.button('Apply', on_click=load_comb) 
                                
            else:
                with col_part1:

                    def _finished_():

                        load_types = ['Dead', 'Live', 'Wind', 'Snow', 'Earthquake']
                        combination_factors = {}
                        print('pass')

                        for index, row in df_load_combination.iterrows():
                            combination_name = row['Combination']
                            factors = {load_type: row[load_type] for load_type in load_types}
                            combination_factors[combination_name] = factors
                        print('pass2')

                    
                        if 'Combination' not in element_all_loads_3d.columns:
                            element_all_loads_3d['Combination'] = combination_name
                        print('pass3')

                        element_wxy_dict = {}

                        for element_number, group_element in element_all_loads_3d.groupby('Element Number'):
                            element_combinations = {}
                            for _, group_combination in df_load_combination.iterrows():
                                combination_name = group_combination['Combination']
                                loadtype_wxy = {}
                                for load_type in load_types:
                                    loadtype_wxy[load_type] = {
                                        'Wx': group_element[group_element['Load Type'] == load_type]['Wx'].tolist(),
                                        'Wy': group_element[group_element['Load Type'] == load_type]['Wy'].tolist(),
                                        'Wz': group_element[group_element['Load Type'] == load_type]['Wz'].tolist()

                                    }
                                element_combinations[combination_name] = loadtype_wxy
                            element_wxy_dict[element_number] = element_combinations

                        total_loads = []
                        total_loads_df = pd.DataFrame(columns=['Element Number', 'Combination', 'Total Wx', 'Total Wy','Total Wz','Total Wz'])

                        for element_number, combinations in element_wxy_dict.items():
                            for combination_name, loadtypes in combinations.items():
                                total_wx = 0.0
                                total_wy = 0.0
                                total_wz = 0.0
                                for load_type in load_types:
                                    for wx in loadtypes[load_type]['Wx']:
                                        factor_value = combination_factors.get(combination_name, {}).get(load_type, 1.0)
                                        total_wx += wx * factor_value
                                    for wy in loadtypes[load_type]['Wy']:
                                        factor_value = combination_factors.get(combination_name, {}).get(load_type, 1.0)
                                        total_wy += wy * factor_value
                                    for wz in loadtypes[load_type]['Wz']:
                                        factor_value = combination_factors.get(combination_name, {}).get(load_type, 1.0)
                                        total_wz += wz * factor_value    

                                total_loads.append({'Element Number': element_number, 'Combination': combination_name, 'Total Wx': total_wx, 'Total Wy': total_wy ,'Total Wz':total_wz})

                        total_loads_element_df = pd.DataFrame(total_loads)
                        st.session_state.total_loads_df = total_loads_element_df
                        st.session_state.combinations = total_loads_df['Combination'].unique().tolist()
                        
                
                finished_button = st.button("finished", on_click= _finished_)  

                      
                    
                if 'total_loads_df' in st.session_state:

                    with col_part2:
                            st.session_state.combinations = st.session_state.total_loads_df['Combination'].unique().tolist()    
                            st.dataframe(st.session_state.total_loads_df)
                            
                                

                    with col_part3:
                    
                        selected_combination = st.selectbox("Select Combination", st.session_state.combinations)
                                    
                        filtered_element_df = st.session_state.total_loads_df[st.session_state.total_loads_df['Combination'] == selected_combination]
                        #filtered_node_df = st.session_state.total_node_df[st.session_state.total_node_df['Combination'] == selected_combination]
                        st.write(node_all_loads_3d)
                        st.write(filtered_element_df)
                        def load_comb():
                            st.session_state.data_load_combination = df_load_combination.copy()
                            st.session_state.filtered_node_df = node_all_loads_3d
                            st.session_state.filtered_element_df = filtered_element_df    
                                    
                        Determine_loadcomb= st.button('Apply', on_click=load_comb)
                

        with tab_lastmodel:
            st.write('Do you want to see the final model?')
            st.write('You should press the (See Model) button if you want. :)')

            buttons = st.button('See Model')


            if buttons:
                
                st.plotly_chart(st.session_state.graph_state_node,key="unique23")

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
    with tab_results:
      
        Analyze = st.button("Analyze")
        
        if option=='2D':
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
                    E = st.session_state.data_section['Modulus of Elastisity (MPa)']
                    for index,row in st.session_state.data_element.iterrows():
                        first_node = int(row['First Node Number'])
                        second_node = int(row['Second Node Number'])
                        element_num = int(row['Element Number'])
                        section_elm = (row['Section'])
                        
                        indexx= st.session_state.data_section.to_dict(orient='list')['Section Name'].index(section_elm)
                        
                        A = st.session_state.data_section.to_dict(orient='list')['Area(m^2)'][indexx]
                        if st.session_state.data_section.loc[indexx,'Section Type']=='Beam':
                            I = st.session_state.data_section.to_dict(orient='list')['I(3-3)(m^4)'][indexx]
                        else:
                            I = st.session_state.data_section.to_dict(orient='list')['I(2-2)(m^4)'][indexx]

                        
                        M = 0.
                        massType = "-lMass"
                        
                        ops.element('elasticBeamColumn',element_num,first_node,second_node,A,E[0],I,1,'-mass', M, massType)
                    
                    #st.session_state.data_support = df_support.copy()
                    for index, row in st.session_state.data_support.iterrows():
                        node_number = int(row['Support Node Number'])
                        x_direction = int(row['X direction'])
                        y_direction = int(row['Y direction'])
                        moment = int(row['Moment'])
                        ops.fix(node_number,x_direction,y_direction,moment)
                    
                    ops.timeSeries('Constant', 1)
                    ops.pattern('Plain', 1, 1)
                    


                    for index, row in st.session_state.filtered_element_df.iterrows():
                        Ew[int(row['Element Number'])]=['-beamUniform',float(row['Total Wy']),float(row['Total Wx'])]
                        print(Ew)

                    for etag in Ew:
                        ops.eleLoad('-ele', etag, '-type', Ew[etag][0], Ew[etag][1],Ew[etag][2])
        
                    for index, row in st.session_state.filtered_node_df.iterrows():
                        ops.load(int(row['Node Number']),float(row['Total Px']),float(row['Total Py']),float(row['Mz']))
                        print(int(row['Node Number']),float(row['Total Px']),float(row['Total Py']),float(row['Mz']))
                    
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
                
              
                
                with st.container():
                    col_part1,col_part2,col_part3 = st.columns(3)
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
                                        

                         
                    
                with st.container():
                    #outputs for nodes
                    displacements=[]
                

                    for i in st.session_state.data_node['Node Number']:
                        #   print(i)
                        disp_2d=ops.nodeDisp(int(i))
                        displacements.append(disp_2d)

                    df_output=pd.DataFrame(displacements, columns=['Disp. in X', 'Disp. in Y', 'Disp. in Z'])
                    df_outputs_final = pd.concat([st.session_state.data_node,df_output ], axis=1)
                    
                    df_outputs_final_st = st.data_editor(df_outputs_final)
                    
                        


                        
                with st.container():
                            
                        #outputs for elements
                    displacement_element=[]
                    nvm_element=[]
                    for i in st.session_state.data_element['Element Number']:
                    #   print(i)
                        disp_2d_el=ops.basicDeformation(int(i))
                        nvm=ops.eleForce(int(i))

                        displacement_element.append(disp_2d_el)
                        nvm_element.append(nvm)

                    st.session_state.data_element = st.session_state.data_element.drop(['Section','Story Level','Element Length (m)','Weight (kN)'], axis=1)
                    df_output_el=pd.DataFrame(displacement_element, columns=['Deform. in X', 'Deform. in Y', 'Deform. in Z'])
                    df_output_el_nvm=pd.DataFrame(nvm_element, columns=['N1', 'V1', 'M1','N2', 'V2', 'M2'])
                    

                    df_outputs_final_el = pd.concat([st.session_state.data_element,df_output_el,df_output_el_nvm ], axis=1)
                    
                    
                    df_merged_kolon = pd.merge(df_outputs_final_el, st.session_state.df_element_length[['Element Number', 'First_x_node', 'Second_x_node','First_y_node','Second_y_node']], on='Element Number', how='left')
                    for index, row in df_merged_kolon.iterrows():
                        if row['First_x_node'] == row['Second_x_node']:
                            # N1 ve V1 değerlerini birbirleriyle değiştir
                           df_merged_kolon.at[index, 'N1'], df_merged_kolon.at[index, 'V1'] = row['V1'], row['N1']
                           df_merged_kolon.at[index, 'N2'],df_merged_kolon.at[index, 'V2'] = row['V2'], row['N2']
                    
                    filtered_df_kolon = df_merged_kolon[(df_merged_kolon['First_x_node'] == df_merged_kolon['Second_x_node'])]
                    filtered_df_kiris = df_merged_kolon[(df_merged_kolon['First_y_node'] == df_merged_kolon['Second_y_node'])]
                    
                    st.write('kolonlar')
                    st.dataframe(filtered_df_kolon)
                    st.write('kirişler')
                    st.dataframe(filtered_df_kiris)
                    #df_kolon=pd.concat([st.session_state.df_element_length,df_outputs_final_el],axis=1)
                    #filtered_df = df[(df['First x node'] == 0) & (df['Second x node'] == 0)
                    #st.dataframe(df_kolon)
                   
                with st.container():
                  #  st.dataframe(df_modal)
                 
                    print(ops.printModel())
                    ops.printModel( '-file','deneme85')

                with st.container():
                    if st.session_state.df_element['Story Level'].max()>0:
        
                        numFloor=storynumber
                        numBay=baynumber
                        bayWidth=beamlength[0:baynumber:1]
                        bayWidth = [i for i in bayWidth for _ in range(2)]
                        storyHeights=list((reversed(columnlength[0::baynumber])))
                        print(columnlength)
                        print(storyHeights,'storyhe')

                        #mass for each element
                        listofbeamweights=[]
                        listofcolumnweights=[]
                        
                        st.session_state.df_element_length=st.session_state.df_element_length.sort_values(by=['Story Level'],ascending=False) #sorting from the top story to bottom story
                        st.dataframe(st.session_state.df_element_length)
                        for index, row in st.session_state.df_element_length.iterrows():
                            if row['First_y_node']==row['Second_y_node']:
                                listofbeamweights.append((row['Weight (kN)'])/9.81)
                            if row['First_x_node']==row['Second_x_node']:
                                listofcolumnweights.append((row['Weight (kN)'])/(9.81*2))  #ton

                        print(listofbeamweights,'beamweights')
                        print(listofcolumnweights,'columnweights')# from top to bpottom
                        col=[]# finding column masses for each story(lumped mass)
                        for i in range(0,len(listofcolumnweights),numBay+1):
                            sumcol=sum(listofcolumnweights[i:i+numBay+1])
                            col.append(sumcol)   
                        massxcolumn=[]
                        for i in range(0,len(col)-1):
                            weight_1=col[i]+col[i+1]
                            massxcolumn.append(weight_1)
                        massxcolumn.insert(0,col[0])
                        

                        #finding beam masses for each story(lumped mass)
                        massxbeam=[]
                        for i in range(0,len(listofbeamweights),numBay):
                            sumbeam=sum(listofbeamweights[i:i+numBay])
                            massxbeam.append(sumbeam)
                        #summing beams and column masses for each lumped mass
                        massxstory=[sum(i) for i in zip(massxbeam, massxcolumn)]
                        massxstory=massxstory[::-1] #sorting from bottom story to top story
                        print(massxstory,"story agırlık")
                        print(massxbeam,'massxbeam')
                        print(massxcolumn,'massxcolumn')
                        
                        ops.wipe()
                        ops.model('Basic', '-ndm', 2)

                        E = 25000000
                        
                        coordTransf = "Linear"  # Linear, PDelta, Corotational
                    

                    
                        #column sections for each column 
                        
                        columntable=st.session_state.df_element_length
                        columntable=columntable.sort_values(by='First_x_node')
                        columntable = columntable[columntable['First_x_node'] == columntable['Second_x_node']]

                        columntable['A']=columntable['Section'].map( st.session_state.data_section.set_index('Section Name')['Area(m^2)'])
                        columntable['I']=columntable['Section'].map( st.session_state.data_section.set_index('Section Name')['I(2-2)(m^4)'])
                        columnsections=[]
                        
                        for i in range(0,len(columntable),storynumber):
                            columntable2=columntable.iloc[i:i+storynumber]
                            columntable2=columntable2.sort_values(by='First_y_node')
                            columnsections+=columntable2['Section'].tolist()
                        columnsections = [columnsections[i:i+storynumber] for i in range(0, len(columnsections), storynumber)]
                    
                        #beam sections for each story
                        beamtable=st.session_state.df_element_length.sort_values(by='First_y_node')
                        beamtable = beamtable[beamtable['First_y_node'] == beamtable['Second_y_node']]
                        beamtable['A']=beamtable['Section'].map( st.session_state.data_section.set_index('Section Name')['Area(m^2)'])
                        beamtable['I']=beamtable['Section'].map( st.session_state.data_section.set_index('Section Name')['I(3-3)(m^4)'])
                        beamsections=[]
                        for i in range(0,len(beamtable)):
                            beamtable2=beamtable.iloc[i:i+numBay]
                            beamtable2=beamtable2.sort_values(by='First_x_node')
                            beamsections.extend(beamtable2['Section'].tolist())
                        print(beamsections,"kiriş enkesit")

                        section_all={}
                        for index,row in columntable.iterrows():
                            key=row['Section']
                            A=row['A']
                            I=row['I']
                            if key not in section_all:
                                section_all[key]=[A,I]
                        for index,row in beamtable.iterrows():
                            key=row['Section']
                            A=row['A']
                            I=row['I']
                            if key not in section_all:
                                section_all[key]=[A,I]
                        

                        # procedure to read
                        def ElasticBeamColumn(eleTag, iNode, jNode, sectType, E, transfTag, M, massType):
                            found = 0

                            prop = section_all[sectType]
                            A = prop[0]
                            I = prop[1]
                            ops.element('elasticBeamColumn', eleTag, iNode, jNode, A, E, I, transfTag, '-mass', M, massType)

                        print ("nerede duruyor")

                        # add the nodes
                        #  - floor at a time
                        yLoc = 0.
                        nodeTag = 1
                        for j in range(0, numFloor + 1):   #  NODE OLUŞTURMA

                            xLoc = 0.
                            for i in range(0, numBay + 1):
                                ops.node(nodeTag, xLoc, yLoc)
                                if yLoc==0:
                                    ops.fix(nodeTag,1,1,1)

                                xLoc += bayWidth[i]
                                nodeTag += 1

                            if j < numFloor:
                                storyHeight = storyHeights[j]

                            yLoc += storyHeight
                        
                    
                        # fix first floor

                        #for index,row in st.session_state.data_node[st.session_state.data_node['Node y']==0].iterrows():
                            #   ops.fix(int(row['Node Number']),1,1,1)
                        

                        # rigid floor constraint & masses

                        nodeTagR = baynumber+3
                        nodeTag = baynumber+2
                        a_j=0
                        mass_index=0
                        
                        for j in range(1, numFloor + 1):
                            for i in range(0, numBay + 1):

                                if nodeTag != nodeTagR:
                                    ops.equalDOF(nodeTagR, nodeTag, 1)
                                    print(nodeTagR, nodeTag, 1)
                                else:
                                                            # `mass_index`'i kullanarak doğru değeri alıyoruz ve artırıyoruz
                                    if mass_index < len(massxstory):  # index sınırını kontrol edelim
                                        a_j = massxstory[mass_index]
                                        ops.mass(nodeTagR, a_j, 1.0e-10, 1.0e-10)
                                        print(nodeTagR, a_j, 1.0e-10, 1.0e-10)
                                        mass_index += 1  # index artırılıyor

                                nodeTag += 1

                            nodeTagR += numBay + 1
                        
                        M = 0.
                        massType = "-lMass"

                        # add the columns
                        # add column element
                        ops.geomTransf(coordTransf, 1)

                        eleTag = 1

                        
                        for j in range(0,numBay + 1):

                            end1 = j + 1
                            end2 = end1 + numBay + 1

                            thisColumn = columnsections[j]

                            for i in range(0, numFloor):
                                secType = thisColumn[i]
                                ElasticBeamColumn(eleTag, end1, end2, secType, E, 1, M, massType)
                                end1 = end2
                                end2 += numBay + 1
                                eleTag += 1

                        # add beam elements
                        for j in range(1, numFloor + 1):
                            end1 = (numBay + 1) * j + 1
                            end2 = end1 + 1
                            
                            for i in range(0, numBay):
                                secType = beamsections[i]
                                ElasticBeamColumn(eleTag, end1, end2, secType, E, 1, M, massType)
                                end1 = end2
                                end2 = end1 + 1
                                eleTag += 1
                    

                        
                        # calculate eigenvalues & print results
                        numEigen = len(storyHeights)+1
                        eigenValues = ops.eigen('-fullGenLapack',numEigen)
                        print(numEigen, "eigen number")
                        print(eigenValues,"değerleri")
                        PI = 2 * asin(1.0)
                        ops.timeSeries('Linear', 1)
                        ops.pattern('Plain', 1, 1)
                        ops.integrator('LoadControl', 1.0)
                        ops.algorithm('Linear')
                        ops.analysis('Static')
                        ops.analyze(1)
                        periodlist=[]
                        for i in range(0,numEigen):
                            period=2*PI/sqrt(eigenValues[i])
                            periodlist.append(period)
                        
                        opsv.plot_model()
                        col_part1,col_part2,col_part3 = st.columns(3)
                        with col_part1:
                            st.pyplot(plt.gcf())

                            with col_part2:
                                

                                data_dict=ops.modalProperties('-return','-unorm')
                                print('it works')
                            
                                # Find the maximum length
                                max_length = max(len(v) for v in data_dict.values())

                                # Extend each list to the maximum length with None or any other placeholder
                                for key, value in data_dict.items():
                                    if len(value) < max_length:
                                        value.extend([None] * (max_length - len(value)))

                                # Convert to DataFrame
                                df_modal = pd.DataFrame(data_dict)
                    
                                ops.responseSpectrumAnalysis(1,1)
                                
                            
                                modenumbers=list(range(1, numEigen+1))
                                df_period=pd.DataFrame({
                                    'Mode Number':modenumbers,
                                    'Period':periodlist
                                })
                                st.session_state.data_period=st.data_editor(df_period,num_rows='dynamic')

                                print(df_period)

                                
                                with col_part3:
                                    opsv.plot_mode_shape(1)
                            
                                    st.pyplot(plt.gcf())

                    else:
                        st.write('kiriş hesabı')
                                    
                
                    

                                    

        else:
            if Analyze:
                
                ops.wipe()  #required to open a new model
                ops.model('basic', '-ndm', 3, '-ndf', 6)
                
                #st.session_state.data_node =df_node.copy()
                i=0

                #shear modulus ve polar moment of inertia hesabı yapılmadı#
              

                for index, row in st.session_state.data_node_3d.iterrows():
                    node_number = int(row['Node Number'])
                    indexx= st.session_state.data_node_3d.to_dict(orient='list')['Node Number'].index(node_number)
                    x_axis_node = st.session_state.data_node_3d.to_dict(orient='list')['Node x'][indexx]      
                    y_axis_node = st.session_state.data_node_3d.to_dict(orient='list')['Node y'][indexx]
                    z_axis_node = st.session_state.data_node_3d.to_dict(orient='list')['Node z'][indexx]
                    ops.node(i+1,x_axis_node,y_axis_node,z_axis_node)
                    i+=1
                ###???#####          
                gTTagz = 1
                gTTagx = 2
                gTTagy = 3
                

                coordTransf = 'Linear'
                
                ops.geomTransf(coordTransf, gTTagz, 0., -1., 0.)
                ops.geomTransf(coordTransf, gTTagx, 0., -1., 0.)
                ops.geomTransf(coordTransf, gTTagy, 1., 0., 0.)
                
                
              
               #for i, row in st.session_state.df_element_length.iterrows():
                   #if row['First_y_node'] != row['Second_y_node'] and row['First_x_node'] == row['Second_x_node'] and row['First_z_node'] == row['Second_z_node'] :
                   #    ops.geomTransf(coordTransf, i, 1., 0., 0.)qS
                  # elif row['First_x_node'] != row['Second_x_node'] and row['First_y_node'] == row['Second_y_node'] and row['First_z_node'] == row['Second_z_node'] :
                  #     ops.geomTransf(coordTransf, i, 0., -1., 0.)
                  # elif row['First_z_node'] != row['Second_z_node'] and row['First_y_node'] == row['Second_y_node'] and row['First_x_node'] == row['Second_x_node'] :
                  #     ops.geomTransf(coordTransf, i, 0., -1, 0)"""
                

                #st.session_state.data_element = df_element.copy()
                E = st.session_state.data_section['Modulus of Elastisity (MPa)']
                for index,row in st.session_state.df_element_length.iterrows():
                    if pd.isna(row['First Node Number']):
                        continue
                    else:
                        first_node = int(row['First Node Number'])
                        second_node = int(row['Second Node Number'])
                        element_num = int(row['Element Number'])
                        section_elm = (row['Section'])
                        indexx= st.session_state.data_section.to_dict(orient='list')['Section Name'].index(section_elm)
                        A = st.session_state.data_section.to_dict(orient='list')['Area(m^2)'][indexx]      
                        Iy = st.session_state.data_section.to_dict(orient='list')['I(2-2)(m^4)'][indexx]
                        Iz = st.session_state.data_section.to_dict(orient='list')['I(3-3)(m^4)'][indexx]
                        G = st.session_state.data_section.to_dict(orient='list')['G(MPa)'][indexx]
                        J = st.session_state.data_section.to_dict(orient='list')['J(m^4)'][indexx]
                        #ornekteki gibi lumped mass atanmadı####        
                        
                        #coord transf yapıldı.

                        if row['First_y_node']!=row['Second_y_node']:
                            gTTag= gTTagy
                        elif row['First_x_node']!=row['Second_x_node']:
                            gTTag= gTTagx

                        elif row['First_z_node']!=row['Second_z_node']:
                            gTTag= gTTagz

                        

                        
                        ops.element('elasticBeamColumn',element_num,first_node,second_node,A,E[0],G,J,Iy,Iz,gTTag)
                    
            

                

                        
                            
                #st.session_state.data_support = df_support.copy()
                for index, row in st.session_state.data_support_3d.iterrows():
                    node_number = int(row['Support Node Number'])
                    x_direction = int(row['X translation'])
                    y_direction = int(row['Y translation'])
                    z_direction = int(row['Z translation'])
                    moment_x = int(row['Rotation about x'])
                    moment_y =int(row['Rotation about y'])
                    moment_z =int(row['Rotation about z'])
                    ops.fix(node_number,x_direction,y_direction,z_direction,moment_x,moment_y,moment_z)
                            
                ops.timeSeries('Constant', 1)
                ops.pattern('Plain', 1, 1)
            

                Ew={}
         
                for index,row in st.session_state.filtered_element_df.iterrows():
                    Ew[int(row['Element Number'])]=['-beamUniform',float(row['Total Wy']),float(row['Total Wz']),float(row['Total Wx'])]
                    print(Ew)
            
                for etag in Ew:
                    ops.eleLoad('-ele', etag, '-type', Ew[etag][0], Ew[etag][1],Ew[etag][2],Ew[etag][3])

                
                for index, row in st.session_state.filtered_node_df.iterrows():
                    ops.load(int(row['Node Number']),float(row['Px']),float(row['Py']),float(row['Pz']),float(row['Mx']),float(row['My']),float(row['Mz']))
                            
                ops.constraints('Transformation')
                ops.numberer('RCM')
                ops.system('BandGeneral')
                ops.test('NormDispIncr', 1.0e-6, 6, 2)
                ops.algorithm('Linear')
                ops.integrator('LoadControl', 1)
                ops.analysis('Static')
                ops.analyze(1)
            
                sfacVy = 10.e-3
                sfacVz = 10.e-3
                sfacMy = 10.e-3
                sfacMz = 10.e-3
                sfacT = 10.e-3
                sfacN = 10.e-3
                fig_wi_he = 30,20
                
                
        
                col_part1, col_part2 = st.columns(2)

                with col_part1:

                    opsv.section_force_diagram_3d('Vz',int(sfacVz))
                    plt.title('Transverse force Vz')
                    st.pyplot(plt.gcf())
                            
                    with col_part2:
                        opsv.section_force_diagram_3d('Vy',int(sfacVy))
                        plt.title('Transverse force Vy')
                        st.pyplot(plt.gcf())

                st.divider()
                with col_part1:

                    opsv.section_force_diagram_3d('My',int(sfacMy))
                    plt.title('Bending moments My')
                    st.pyplot(plt.gcf())
                            
                    with col_part2:
                        opsv.section_force_diagram_3d('Mz',int(sfacMz))
                        plt.title('Bending moments Mz')
                        st.pyplot(plt.gcf())

                st.divider()
                with col_part1:

                    opsv.section_force_diagram_3d('N',int(sfacN))
                    plt.title('Axial force distribution')
                    st.pyplot(plt.gcf())

                    with col_part2:
                            opsv.section_force_diagram_3d('T',int(sfacT))
                            plt.title('Torsional Moment T')
                            st.pyplot(plt.gcf())

                            print(ops.printModel())

                st.divider()

                with st.container():
                            
                        #outputs for elements
                    displacement_element=[]
                    nvm_element=[]

                    for i in st.session_state.data_element['Element Number']:
                    #   print(i)
                        nvm=ops.eleForce(int(i))
                        nvm_element.append(nvm)
                        print('element number',i,nvm)
                        print(nvm_element)
                    print(nvm_element)
                    st.session_state.data_element = st.session_state.data_element.drop(['Section','Story Level','Element Length (m)','Weight (kN)'], axis=1)
                    
                    df_output_el_nvm=pd.DataFrame(nvm_element, columns=['N1', 'Mz1', 'Vy1','My1', 'Vz1', 'T1','N2', 'Mz2', 'Vy2','My2', 'Vz2', 'T2'])
                    #df_output_el_nvm=df_output_el_nvm.drop(['My1', 'Vz1','T1','My2', 'Vz2','T2'],axis=1)

                    df_outputs_final_el = pd.concat([st.session_state.data_element,df_output_el_nvm ], axis=1)
                    
                    
                    df_merged_kolon = pd.merge(df_outputs_final_el, st.session_state.df_element_length[['Element Number', 'First_x_node', 'Second_x_node','First_y_node','Second_y_node','First_z_node','Second_z_node']], on='Element Number', how='left')
                    
                    #for index, row in df_merged_kolon.iterrows():
                    #    if row['First_x_node'] == row['Second_x_node'] and row['First_z_node']==row['Second_z_node']:
                    #        # N1 ve mZ1 değerlerini birbirleriyle değiştir
                    #       df_merged_kolon.at[index, 'N1'], df_merged_kolon.at[index, 'Mz1'] = row['Mz1'], row['N1']
                    #       df_merged_kolon.at[index, 'N2'],df_merged_kolon.at[index, 'Mz2'] = row['Mz2'], row['N2']
                          
                    
                    filtered_df_kolon = df_merged_kolon[((df_merged_kolon['First_y_node']==df_merged_kolon['Second_y_node']) & (df_merged_kolon['First_x_node']==df_merged_kolon['Second_x_node']))]
                    filtered_df_kiris = df_merged_kolon[(((df_merged_kolon['First_y_node']==df_merged_kolon['Second_y_node']) & (df_merged_kolon['First_z_node']==df_merged_kolon['Second_z_node'])) | ((df_merged_kolon['First_x_node']==df_merged_kolon['Second_x_node']) & (df_merged_kolon['First_z_node']==df_merged_kolon['Second_z_node'])))]
                    
                    st.write('kolonlar')
                    st.dataframe(filtered_df_kolon)
                    st.write('kirişler')
                    st.dataframe(filtered_df_kiris)
                    #df_kolon=pd.concat([st.session_state.df_element_length,df_outputs_final_el],axis=1)
                    #filtered_df = df[(df['First x node'] == 0) & (df['Second x node'] == 0)
                    #st.dataframe(df_kolon)
                exit()



    



    

        