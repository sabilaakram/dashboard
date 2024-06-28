import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Plotly from 'plotly.js-dist';

function BarChartDepot() {
  const [depotData, setDepotData] = useState({
    depots: { labels: [], values: [] },
  });

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/api/depots')
      .then(response => {
        setDepotData(response.data);
      })
      .catch(error => {
        console.error('There was an error fetching the data!', error);
      });
  }, []);

  useEffect(() => {
    if (depotData.depots.labels.length > 0 && depotData.depots.values.length > 0) {
      const data = [{
        x: depotData.depots.labels,
        y: depotData.depots.values,
        type: 'bar',
        name: 'Depots'
      }];

      const layout = {
        xaxis: {
          title: {
            text: 'Depot',
            font: { size: 10 }
          }, 
          tickfont: { size: 8 }
        },
        yaxis: {
          title: {
            text: 'Number of Leads',
            font: { size: 10 }
          },
          tickfont: { size: 8 }
        },
        height: 250,
        margin: { t: 40, b: 40, l: 40, r: 20 }
      };

      Plotly.newPlot('depotchart', data, layout);
    }
  }, [depotData]);

  return (
    <div id="depotchart" style={{ width: '100%', height: '250px' , boxShadow: '2px 2px 2px 2px rgba(0, 0, 0, 0.3)'}}></div>
  );
}

export default BarChartDepot;
