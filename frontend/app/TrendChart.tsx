"use client";
import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

// --- ФИНАЛЬНЫЙ ПАТЧ ---
// Глушим console.warn, так как Recharts использует именно его для этого сообщения
const originalWarn = console.warn;
const originalError = console.error;

console.warn = (...args) => {
  // Если сообщение содержит текст про ширину - игнорируем его
  if (args[0] && typeof args[0] === 'string' && args[0].includes('width(-1)')) return;
  originalWarn(...args);
};

console.error = (...args) => {
  if (args[0] && typeof args[0] === 'string' && args[0].includes('width(-1)')) return;
  originalError(...args);
};
// ----------------------

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

interface ChartProps {
  data: any[];
}

const TrendChart = ({ data }: ChartProps) => {
  if (!data || data.length === 0) return null;

  const keys = Object.keys(data[0]).filter(key => key !== 'date');

  return (
    <div style={{ width: '100%', height: 400 }}>
      {/* Добавляем minWidth={0}, это официальная рекомендация, чтобы снизить шанс появления ошибки */}
      <ResponsiveContainer width="100%" height="100%" minWidth={0}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis dataKey="date" stroke="#94a3b8" tick={{ fontSize: 12 }} />
          <YAxis stroke="#94a3b8" />
          <Tooltip
            contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', color: '#fff' }}
            itemStyle={{ color: '#fff' }}
          />
          <Legend />
          {keys.map((key, index) => (
            <Line
              key={key}
              type="monotone"
              dataKey={key}
              stroke={COLORS[index % COLORS.length]}
              strokeWidth={3}
              dot={false}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default TrendChart;