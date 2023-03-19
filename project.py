import pandas as pd
import numpy as np
import plotly.graph_objects as go
import h3
import streamlit as st
from catboost import CatBoostRegressor

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
     
    return "%d:%02d:%02d" % (hour, minutes, seconds)

def main():
  model = CatBoostRegressor()
  model.load_model("model")

  dist_model = CatBoostRegressor()
  dist_model.load_model('dist_model')

  start_h3 = st.text_input("Start H3", key="start_h3")

  end_h3 = st.text_input("End H3", key="end_h3")
  
  distance_in_meters = st.text_input('Distance in km (type "predict" if unknown)', key="distance_in_meters")
  
  valhalla_time = st.text_input("Valhalla time", key="valhalla_time")
  valhalla_time = int(valhalla_time)

  start_lat = h3.cell_to_latlng(start_h3)[0]
  start_lng = h3.cell_to_latlng(start_h3)[1]
  end_lat = h3.cell_to_latlng(end_h3)[0]
  end_lng = h3.cell_to_latlng(end_h3)[1]
  
  if st.button('Predict time'): 
    if distance_in_meters == 'predict':
        input_ = [start_lat, start_lng, end_lat, end_lng, valhalla_time]
        distance_in_meters = int(dist_model.predict(np.array(input_)))
        st.write('Predicted distance in meters:', str(round(float(distance_in_meters)/1000)), 'km')
    else:
        distance_in_meters = float(distance_in_meters)*1000
    
    input_1 = [start_lat, start_lng, end_lat, end_lng, distance_in_meters, 1, valhalla_time]
    input_2 = [start_lat, start_lng, end_lat, end_lng, distance_in_meters, 2, valhalla_time]
    input_3 = [start_lat, start_lng, end_lat, end_lng, distance_in_meters, 3, valhalla_time]    
    
    data = {'Monday, 8 AM' : [convert(model.predict(np.array(input_1)))],
            'Thursday, 11 PM' : [convert(model.predict(np.array(input_2)))],
            'Sunday, 3 PM' : [convert(model.predict(np.array(input_3)))]}

    df = pd.DataFrame(data)
    # CSS to inject contained in a string
    hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
                                   
    st.write('Initial coordinates:', str(h3.cell_to_latlng(start_h3)))
    st.write('Final coordinates:', str(h3.cell_to_latlng(end_h3)))
    st.table(df)


if __name__ == "__main__":
    main()
