"use client";

import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import { useState } from "react";

type Video = {
  title: string;
  publishedAt: string;
  views: number;
  likes: number;
  comments: number;
};

type ViewsChartProps = {
  videos: Video[];
  medianViews?: number;
  averageViews?: number;
};

export default function ViewsChart({
  videos,
  medianViews,
  averageViews,
}: ViewsChartProps) {
  const [chartType, setChartType] = useState<"line" | "bar">("bar");

  // Prepare data for chart
  const chartData = videos
    .map((video, index) => ({
      name: `Video ${videos.length - index}`,
      views: video.views,
      title: video.title,
      date: new Date(video.publishedAt).toLocaleDateString(),
    }))
    .reverse();

  // Add median and average lines data
  const enrichedData = chartData.map((item) => ({
    ...item,
    median: medianViews,
    average: averageViews,
  }));

  const formatYAxis = (value: number) => {
    if (value >= 1000000) return `${(value / 1000000).toFixed(1)}M`;
    if (value >= 1000) return `${(value / 1000).toFixed(0)}K`;
    return value.toString();
  };

  const CustomTooltip = ({ active, payload }: any) => {
    if (!active || !payload || !payload.length) return null;

    const data = payload[0].payload;

    return (
      <div
        className="rounded-lg p-3 text-sm"
        style={{
          background: "var(--bg)",
          border: "1px solid var(--border)",
          boxShadow: "0 4px 12px rgba(0,0,0,0.3)",
        }}
      >
        <div className="font-medium">{data.name}</div>
        <div className="mt-1 text-xs opacity-70">{data.date}</div>
        <div className="mt-2 space-y-1">
          <div style={{ color: "var(--primary)" }}>
            Views: {data.views.toLocaleString()}
          </div>
          {medianViews && (
            <div className="text-xs opacity-70">
              Median: {medianViews.toLocaleString()}
            </div>
          )}
          {averageViews && (
            <div className="text-xs opacity-70">
              Average: {averageViews.toLocaleString()}
            </div>
          )}
        </div>
        <div className="mt-2 text-xs opacity-60 max-w-xs truncate">
          {data.title}
        </div>
      </div>
    );
  };

  return (
    <div
      className="rounded-2xl p-6"
      style={{
        border: "1px solid var(--border)",
        background: "rgba(255,255,255,0.04)",
        backdropFilter: "blur(10px)",
      }}
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-lg font-semibold">Video Performance</h3>
          <p className="text-sm opacity-70 mt-1">
            Views across recent uploads
          </p>
        </div>

        {/* Chart Type Toggle */}
        <div
          className="flex gap-1 rounded-lg p-1"
          style={{
            border: "1px solid var(--border)",
            background: "color-mix(in srgb, var(--muted) 50%, transparent)",
          }}
        >
          <button
            onClick={() => setChartType("bar")}
            className={`rounded-md px-3 py-1 text-xs transition ${
              chartType === "bar" ? "font-medium" : "opacity-70"
            }`}
            style={{
              background:
                chartType === "bar"
                  ? "var(--primary)"
                  : "transparent",
              color: chartType === "bar" ? "#0E1114" : "inherit",
            }}
          >
            Bar
          </button>
          <button
            onClick={() => setChartType("line")}
            className={`rounded-md px-3 py-1 text-xs transition ${
              chartType === "line" ? "font-medium" : "opacity-70"
            }`}
            style={{
              background:
                chartType === "line"
                  ? "var(--primary)"
                  : "transparent",
              color: chartType === "line" ? "#0E1114" : "inherit",
            }}
          >
            Line
          </button>
        </div>
      </div>

      {/* Chart */}
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          {chartType === "bar" ? (
            <BarChart data={enrichedData}>
              <CartesianGrid
                strokeDasharray="3 3"
                stroke="rgba(255,255,255,0.1)"
              />
              <XAxis
                dataKey="name"
                stroke="rgba(255,255,255,0.5)"
                style={{ fontSize: "12px" }}
              />
              <YAxis
                stroke="rgba(255,255,255,0.5)"
                style={{ fontSize: "12px" }}
                tickFormatter={formatYAxis}
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend
                wrapperStyle={{ fontSize: "12px", paddingTop: "20px" }}
              />
              <Bar
                dataKey="views"
                fill="var(--primary)"
                radius={[8, 8, 0, 0]}
              />
              {medianViews && (
                <Line
                  type="monotone"
                  dataKey="median"
                  stroke="#10b981"
                  strokeWidth={2}
                  strokeDasharray="5 5"
                  dot={false}
                  name="Median"
                />
              )}
              {averageViews && (
                <Line
                  type="monotone"
                  dataKey="average"
                  stroke="#f59e0b"
                  strokeWidth={2}
                  strokeDasharray="5 5"
                  dot={false}
                  name="Average"
                />
              )}
            </BarChart>
          ) : (
            <LineChart data={enrichedData}>
              <CartesianGrid
                strokeDasharray="3 3"
                stroke="rgba(255,255,255,0.1)"
              />
              <XAxis
                dataKey="name"
                stroke="rgba(255,255,255,0.5)"
                style={{ fontSize: "12px" }}
              />
              <YAxis
                stroke="rgba(255,255,255,0.5)"
                style={{ fontSize: "12px" }}
                tickFormatter={formatYAxis}
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend
                wrapperStyle={{ fontSize: "12px", paddingTop: "20px" }}
              />
              <Line
                type="monotone"
                dataKey="views"
                stroke="var(--primary)"
                strokeWidth={3}
                dot={{ fill: "var(--primary)", r: 4 }}
                activeDot={{ r: 6 }}
              />
              {medianViews && (
                <Line
                  type="monotone"
                  dataKey="median"
                  stroke="#10b981"
                  strokeWidth={2}
                  strokeDasharray="5 5"
                  dot={false}
                  name="Median"
                />
              )}
              {averageViews && (
                <Line
                  type="monotone"
                  dataKey="average"
                  stroke="#f59e0b"
                  strokeWidth={2}
                  strokeDasharray="5 5"
                  dot={false}
                  name="Average"
                />
              )}
            </LineChart>
          )}
        </ResponsiveContainer>
      </div>
    </div>
  );
}
