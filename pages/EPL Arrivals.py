import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# For sankey chart
import holoviews as hv
from holoviews import opts, dim
from bokeh.plotting import show
hv.extension('bokeh', logo=False)

# For image display
from PIL import Image

#####################################################################

# Import the sankey function from the sankey module within pySankey
from pySankey.sankey import sankey
from pandasql import sqldf 


@st.cache
def download_data():
    df=pd.read_excel('https://github.com/adlihs/streamlit/releases/download/data/england_transfers.xlsx',
                     engine='openpyxl')
    df = df.query("transfer_type == 'Arrivals'")
    
    df_position = (df.groupby(['team_name', 'player_position']).size() 
     .sort_values(ascending=False) 
     .reset_index(name='count'))
    
    df_league = (df.groupby(['league_2']).size() 
     .sort_values(ascending=False) 
     .reset_index(name='count'))
    
    df_league['league_2'] = df_league['league_2'].str.replace('Premier League', 'Premier League (Local)')
    


    return df_position, df_league

arrivals_position, arrivals_league = download_data()
#arrivals

# Title display
st.markdown(
    """
    # EPL Arrivals
    ### Transfer Window 2022-2023
    """
)


###### arrivals_position Graph display ######
arrivals_position_data = hv.Sankey(arrivals_position)
arrivals_position_sankey = hv.render(arrivals_position_data.opts(width=1000, 
                                               height=1400,
                                               label_position='left', 
                                               edge_color=dim('team_name').str(),
                                               title="Arrivals by Positions",
                                               bgcolor='white')
    , backend='bokeh')

# Hide holoviews toolbar
arrivals_position_sankey.toolbar.autohide = True

# Display Sankey
st.write(arrivals_position_sankey)

###### arrivals_league Graph display ######


# Display Sankey
#st.write(arrivals_league_sankey)
#st.bar_chart(arrivals_league)

#st.write(hv.render(arrivals_data.opts(width=1000, height=1400,label_position='left', edge_color=dim('team_name').str())
    #, backend='bokeh'))

# https://tmsi.akamaized.net/head/transfermarkt_logo.svg

image = Image.open('transfermarkt_logo.png')

st.image(image, caption='')