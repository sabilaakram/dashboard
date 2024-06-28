import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Plotly from 'plotly.js-dist';

function LineChart() {
  const [monthlyTrendData, setMonthlyTrendData] = useState({});

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/api/monthlytrend')
      .then(response => {
        console.log('API Response:', response.data);
        setMonthlyTrendData(response.data);
      })
      .catch(error => {
        console.error('There was an error fetching the data!', error);
      });
  }, []);

  useEffect(() => {
    if (monthlyTrendData.labels && monthlyTrendData.values) {
      const trace1 = {
        x: monthlyTrendData.labels,
        y: monthlyTrendData.values,
        type: 'scatter',
        mode: 'lines+markers',
        marker: { color: 'blue' },
      };

      const data = [trace1];

      const layout = {
        
        xaxis: {
          title: {
            text: 'Month',
            font: { size: 10 }
          },
          tickfont: {
            size: 8  // Decrease the font size of the dates on the x-axis
          }

        },
        yaxis: {
          title: {
            text: 'Number of Trends',
            font: { size: 10 }
          },
          tickfont: {
            size: 8  // Decrease the font size of the dates on the x-axis
          }

        },
        height: 250,
        margin: { t: 40, b: 40, l: 40, r: 20 }
      };

      Plotly.newPlot('line-chart', data, layout);
    }
  }, [monthlyTrendData]);

  return (
    <div id="line-chart" style={{ height: '250px', width: '100%', boxShadow: '2px 2px 2px 2px rgba(0, 0, 0, 0.3)' }}>
      {/* Plotly will render the chart here */}
    </div>
  );
}

export default LineChart;
