import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Plotly from 'plotly.js-dist';

function Top5BarChart() {
  const [top5Data, setTop5Data] = useState({
    'Lead Source': { labels: [], values: [] },
    'Brand Source': { labels: [], values: [] },
    'Lead Category': { labels: [], values: [] },
    'Customer Name': { labels: [], values: [] }
  });
  const [selectedCategory, setSelectedCategory] = useState('Lead Source');

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/api/top5')
      .then(response => {
        setTop5Data(response.data);
      })
      .catch(error => {
        console.error('There was an error fetching the data!', error);
      });
  }, []);

  useEffect(() => {
    if (top5Data[selectedCategory].labels.length > 0) {
      const data = [{
        x: top5Data[selectedCategory].labels,
        y: top5Data[selectedCategory].values,
        type: 'bar',
        marker: { color: 'rgba(100,200,102,0.7)' }
      }];

      const layout = {
        title: {
          text: `Top 5 ${selectedCategory}`,
          font: { size: 16, weight: 'bold' },
          xref: 'paper',
          x: 0.05
        },
        xaxis: { title: { text: selectedCategory, font: { size: 10 } }, tickfont: { size: 8 } },
        yaxis: { title: { text: 'Count', font: { size: 10 } }, tickfont: { size: 8 }, range: [0, Math.max(...top5Data[selectedCategory].values) ] },
        height: 200,
        margin: { t: 40, b: 40, l: 40, r: 20 }
      };

      Plotly.newPlot('chart', data, layout);
    }
  }, [top5Data, selectedCategory]);

  const handleCategoryChange = (event) => {
    setSelectedCategory(event.target.value);
  };

  return (
    <div>
    <div style={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'center', marginBottom: '20px' }}>
      <select onChange={handleCategoryChange} value={selectedCategory} style={{ marginRight: '20px', padding: '5px', fontSize: '14px' }}>
        <option value="Lead Source">Lead Source</option>
        <option value="Brand Source">Brand Source</option>
        <option value="Lead Category">Lead Category</option>
        <option value="Customer Name">Customer Name</option>
      </select>
    </div>
    <div id="chart" style={{ height: '200px', width: '100%', boxShadow: '2px 2px 2px 2px rgba(0, 0, 0, 0.3)' }}></div>
    </div>
  );
}

export default Top5BarChart;
