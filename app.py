# from flask_cors import CORS 
# from flask import Flask, jsonify
# app = Flask(__name__)
# CORS(app)  # This will enable CORS for all routes

# @app.route('/api/data')
# def get_data():
#     data = {
#         "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"],
#         "values": [10, 41, 35, 51, 49, 62, 69, 91, 148]
#     }
#     return jsonify(data)

# if __name__ == '__main__':
#     app.run(debug=True)



import os
import pandas as pd
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Load the Excel file path from the environment variable
file_path = os.getenv('EXCEL_FILE_PATH')

# Log the file path for debugging
print(f"Using Excel file path: {file_path}")

if not os.path.isfile(file_path):
    raise FileNotFoundError(f"The file {file_path} does not exist")

xlsx = pd.ExcelFile(file_path)
df = pd.read_excel(file_path, sheet_name='Test Sheet')

# Data cleaning and preprocessing as before
df = df.drop(columns=['Column2', 'Column3', 'Column4', 'Column5'])
df.dropna(subset=['Date Lead Received '], inplace=True)
df['Date Lead Received'] = pd.to_datetime(df['Date Lead Received '], errors='coerce')
df['Date Quote Created'].fillna(pd.Timestamp('2000-01-01'), inplace=True)
df['Start Date'].fillna(pd.Timestamp('2000-01-01'), inplace=True)
df['Quote Number'].fillna(0, inplace=True)
df['Customer Name'].fillna('Unknown', inplace=True)
df['Assigned to'].fillna('Unassigned', inplace=True)
df['Sales Rep'].fillna('Unassigned', inplace=True)
df['Value'].fillna(0, inplace=True)
df['Device Type'].fillna('Unknown Device', inplace=True)
df['Email'].fillna('No Email', inplace=True)
df['Status'].fillna('Unknown Status', inplace=True)
df['Notes'].fillna('No Notes', inplace=True)

@app.route('/api/monthlytrend')
def monthly_trend():
    df_2024 = df[df['Date Lead Received'].dt.year == 2024]
    df_2024['Month'] = df_2024['Date Lead Received'].dt.to_period('M')
    monthly_trends = df_2024.groupby('Month').size()
    data = {
        'labels': monthly_trends.index.astype(str).tolist(),
        'values': monthly_trends.tolist()
    }
    return jsonify(data)

@app.route('/api/bars')
def bars():
    lead_source_counts = df.groupby('Lead Source').size().reset_index(name='Number of Leads')
    lead_source_counts = lead_source_counts.sort_values(by='Number of Leads', ascending=False)
    data = {
        'lead_sources': {
            'labels': lead_source_counts['Lead Source'].tolist(),
            'values': lead_source_counts['Number of Leads'].tolist()
        }
    }
    return jsonify(data)


@app.route('/api/depots')
def depots():
    depot_counts = df.groupby('Depot').size().reset_index(name='Number of Leads')
    depot_counts = depot_counts.sort_values(by='Number of Leads', ascending=False)
    data = {
        'depots': {
            'labels': depot_counts['Depot'].tolist(),
            'values': depot_counts['Number of Leads'].tolist()
        },
    }
    return jsonify(data)

@app.route('/api/scatter')
def scatter():
    top_device_types = df['Device Type'].value_counts().nlargest(10).index
    df_filtered = df[df['Device Type'].isin(top_device_types)]
    grouped_counts = df_filtered.groupby(['Lead Category', 'Device Type']).size().unstack(fill_value=0)
    data = {
        'categories': grouped_counts.index.tolist(),
        'devices': grouped_counts.columns.tolist(),
        'values': grouped_counts.values.tolist()
    }
    return jsonify(data)

