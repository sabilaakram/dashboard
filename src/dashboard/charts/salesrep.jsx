import React, { useEffect, useState } from "react";
import axios from "axios";
import Plotly from "plotly.js-dist";

function SalesRepBarChart() {
  const [salesRepData, setSalesRepData] = useState({
    sales_reps: [],
    values: [],
  });

  useEffect(() => {
    axios
      .get("http://127.0.0.1:5000/api/salesrep")
      .then((response) => {
        setSalesRepData(response.data);
      })
      .catch((error) => {
        console.error("There was an error fetching the data!", error);
      });
  }, []);

  useEffect(() => {
    if (salesRepData.sales_reps.length > 0 && salesRepData.values.length > 0) {
      const data = [
        {
          x: salesRepData.sales_reps,
          y: salesRepData.values,
          type: "bar",
          marker: { color: "rgba(100,200,102,0.7)" },
        },
      ];

      const layout = {
        xaxis: {title: { text: "Sales Representative", font: { size:   10 }}, tickfont: { size: 8 }}, 
        yaxis: {
          title:{ text: "Number of Sales", font: { size: 10 }},
          tickfont: {
            size: 8,
          },
          range: [0, Math.max(...salesRepData.values) + 10],
          dtick: 200,
        },
        height: 250,
        margin: { t: 40, b: 40, l: 40, r: 20 }
      };

      Plotly.newPlot("salesrepchart", data, layout);
    }
  }, [salesRepData]);

  return (
    <div
      id="salesrepchart"
      style={{
        height: "250px",
        boxShadow: "2px 2px 2px 2px rgba(0, 0, 0, 0.3)",
      }}
    ></div>
  );
}

export default SalesRepBarChart;
