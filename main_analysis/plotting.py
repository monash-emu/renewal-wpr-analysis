import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta

def plot_main_plot(model_data, case_data, mobility_data, vax_data):
    
    # Define elements needed to add case plot
    case_index = case_data.index
    cases = case_data
    
    # Define elements needed to add median line plots
    model_index = model_data.index
    weekly_median = model_data["weekly_sum"][0.50]
    rt_median = model_data["R"][0.50]
    
    
    # Define elements needed for uncertainty plots
    x_vals = model_data.index.to_list() + model_data.index[::-1].to_list()
    y_vals_weekly = model_data["weekly_sum"][0.05].to_list() + model_data["weekly_sum"][0.95][::-1].to_list()
    y_vals_R = model_data["R"][0.05].to_list() + model_data["R"][0.95][::-1].to_list()
    
    # Define elements for mobility plot
    mobility_index = mobility_data.index
    mobility_est = ['transit_stations_percent_change_from_baseline', 'workplaces_percent_change_from_baseline', 'residential_percent_change_from_baseline']
    
    # Define elements for vax plot
    vax_index = vax_data.index
    vax_est = vax_data['people_fully_vaccinated_per_hundred']
                                 
    # Create 2x2 subplot
    fig = make_subplots(2,2, shared_xaxes=True)
    
    # Add modelled case notifications median line
    fig.add_trace(go.Scatter(x=model_index, y=weekly_median, mode="lines", name="Modelled cases", marker_color='#636EFA' ), row=1, col=1)
    # Add modelled case notifications uncertainty
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals_weekly, mode="lines", name="Modelled cases", line={"width": 0.0, "color": '#636EFA'}, fill='toself', showlegend=False ), row=1, col=1)
    
    # Add case notifications
    fig.add_trace(go.Scatter(x=case_index, y=cases,  mode="markers", name="Reported cases", marker_color="black" ), row=1, col=1)
    
    # Add Rt median line
    fig.add_trace(go.Scatter(x=model_index, y=rt_median, mode="lines", name="Rt", marker_color='#00CC96' ), row=1, col=2)
    # Add Rt uncertainty 
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals_R, mode="lines", name="Rt", line={"width": 0.0, "color": '#00CC96'}, fill='toself', showlegend=False ), row=1, col=2)
    
    # Add mobility figure
    for i in mobility_est:
        fig.add_trace(go.Scatter(x=mobility_data.index, y=mobility_data[i], mode="lines", name="Mobility", line={"color": 'black'}), row=2, col=1)
    
    # Add vaccination figure
    fig.add_trace(go.Scatter(x=vax_data.index, y=vax_est, mode="lines", name="Vaccination",), row=2, col=2)
    
                                 
    return fig.update_layout(height=800, width=1200)