@app.route('/api/stackedbar')
def stacked_bar():
    df['Date Lead Received'] = pd.to_datetime(df['Date Lead Received'])
    df['Month'] = df['Date Lead Received'].dt.strftime('%B')
    sales_by_month_device = df.groupby(['Month', 'Device Type']).size().reset_index(name='Number of Sales')
    max_sales_per_device = sales_by_month_device.loc[sales_by_month_device.groupby('Device Type')['Number of Sales'].idxmax()]
    data = {
        'months': max_sales_per_device['Month'].tolist(),
        'devices': max_sales_per_device['Device Type'].tolist(),
        'values': max_sales_per_device['Number of Sales'].tolist()
    }
    return jsonify(data)



@app.route('/api/salesrep')
def sales_rep():
    sales_by_rep = df['Sales Rep'].value_counts().reset_index(name='Number of Sales')
    sales_by_rep.columns = ['Sales Rep', 'Number of Sales']
    sorted_sales_reps = sales_by_rep.sort_values(by='Number of Sales', ascending=False)
    top_sales_reps = sorted_sales_reps.head(5)
    data = {
        'sales_reps': top_sales_reps['Sales Rep'].tolist(),
        'values': top_sales_reps['Number of Sales'].tolist()
    }
    return jsonify(data)


# @app.route('/api/salesrep')
# def salesrep():
#     # Replace 'Unassigned' in 'Sales Rep' with corresponding value in 'Assigned to'
#     df['Sales Rep'] = df.apply(lambda row: row['Assigned to'] if row['Sales Rep'] == 'Unassigned' else row['Sales Rep'], axis=1)

#     sales_by_rep = df['Sales Rep'].value_counts().reset_index(name='Number of Sales')
#     sales_by_rep.columns = ['Sales Rep', 'Number of Sales']  # Rename columns for clarity
#     sorted_sales_reps = sales_by_rep.sort_values(by='Number of Sales', ascending=False)

#     top_sales_reps = sorted_sales_reps.head(5)

#     top_sales_reps_details = pd.merge(top_sales_reps, df[['Sales Rep', 'Customer Name', 'Lead Category', 'Assigned to']],
#                                       on='Sales Rep', how='left')

#     # Plotting
#     fig_top_sales_reps = pd.bar(top_sales_reps_details, x='Sales Rep', y='Number of Sales', title='Top 5 Sales Representatives by Number of Sales',
#                                 labels={'Sales Rep': 'Sales Representative', 'Number of Sales': 'Number of Sales'},
#                                 hover_data=['Customer Name', 'Lead Category', 'Assigned to'])

#     fig_top_sales_reps.update_layout(xaxis_title='Sales Representative', yaxis_title='Number of Sales')
#     fig_top_sales_reps.show()


# salesrep()


@app.route('/api/donuts')
def donuts():
    sales_by_category = df['Lead Category'].value_counts().reset_index(name='Number of Sales')
    sales_by_category.columns = ['Lead Category', 'Number of Sales']
    sales_by_device = df['Device Type'].value_counts().reset_index(name='Number of Sales')
    sales_by_device.columns = ['Device Type', 'Number of Sales']
    lead_source_counts = df['Lead Source'].value_counts().reset_index(name='Number of Leads')
    lead_source_counts.columns = ['Lead Source', 'Number of Leads']
    status_counts = df['Status'].value_counts().reset_index(name='Number of Leads')
    status_counts.columns = ['Status', 'Number of Leads']
    df['Date Lead Received'] = pd.to_datetime(df['Date Lead Received'])
    df['Month'] = df['Date Lead Received'].dt.strftime('%B')
    monthly_trends = df['Month'].value_counts().reset_index(name='Number of Leads')
    monthly_trends.columns = ['Month', 'Number of Leads']
    data = {
        'categories': {
            'labels': sales_by_category['Lead Category'].tolist(),
            'values': sales_by_category['Number of Sales'].tolist()
        },
        'devices': {
            'labels': sales_by_device['Device Type'].tolist(),
            'values': sales_by_device['Number of Sales'].tolist()
        },
        'lead_sources': {
            'labels': lead_source_counts['Lead Source'].tolist(),
            'values': lead_source_counts['Number of Leads'].tolist()
        },
        'statuses': {
            'labels': status_counts['Status'].tolist(),
            'values': status_counts['Number of Leads'].tolist()
        },
        'months': {
            'labels': monthly_trends['Month'].tolist(),
            'values': monthly_trends['Number of Leads'].tolist()
        }
    }
    return jsonify(data)

