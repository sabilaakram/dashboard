import React from "react";

import BarChart from "./charts/barchart_leadsources";
import BarChartStacked from "./charts/stackedBar";
import BarChartDepot from "./charts/barchart_depot";
import PieChart from "./charts/piechart";
import Top5BarChart from "./charts/top5";
import LineChart from "./charts/linechart";
import SalesRepBarChart from "./charts/salesrep";

export default function Dashboardd() {
  return (
    <div>
      <p className="md:text-3xl sm:text-lg lg:text-4xl font-bold text-center md:pt-2 sm:p-2 lg:p-5">
        Dashboard
      </p>
      {/* <div className='flex md:flex-col lg:flex-row sm:flex-col md:gap-5'> */}
      <div className="md:flex-col lg:flex-row sm:flex-col justify-between md:pt-2 w-full">
        {/* <div className='flex md:flex-col lg:flex-row sm:flex-col md:pl-5 justify-between md:pr-5'>
          <Cards text={"$0"} subtext={"Yearly Earning"} />
          <Cards text={"$0"} subtext={"Yearly Earning"} />
          <Cards text={"$0"} subtext={"Yearly Earning"} />
          <Cards text={"$0"} subtext={"Yearly Earning"} />
        </div> */}
        <div className="">
          <div>
            <div className="grid grid-cols-[45%,25%,25%] md:gap-4 md:px-10 ">
              <div className=" h-full border shadow-2xl shadow-slate-300">
                <BarChartStacked />
              </div>
              <div className=" h-full  border shadow-2xl shadow-slate-300">
                <BarChart />
              </div>
              <div className=" h-full  border shadow-2xl shadow-slate-300">
                <PieChart />
              </div>
            </div>
            <div className="grid grid-cols-[23%,23%,23%,23%] md:gap-4 md:px-10 md:pt-5">
              <div className=" border shadow-2xl shadow-slate-300">
                <LineChart />
              </div>
              <div className=" h-full  border shadow-2xl shadow-slate-300">
                <BarChartDepot />
              </div>
              <div className=" h-full  border shadow-2xl shadow-slate-300">
                <SalesRepBarChart />
              </div>
              <div className=" h-full  border shadow-2xl shadow-slate-300">
                <Top5BarChart />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
