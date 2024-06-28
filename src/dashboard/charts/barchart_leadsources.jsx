import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Plotly from 'plotly.js-dist';

function BarChart() {
  const [barData, setBarData] = useState({
    lead_sources: { labels: [], values: [] }
  });

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/api/bars')
      .then(response => {
        setBarData(response.data);
      })
      .catch(error => {
        console.error('There was an error fetching the data!', error);
      });
  }, []);

  useEffect(() => {
    if (barData.lead_sources.labels.length > 0) {
      const data = [
        {
          x: barData.lead_sources.labels,
          y: barData.lead_sources.values,
          type: 'bar'
        }
      ];

      const layout = {
        xaxis: {
          title: {text:'Lead Sources', 'font': {'size': 10}}, tickfont: { size: 8 },
          showticklabels: false  // Hide x-axis tick labels
        },
        yaxis: {
          title: {text: 'Number of Leads', 'font': {'size': 10}}, tickfont: { size: 8 }
        },
        height: 250,
        margin: { t: 40, b: 40, l: 40, r: 20 }
      };

      Plotly.newPlot('barchart', data, layout);
    }
  }, [barData]);

  return (
    <div id="barchart" style={{ height: '250px', width: '100%', boxShadow: '2px 2px 2px 2px rgba(0, 0, 0, 0.3)' }}></div>
  );
}

export default BarChart;
