"use client";

import { Users, MapPin, TrendingUp, AlertCircle } from "lucide-react";

type ChannelCardProps = {
  channelName: string;
  channelUrl?: string;
  subscribers?: number;
  region?: string;
  medianViews?: number;
  averageViews?: number;
  engagementRate?: number;
  riskLevel?: string;
};

export default function ChannelCard({
  channelName,
  channelUrl,
  subscribers,
  region,
  medianViews,
  averageViews,
  engagementRate,
  riskLevel,
}: ChannelCardProps) {
  const formatNumber = (num?: number) => {
    if (num === undefined) return "—";
    return num.toLocaleString();
  };

  const getRiskColor = (risk?: string) => {
    if (!risk) return "var(--muted)";
    const r = risk.toLowerCase();
    if (r.includes("low")) return "#10b981";
    if (r.includes("medium")) return "#f59e0b";
    if (r.includes("high")) return "#ef4444";
    return "var(--muted)";
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
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0 flex-1">
          <h2 className="text-2xl font-semibold truncate">{channelName}</h2>
          {channelUrl && (
            <a
              href={channelUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="mt-1 text-sm opacity-70 hover:opacity-100 transition inline-block"
              style={{ color: "var(--primary)" }}
            >
              View on YouTube →
            </a>
          )}
        </div>

        {riskLevel && (
          <div
            className="rounded-full px-3 py-1 text-xs font-medium"
            style={{
              background: `color-mix(in srgb, ${getRiskColor(riskLevel)} 20%, transparent)`,
              color: getRiskColor(riskLevel),
              border: `1px solid ${getRiskColor(riskLevel)}`,
            }}
          >
            {riskLevel} Risk
          </div>
        )}
      </div>

      {/* Stats Grid */}
      <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {/* Subscribers */}
        <div
          className="rounded-xl p-4"
          style={{
            border: "1px solid var(--border)",
            background: "color-mix(in srgb, var(--muted) 40%, transparent)",
          }}
        >
          <div className="flex items-center gap-2 text-sm opacity-70">
            <Users size={16} />
            <span>Subscribers</span>
          </div>
          <div className="mt-2 text-2xl font-semibold">
            {formatNumber(subscribers)}
          </div>
        </div>

        {/* Region */}
        <div
          className="rounded-xl p-4"
          style={{
            border: "1px solid var(--border)",
            background: "color-mix(in srgb, var(--muted) 40%, transparent)",
          }}
        >
          <div className="flex items-center gap-2 text-sm opacity-70">
            <MapPin size={16} />
            <span>Region</span>
          </div>
          <div className="mt-2 text-2xl font-semibold">
            {region || "Global"}
          </div>
        </div>

        {/* Median Views */}
        <div
          className="rounded-xl p-4"
          style={{
            border: "1px solid var(--border)",
            background: "color-mix(in srgb, var(--muted) 40%, transparent)",
          }}
        >
          <div className="flex items-center gap-2 text-sm opacity-70">
            <TrendingUp size={16} />
            <span>Median Views</span>
          </div>
          <div className="mt-2 text-2xl font-semibold">
            {formatNumber(medianViews)}
          </div>
        </div>

        {/* Average Views */}
        <div
          className="rounded-xl p-4"
          style={{
            border: "1px solid var(--border)",
            background: "color-mix(in srgb, var(--muted) 40%, transparent)",
          }}
        >
          <div className="flex items-center gap-2 text-sm opacity-70">
            <TrendingUp size={16} />
            <span>Average Views</span>
          </div>
          <div className="mt-2 text-2xl font-semibold">
            {formatNumber(averageViews)}
          </div>
        </div>
      </div>

      {/* Engagement Rate */}
      {engagementRate !== undefined && (
        <div
          className="mt-4 rounded-xl p-4"
          style={{
            border: "1px solid var(--border)",
            background: "color-mix(in srgb, var(--primary) 10%, transparent)",
          }}
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <AlertCircle size={16} style={{ color: "var(--primary)" }} />
              <span className="text-sm font-medium">Engagement Rate</span>
            </div>
            <div className="text-xl font-semibold" style={{ color: "var(--primary)" }}>
              {(engagementRate * 100).toFixed(2)}%
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