@app.route('/api/top5')
def top5():
    categories = ['Lead Source', 'Brand Source',  'Lead Category', 'Customer Name']
    top5_data = {}
    for category in categories:
        if category in df.columns:
            top_5 = df[category].value_counts().nlargest(5).reset_index()
            top_5.columns = [category, 'Count']
            top5_data[category] = {
                'labels': top_5[category].tolist(),
                'values': top_5['Count'].tolist()
            }
    return jsonify(top5_data)


if __name__ == '__main__':
    app.run(debug=True)















# from flask import jsonify, Flask
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from plotly.subplots import make_subplots
# import plotly.graph_objects as go
# import plotly.express as px


# app = Flask(__name__)

# # Load the Excel file
# file_path = 'TEST TRACKER.xlsx'
# df = pd.read_excel(file_path, sheet_name='Test Sheet')

# # Function to calculate monthly trend
# # Example of checking column existence and handling datetime
# @app.route('/api/monthlytrend')

# def monthly_trend():
#     print(df.columns)  # Check columns for debugging purposes
    
#     if 'Date Lead Received' in df.columns:
#         df['Date Lead Received'] = pd.to_datetime(df['Date Lead Received'], errors='coerce')
#         df_2024 = df[df['Date Lead Received'].dt.year == 2024]
        
#         # Example of plotting
#         monthly_trends = df_2024.groupby('Month').size()
#         plt.figure(figsize=(10,6))
#         monthly_trends.plot(kind='line', marker='o')
#         plt.title('Monthly Trends of Leads in 2024')
#         plt.xlabel('Month')
#         plt.ylabel('Number of Leads')
#         plt.grid()
#         plt.show()
        
#         return df_2024
#     else:
#         print("Column 'Date Lead Received' not found in DataFrame.")

# # Call the function
# monthly_trend_data = monthly_trend()



# # Function to calculate bars
# @app.route('/bars_data', methods=['GET'])

# def bars():
#     depot_counts = df.groupby('Depot').size().reset_index(name='Number of Leads')
#     lead_source_counts = df.groupby('Lead Source').size().reset_index(name='Number of Leads')
#     depot_counts = depot_counts.sort_values(by='Number of Leads', ascending=False)
#     lead_source_counts = lead_source_counts.sort_values(by='Number of Leads', ascending=False)
#     data = {
#         'depots': {
#             'labels': depot_counts['Depot'].tolist(),
#             'values': depot_counts['Number of Leads'].tolist()
#         },
#         'lead_sources': {
#             'labels': lead_source_counts['Lead Source'].tolist(),
#             'values': lead_source_counts['Number of Leads'].tolist()
#         }
#     }
#     return jsonify(data)

# # Function to calculate scatter plot
# def scatter():
#     top_device_types = df['Device Type'].value_counts().nlargest(10).index
#     df_filtered = df[df['Device Type'].isin(top_device_types)]
#     grouped_counts = df_filtered.groupby(['Lead Category', 'Device Type']).size().unstack(fill_value=0)
#     data = {
#         'categories': grouped_counts.index.tolist(),
#         'devices': grouped_counts.columns.tolist(),
#         'values': grouped_counts.values.tolist()
#     }
#     return jsonify(data)

# # Function to calculate stacked bar chart
# def stacked_bar():
#     df['Date Lead Received'] = pd.to_datetime(df['Date Lead Received'])
#     df['Month'] = df['Date Lead Received'].dt.strftime('%B')
#     sales_by_month_device = df.groupby(['Month', 'Device Type']).size().reset_index(name='Number of Sales')
#     max_sales_per_device = sales_by_month_device.loc[sales_by_month_device.groupby('Device Type')['Number of Sales'].idxmax()]
#     data = {
#         'months': max_sales_per_device['Month'].tolist(),
#         'devices': max_sales_per_device['Device Type'].tolist(),
#         'values': max_sales_per_device['Number of Sales'].tolist()
#     }
#     return jsonify(data)

