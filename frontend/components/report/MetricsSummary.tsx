"use client";

import { TrendingUp, TrendingDown, Activity, DollarSign } from "lucide-react";

type MetricsSummaryProps = {
  medianViews?: number;
  averageViews?: number;
  engagementRate?: number;
  likeRate?: number;
  commentRate?: number;
  volatilityRatio?: number;
  riskLevel?: string;
  quotedFeeClient?: number;
  targetCpm?: number;
  clientCurrency?: string;
};

export default function MetricsSummary({
  medianViews,
  averageViews,
  engagementRate,
  likeRate,
  commentRate,
  volatilityRatio,
  riskLevel,
  quotedFeeClient,
  targetCpm,
  clientCurrency = "ZAR",
}: MetricsSummaryProps) {
  const formatNumber = (num?: number) => {
    if (num === undefined) return "—";
    return num.toLocaleString();
  };

  const formatPercent = (num?: number) => {
    if (num === undefined) return "—";
    return `${(num * 100).toFixed(2)}%`;
  };

  const formatCurrency = (num?: number) => {
    if (num === undefined) return "—";
    return `${clientCurrency} ${num.toLocaleString()}`;
  };

  // Calculate CPM if we have the data
  const calculateCPM = () => {
    if (!quotedFeeClient || !medianViews) return undefined;
    return (quotedFeeClient / (medianViews / 1000)).toFixed(2);
  };

  const effectiveCPM = calculateCPM();

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
      <div className="mb-6">
        <h3 className="text-lg font-semibold">Performance Metrics</h3>
        <p className="text-sm opacity-70 mt-1">
          Key indicators for campaign planning
        </p>
      </div>

      {/* Metrics Grid */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {/* Median Views */}
        <div
          className="rounded-xl p-4"
          style={{
            border: "1px solid var(--border)",
            background: "color-mix(in srgb, var(--muted) 40%, transparent)",
          }}
        >
          <div className="flex items-center gap-2 text-sm opacity-70 mb-2">
            <TrendingUp size={16} />
            <span>Median Views</span>
          </div>
          <div className="text-2xl font-semibold">
            {formatNumber(medianViews)}
          </div>
          <div className="mt-1 text-xs opacity-60">
            Middle value of recent videos
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
          <div className="flex items-center gap-2 text-sm opacity-70 mb-2">
            <TrendingUp size={16} />
            <span>Average Views</span>
          </div>
          <div className="text-2xl font-semibold">
            {formatNumber(averageViews)}
          </div>
          <div className="mt-1 text-xs opacity-60">
            Mean across recent videos
          </div>
        </div>

        {/* Engagement Rate */}
        <div
          className="rounded-xl p-4"
          style={{
            border: "1px solid var(--border)",
            background: "color-mix(in srgb, var(--primary) 15%, transparent)",
          }}
        >
          <div className="flex items-center gap-2 text-sm opacity-70 mb-2">
            <Activity size={16} />
            <span>Engagement Rate</span>
          </div>
          <div
            className="text-2xl font-semibold"
            style={{ color: "var(--primary)" }}
          >
            {formatPercent(engagementRate)}
          </div>
          <div className="mt-1 text-xs opacity-60">
            (Likes + Comments) / Views
          </div>
        </div>

        {/* Like Rate */}
        <div
          className="rounded-xl p-4"
          style={{
            border: "1px solid var(--border)",
            background: "color-mix(in srgb, var(--muted) 40%, transparent)",
          }}
        >
          <div className="flex items-center gap-2 text-sm opacity-70 mb-2">
            <TrendingUp size={16} />
            <span>Like Rate</span>
          </div>
          <div className="text-2xl font-semibold">
            {formatPercent(likeRate)}
          </div>
          <div className="mt-1 text-xs opacity-60">Likes / Views</div>
        </div>

        {/* Comment Rate */}
        <div
          className="rounded-xl p-4"
          style={{
            border: "1px solid var(--border)",
            background: "color-mix(in srgb, var(--muted) 40%, transparent)",
          }}
        >
          <div className="flex items-center gap-2 text-sm opacity-70 mb-2">
            <Activity size={16} />
            <span>Comment Rate</span>
          </div>
          <div className="text-2xl font-semibold">
            {formatPercent(commentRate)}
          </div>
          <div className="mt-1 text-xs opacity-60">Comments / Views</div>
        </div>

        {/* Volatility */}
        <div
          className="rounded-xl p-4"
          style={{
            border: "1px solid var(--border)",
            background: "color-mix(in srgb, var(--muted) 40%, transparent)",
          }}
        >
          <div className="flex items-center gap-2 text-sm opacity-70 mb-2">
            <TrendingDown size={16} />
            <span>Volatility Ratio</span>
          </div>
          <div className="text-2xl font-semibold">
            {volatilityRatio !== undefined
              ? volatilityRatio.toFixed(2)
              : "—"}
          </div>
          <div className="mt-1 text-xs opacity-60">
            View consistency indicator
          </div>
        </div>
      </div>

      {/* Risk Level */}
      {riskLevel && (
        <div
          className="mt-4 rounded-xl p-4"
          style={{
            border: `1px solid ${getRiskColor(riskLevel)}`,
            background: `color-mix(in srgb, ${getRiskColor(riskLevel)} 15%, transparent)`,
          }}
        >
          <div className="flex items-center justify-between">
            <div>
              <div className="text-sm font-medium">Risk Assessment</div>
              <div className="mt-1 text-xs opacity-70">
                Based on volatility and consistency
              </div>
            </div>
            <div
              className="rounded-full px-4 py-2 text-sm font-semibold"
              style={{
                background: getRiskColor(riskLevel),
                color: "#0E1114",
              }}
            >
              {riskLevel} Risk
            </div>
          </div>
        </div>
      )}

      {/* CPM Analysis */}
      {(effectiveCPM || targetCpm) && (
        <div
          className="mt-4 rounded-xl p-4"
          style={{
            border: "1px solid var(--border)",
            background: "color-mix(in srgb, var(--primary) 10%, transparent)",
          }}
        >
          <div className="flex items-center gap-2 text-sm font-medium mb-3">
            <DollarSign size={16} style={{ color: "var(--primary)" }} />
            <span>CPM Analysis</span>
          </div>

          <div className="grid gap-3 sm:grid-cols-2">
            {effectiveCPM && (
              <div>
                <div className="text-xs opacity-70">Effective CPM</div>
                <div
                  className="text-xl font-semibold mt-1"
                  style={{ color: "var(--primary)" }}
                >
                  {clientCurrency} {effectiveCPM}
                </div>
                <div className="text-xs opacity-60 mt-1">
                  Based on quoted fee: {formatCurrency(quotedFeeClient)}
                </div>
              </div>
            )}

            {targetCpm && (
              <div>
                <div className="text-xs opacity-70">Target CPM</div>
                <div className="text-xl font-semibold mt-1">
                  {formatCurrency(targetCpm)}
                </div>
                {effectiveCPM && (
                  <div className="text-xs opacity-60 mt-1">
                    {Number(effectiveCPM) <= targetCpm
                      ? "✓ Within target"
                      : "⚠ Above target"}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
