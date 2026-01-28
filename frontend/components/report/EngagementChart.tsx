"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
  Cell,
} from "recharts";

type Video = {
  title: string;
  publishedAt: string;
  views: number;
  likes: number;
  comments: number;
};

type EngagementChartProps = {
  videos: Video[];
};

export default function EngagementChart({ videos }: EngagementChartProps) {
  // Calculate engagement rate for each video
  const chartData = videos
    .map((video, index) => {
      const engagementRate =
        video.views > 0
          ? ((video.likes + video.comments) / video.views) * 100
          : 0;

      return {
        name: `Video ${videos.length - index}`,
        engagementRate: Number(engagementRate.toFixed(2)),
        likes: video.likes,
        comments: video.comments,
        views: video.views,
        title: video.title,
        date: new Date(video.publishedAt).toLocaleDateString(),
      };
    })
    .reverse();

  // Calculate average engagement
  const avgEngagement =
    chartData.reduce((sum, item) => sum + item.engagementRate, 0) /
    chartData.length;

  // Color based on engagement rate
  const getColor = (rate: number) => {
    if (rate >= avgEngagement) return "var(--primary)";
    return "rgba(126,143,201,0.5)";
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
            Engagement: {data.engagementRate}%
          </div>
          <div className="text-xs opacity-70">
            Likes: {data.likes.toLocaleString()}
          </div>
          <div className="text-xs opacity-70">
            Comments: {data.comments.toLocaleString()}
          </div>
          <div className="text-xs opacity-70">
            Views: {data.views.toLocaleString()}
          </div>
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
      <div className="mb-6">
        <h3 className="text-lg font-semibold">Engagement Analysis</h3>
        <p className="text-sm opacity-70 mt-1">
          Engagement rate = (Likes + Comments) / Views × 100
        </p>
        <div className="mt-3 flex items-center gap-4 text-sm">
          <div>
            <span className="opacity-70">Average: </span>
            <span className="font-semibold" style={{ color: "var(--primary)" }}>
              {avgEngagement.toFixed(2)}%
            </span>
          </div>
          <div className="opacity-60">
            • Higher bars indicate better engagement
          </div>
        </div>
      </div>

      {/* Chart */}
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData}>
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
              label={{
                value: "Engagement Rate (%)",
                angle: -90,
                position: "insideLeft",
                style: { fontSize: "12px", fill: "rgba(255,255,255,0.7)" },
              }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="engagementRate" radius={[8, 8, 0, 0]}>
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={getColor(entry.engagementRate)} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
