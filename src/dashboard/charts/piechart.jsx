import React, { useEffect, useState } from 'react';
import Plotly from 'plotly.js-dist';

function PieChart() {
  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/donuts')
      .then(response => response.json())
      .then(data => {
        const categories = data.categories;

        const chartData = [{
          values: categories.values,
          labels: categories.labels,
          domain: { x: [0, 1], y: [0, 1] },
          name: 'Lead Category',
          hoverinfo: 'label+percent+name',
          hole: .4,
          type: 'pie'
        }];

        const layout = {
          annotations: [
            {
              showarrow: false,
              text: '',
              x: 0.5,
              y: 0.5
            },
          ],
          showlegend: false,
          height: 250,
          margin: { t: 40, b: 40, l: 40, r: 20 }
        };

        Plotly.newPlot('myDiv', chartData, layout);
      });
  }, []);

  return (
    <div id="myDiv" style={{ height: '250px', width: '100%', boxShadow: '2px 2px 2px 2px rgba(0, 0, 0, 0.3)' }}></div>
  );
}

export default PieChart;
