"use client";

import { useState, useMemo } from "react";
import { ArrowUpDown, ArrowUp, ArrowDown } from "lucide-react";

type Video = {
  title: string;
  publishedAt: string;
  views: number;
  likes: number;
  comments: number;
  duration: string;
};

type VideoTableProps = {
  videos: Video[];
};

type SortKey = "title" | "publishedAt" | "views" | "likes" | "comments" | "engagement";
type SortOrder = "asc" | "desc";

export default function VideoTable({ videos }: VideoTableProps) {
  const [sortKey, setSortKey] = useState<SortKey>("publishedAt");
  const [sortOrder, setSortOrder] = useState<SortOrder>("desc");

  const handleSort = (key: SortKey) => {
    if (sortKey === key) {
      setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    } else {
      setSortKey(key);
      setSortOrder("desc");
    }
  };

  const sortedVideos = useMemo(() => {
    const sorted = [...videos].sort((a, b) => {
      let aVal: any;
      let bVal: any;

      if (sortKey === "engagement") {
        aVal = a.views > 0 ? ((a.likes + a.comments) / a.views) * 100 : 0;
        bVal = b.views > 0 ? ((b.likes + b.comments) / b.views) * 100 : 0;
      } else if (sortKey === "publishedAt") {
        aVal = new Date(a.publishedAt).getTime();
        bVal = new Date(b.publishedAt).getTime();
      } else {
        aVal = a[sortKey];
        bVal = b[sortKey];
      }

      if (sortOrder === "asc") {
        return aVal > bVal ? 1 : -1;
      } else {
        return aVal < bVal ? 1 : -1;
      }
    });

    return sorted;
  }, [videos, sortKey, sortOrder]);

  const formatNumber = (num: number) => num.toLocaleString();

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  };

  const calculateEngagement = (video: Video) => {
    if (video.views === 0) return "0.00";
    const rate = ((video.likes + video.comments) / video.views) * 100;
    return rate.toFixed(2);
  };

  const SortIcon = ({ columnKey }: { columnKey: SortKey }) => {
    if (sortKey !== columnKey) {
      return <ArrowUpDown size={14} className="opacity-40" />;
    }
    return sortOrder === "asc" ? (
      <ArrowUp size={14} style={{ color: "var(--primary)" }} />
    ) : (
      <ArrowDown size={14} style={{ color: "var(--primary)" }} />
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
        <h3 className="text-lg font-semibold">Video Breakdown</h3>
        <p className="text-sm opacity-70 mt-1">
          Detailed metrics for each video • Click headers to sort
        </p>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr
              className="border-b"
              style={{ borderColor: "var(--border)" }}
            >
              <th className="text-left py-3 px-2 font-medium">
                <button
                  onClick={() => handleSort("title")}
                  className="flex items-center gap-2 hover:opacity-80 transition"
                >
                  Title
                  <SortIcon columnKey="title" />
                </button>
              </th>
              <th className="text-left py-3 px-2 font-medium">
                <button
                  onClick={() => handleSort("publishedAt")}
                  className="flex items-center gap-2 hover:opacity-80 transition"
                >
                  Published
                  <SortIcon columnKey="publishedAt" />
                </button>
              </th>
              <th className="text-right py-3 px-2 font-medium">
                <button
                  onClick={() => handleSort("views")}
                  className="flex items-center gap-2 ml-auto hover:opacity-80 transition"
                >
                  Views
                  <SortIcon columnKey="views" />
                </button>
              </th>
              <th className="text-right py-3 px-2 font-medium">
                <button
                  onClick={() => handleSort("likes")}
                  className="flex items-center gap-2 ml-auto hover:opacity-80 transition"
                >
                  Likes
                  <SortIcon columnKey="likes" />
                </button>
              </th>
              <th className="text-right py-3 px-2 font-medium">
                <button
                  onClick={() => handleSort("comments")}
                  className="flex items-center gap-2 ml-auto hover:opacity-80 transition"
                >
                  Comments
                  <SortIcon columnKey="comments" />
                </button>
              </th>
              <th className="text-right py-3 px-2 font-medium">
                <button
                  onClick={() => handleSort("engagement")}
                  className="flex items-center gap-2 ml-auto hover:opacity-80 transition"
                >
                  Engagement
                  <SortIcon columnKey="engagement" />
                </button>
              </th>
              <th className="text-center py-3 px-2 font-medium">Duration</th>
            </tr>
          </thead>
          <tbody>
            {sortedVideos.map((video, index) => (
              <tr
                key={index}
                className="border-b transition hover:bg-opacity-50"
                style={{
                  borderColor: "var(--border)",
                  background: index % 2 === 0 ? "transparent" : "rgba(255,255,255,0.02)",
                }}
              >
                <td className="py-3 px-2 max-w-xs">
                  <div className="truncate" title={video.title}>
                    {video.title}
                  </div>
                </td>
                <td className="py-3 px-2 opacity-70 whitespace-nowrap">
                  {formatDate(video.publishedAt)}
                </td>
                <td className="py-3 px-2 text-right font-medium">
                  {formatNumber(video.views)}
                </td>
                <td className="py-3 px-2 text-right opacity-70">
                  {formatNumber(video.likes)}
                </td>
                <td className="py-3 px-2 text-right opacity-70">
                  {formatNumber(video.comments)}
                </td>
                <td
                  className="py-3 px-2 text-right font-medium"
                  style={{ color: "var(--primary)" }}
                >
                  {calculateEngagement(video)}%
                </td>
                <td className="py-3 px-2 text-center opacity-70 text-xs">
                  {video.duration}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Summary */}
      <div
        className="mt-6 rounded-xl p-4 text-sm"
        style={{
          border: "1px solid var(--border)",
          background: "color-mix(in srgb, var(--muted) 40%, transparent)",
        }}
      >
        <div className="flex items-center justify-between flex-wrap gap-4">
          <div>
            <span className="opacity-70">Total Videos: </span>
            <span className="font-semibold">{videos.length}</span>
          </div>
          <div>
            <span className="opacity-70">Total Views: </span>
            <span className="font-semibold">
              {formatNumber(videos.reduce((sum, v) => sum + v.views, 0))}
            </span>
          </div>
          <div>
            <span className="opacity-70">Total Likes: </span>
            <span className="font-semibold">
              {formatNumber(videos.reduce((sum, v) => sum + v.likes, 0))}
            </span>
          </div>
          <div>
            <span className="opacity-70">Total Comments: </span>
            <span className="font-semibold">
              {formatNumber(videos.reduce((sum, v) => sum + v.comments, 0))}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
