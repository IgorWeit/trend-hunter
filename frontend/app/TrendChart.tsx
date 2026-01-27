"use client";
import React from 'react';
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend
} from 'recharts';

interface ChartProps { data: any[]; }

const TrendChart = ({ data }: ChartProps) => {
  if (!data || data.length === 0) return null;
  const keys = Object.keys(data[0]).filter(key => key !== 'date');
  const colors = ["#3b82f6", "#10b981", "#8b5cf6", "#f59e0b", "#ef4444"];

  return (
    <div className="h-[400px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
          <defs>
            {keys.map((key, index) => (
              <linearGradient key={key} id={`color${index}`} x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={colors[index % colors.length]} stopOpacity={0.8}/>
                <stop offset="95%" stopColor={colors[index % colors.length]} stopOpacity={0}/>
              </linearGradient>
            ))}
          </defs>
          <XAxis dataKey="date" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
          <YAxis stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
          <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', color: '#f1f5f9' }} />
          <Legend />
          {keys.map((key, index) => (
            <Area 
              key={key} type="monotone" dataKey={key} 
              stroke={colors[index % colors.length]} 
              fillOpacity={1} fill={`url(#color${index})`} 
            />
          ))}
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};
export default TrendChart;
