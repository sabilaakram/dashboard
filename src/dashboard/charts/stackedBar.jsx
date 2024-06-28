import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Plotly from 'plotly.js-dist';

function BarChartStacked() {
  const [stackedBarData, setStackedBarData] = useState({
    months: [],
    devices: [],
    values: []
  });

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/api/stackedbar')
      .then(response => {
        setStackedBarData(response.data);
      })
      .catch(error => {
        console.error('There was an error fetching the data!', error);
      });
  }, []);

  useEffect(() => {
    if (stackedBarData.months.length > 0 && stackedBarData.devices.length > 0) {
      const { months, devices, values } = stackedBarData;
      const uniqueDevices = [...new Set(devices)];
      const colorPalette = [
        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#B0E57C',
        '#FF5733', '#33FF57', '#3357FF'
      ];

      const data = uniqueDevices.map((device, index) => ({
        x: months.filter((_, i) => devices[i] === device),
        y: values.filter((_, i) => devices[i] === device),
        type: 'bar',
        name: device,
        marker: { color: colorPalette[index % colorPalette.length] }
      }));

      const layout = {
        barmode: 'stack',
        xaxis: {
          title: { text: 'Month', font: { size: 10 } },
          tickfont: { size: 8 }
        },
        yaxis: {
          title: { text: 'Number of Sales', font: { size: 10 } },
          tickfont: { size: 8 },
          range: [0, 800],
          dtick: 200
        },
        legend: {
          font: { size: 8 }
        },
        height: 250,
        margin: { t: 40, b: 40, l: 40, r: 20 }
      };

      Plotly.newPlot('chartStacked', data, layout);
    }
  }, [stackedBarData]);

  return (
    <div id="chartStacked" style={{ height: '250px', width: "100%", boxShadow: '2px 2px 2px 2px rgba(0, 0, 0, 0.3)' }}></div>
  );
}

export default BarChartStacked;