# # Function to calculate sales rep performance
# def sales_rep():
#     sales_by_rep = df['Sales Rep'].value_counts().reset_index(name='Number of Sales')
#     sales_by_rep.columns = ['Sales Rep', 'Number of Sales']
#     sorted_sales_reps = sales_by_rep.sort_values(by='Number of Sales', ascending=False)
#     top_sales_reps = sorted_sales_reps.head(5)
#     data = {
#         'sales_reps': top_sales_reps['Sales Rep'].tolist(),
#         'values': top_sales_reps['Number of Sales'].tolist()
#     }
#     return jsonify(data)


# # Function to calculate donut charts
# def donuts():
#     sales_by_category = df['Lead Category'].value_counts().reset_index(name='Number of Sales')
#     sales_by_category.columns = ['Lead Category', 'Number of Sales']
#     sales_by_device = df['Device Type'].value_counts().reset_index(name='Number of Sales')
#     sales_by_device.columns = ['Device Type', 'Number of Sales']
#     lead_source_counts = df['Lead Source'].value_counts().reset_index(name='Number of Leads')
#     lead_source_counts.columns = ['Lead Source', 'Number of Leads']
#     status_counts = df['Status'].value_counts().reset_index(name='Number of Leads')
#     status_counts.columns = ['Status', 'Number of Leads']
#     df['Date Lead Received'] = pd.to_datetime(df['Date Lead Received'])
#     df['Month'] = df['Date Lead Received'].dt.strftime('%B')
#     monthly_trends = df['Month'].value_counts().reset_index(name='Number of Leads')
#     monthly_trends.columns = ['Month', 'Number of Leads']
#     data = {
#         'categories': {
#             'labels': sales_by_category['Lead Category'].tolist(),
#             'values': sales_by_category['Number of Sales'].tolist()
#         },
#         'devices': {
#             'labels': sales_by_device['Device Type'].tolist(),
#             'values': sales_by_device['Number of Sales'].tolist()
#         },
#         'lead_sources': {
#             'labels': lead_source_counts['Lead Source'].tolist(),
#             'values': lead_source_counts['Number of Leads'].tolist()
#         },
#         'statuses': {
#             'labels': status_counts['Status'].tolist(),
#             'values': status_counts['Number of Leads'].tolist()
#         },
#         'months': {
#             'labels': monthly_trends['Month'].tolist(),
#             'values': monthly_trends['Number of Leads'].tolist()
#         }
#     }
#     return jsonify(data)

# # Function to calculate top 5 performers
# def top5():
#     categories = ['Lead Source', 'Brand Source', 'Lead Channel', 'Lead Category', 'Customer Name']
#     top5_data = {}
#     for category in categories:
#         top_5 = df[category].value_counts().nlargest(5).reset_index()
#         top_5.columns = [category, 'Count']
#         top5_data[category] = {
#             'labels': top_5[category].tolist(),
#             'values': top_5['Count'].tolist()
#         }
#     return jsonify(top5_data)

# # Execute all functions to populate data
# monthly_trend_data = monthly_trend()
# bars_data = bars()
# scatter_data = scatter()
# stacked_bar_data = stacked_bar()
# sales_rep_data = sales_rep()
# donuts_data = donuts()
# top5_data = top5()

# # Construct JSON response
# api_response = {
#     "monthly_trend": monthly_trend_data,
#     "bars": bars_data,
#     "scatter": scatter_data,
#     "stacked_bar": stacked_bar_data,
#     "sales_rep": sales_rep_data,
#     "donuts": donuts_data,
#     "top5": top5_data
# }


# # Example: Printing the JSON response
# import json
# print(json.dumps(api_response, indent=2))
