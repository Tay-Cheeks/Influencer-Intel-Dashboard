"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import { useTheme } from "next-themes";
import { useAnalysis } from "@/context/AnalysisContext";
import { useSession, signOut } from "next-auth/react";
import { LogOut, User } from "lucide-react";

const nav = [
  { href: "/app/analyse", label: "Analyse" },
  { href: "/app/saved", label: "Saved" },
  { href: "/app/calculator", label: "Calculator" },
];

function cn(...classes: Array<string | false | undefined>) {
  return classes.filter(Boolean).join(" ");
}

function ThemeToggle() {
  const { theme, setTheme, resolvedTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => setMounted(true), []);

  // Avoid hydration mismatch: render a stable placeholder on SSR
  const current = mounted
    ? theme === "system"
      ? resolvedTheme
      : theme
    : "light";

  return (
    <button
      type="button"
      onClick={() => {
        const next = current === "dark" ? "light" : "dark";
        setTheme(next);
      }}
      className="rounded-md px-2 py-1 text-xs transition hover:opacity-90"
      style={{
        border: "1px solid var(--border)",
        background: "color-mix(in srgb, var(--muted) 78%, transparent)",
        backdropFilter: "blur(10px)",
      }}
      aria-label="Toggle theme"
      title="Toggle theme"
      suppressHydrationWarning
    >
      {mounted ? (current === "dark" ? "Dark" : "Light") : "Theme"}
    </button>
  );
}

export default function Sidebar() {
  const pathname = usePathname();
  const [collapsed, setCollapsed] = useState(false);

  const { state, setActive } = useAnalysis();

  // Persist collapse state
  useEffect(() => {
    const saved = localStorage.getItem("ii.sidebar.collapsed");
    if (saved === "1") setCollapsed(true);
  }, []);

  useEffect(() => {
    localStorage.setItem("ii.sidebar.collapsed", collapsed ? "1" : "0");
  }, [collapsed]);

  const widthClass = collapsed ? "w-[72px]" : "w-64";

  const recent = useMemo(() => {
    return state.recentIds.map((id) => state.byId[id]).filter(Boolean);
  }, [state.recentIds, state.byId]);

  const activeAnalysis = state.activeId ? state.byId[state.activeId] : null;

  return (
    <aside
      className={cn(
        "h-screen shrink-0 border-r p-3 md:p-4 transition-[width] duration-200 flex flex-col",
        widthClass,
      )}
      style={{ background: "var(--bg)", borderColor: "var(--border)" }}
    >
      {/* Header */}
      <div
        className={cn(
          "mb-4 flex items-center justify-between gap-2 rounded-xl p-2",
          collapsed ? "px-2" : "px-3",
        )}
        style={{
          background: "color-mix(in srgb, var(--muted) 65%, transparent)",
          border:
            "1px solid color-mix(in srgb, var(--border) 75%, transparent)",
          backdropFilter: "blur(12px)",
        }}
      >
        <div className={cn("min-w-0", collapsed && "hidden")}>
          <div className="text-sm font-semibold leading-none">
            Influencer Intel
          </div>
          <div className="mt-1 text-[11px] opacity-70">MVP</div>
        </div>

        <div className="flex items-center gap-2">
          {/* Theme toggle */}
          {!collapsed && <ThemeToggle />}

          {/* Collapse toggle */}
          <button
            type="button"
            onClick={() => setCollapsed((v) => !v)}
            className="rounded-md px-2 py-1 text-xs transition hover:opacity-90"
            style={{
              border: "1px solid var(--border)",
              background: "transparent",
            }}
            aria-label="Toggle sidebar"
            title="Toggle sidebar"
          >
            {collapsed ? "→" : "←"}
          </button>
        </div>
      </div>

      {/* Active analysis chip */}
      {!collapsed && (
        <div
          className="mb-4 rounded-xl p-3 text-xs"
          style={{
            border:
              "1px solid color-mix(in srgb, var(--border) 70%, transparent)",
            background: "color-mix(in srgb, var(--muted) 55%, transparent)",
            backdropFilter: "blur(12px)",
          }}
        >
          <div className="opacity-70">Active analysis</div>
          <div className="mt-1 font-medium">
            {activeAnalysis?.channelName ?? "None yet"}
          </div>
          <div className="mt-1 opacity-70">
            {activeAnalysis?.region ? `${activeAnalysis.region} • ` : ""}
            {activeAnalysis?.subscribers
              ? `${activeAnalysis.subscribers.toLocaleString()} subs`
              : "Run an analysis to begin"}
          </div>
        </div>
      )}

      {/* Nav */}
      <nav className="space-y-1">
        {nav.map((item) => {
          const active = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-2 rounded-lg px-3 py-2 text-sm transition",
                active ? "font-medium" : "opacity-80 hover:opacity-100",
                collapsed && "justify-center px-2",
              )}
              style={{
                background: active
                  ? "color-mix(in srgb, var(--muted) 78%, transparent)"
                  : "transparent",
                border: active
                  ? "1px solid var(--border)"
                  : "1px solid transparent",
              }}
            >
              <span className={cn(collapsed && "hidden")}>{item.label}</span>
              {collapsed && (
                <span className="text-[11px]">{item.label[0]}</span>
              )}
            </Link>
          );
        })}
      </nav>

      {/* Recent analyses */}
      <div className="mt-4">
        {!collapsed && (
          <div className="mb-2 px-1 text-xs font-medium opacity-80">
            Recent analyses
          </div>
        )}

        <div className="space-y-1">
          {recent.length === 0 ? (
            <div
              className={cn(
                "rounded-lg p-3 text-xs opacity-70",
                collapsed && "hidden",
              )}
              style={{
                border: "1px solid transparent",
                background: "transparent",
              }}
            >
              No recent analyses yet.
            </div>
          ) : (
            recent.map((a) => {
              const isActive = a.id === state.activeId;

              return (
                <button
                  key={a.id}
                  type="button"
                  onClick={() => setActive(a.id)}
                  className={cn(
                    "w-full rounded-lg px-3 py-2 text-left text-xs transition",
                    collapsed && "px-2 flex justify-center",
                  )}
                  style={{
                    background: isActive
                      ? "color-mix(in srgb, var(--muted) 78%, transparent)"
                      : "transparent",
                    border: isActive
                      ? "1px solid var(--border)"
                      : "1px solid transparent",
                    opacity: isActive ? 1 : 0.85,
                  }}
                  title={a.channelName}
                >
                  {collapsed ? (
                    <span className="text-[11px]">•</span>
                  ) : (
                    <div className="flex items-center justify-between gap-2">
                      <div className="min-w-0">
                        <div className="truncate font-medium">
                          {a.channelName}
                        </div>
                        <div className="truncate opacity-70">
                          {a.region ?? "Global"}{" "}
                          {typeof a.medianViews === "number"
                            ? `• med ${a.medianViews.toLocaleString()}`
                            : ""}
                        </div>
                      </div>
                      <div className="shrink-0 opacity-60">
                        {isActive ? "Active" : ""}
                      </div>
                    </div>
                  )}
                </button>
              );
            })
          )}
        </div>
      </div>

      {/* Footer */}
      <div className="mt-auto pt-4 space-y-3">
        {/* User Info */}
        {!collapsed && (
          <div
            className="rounded-xl p-3 text-xs"
            style={{
              border:
                "1px solid color-mix(in srgb, var(--border) 70%, transparent)",
              background: "color-mix(in srgb, var(--muted) 55%, transparent)",
              backdropFilter: "blur(12px)",
            }}
          >
            <div className="flex items-center gap-2 mb-2">
              <User size={14} className="opacity-70" />
              <span className="font-medium opacity-80">
                {useSession().data?.user?.name || "User"}
              </span>
            </div>
            <div className="opacity-60 truncate">
              {useSession().data?.user?.email || ""}
            </div>
          </div>
        )}

        {/* Logout Button */}
        <button
          onClick={() => signOut({ callbackUrl: "/" })}
          className={cn(
            "w-full rounded-xl px-3 py-2 text-xs transition hover:opacity-90",
            collapsed && "px-2",
          )}
          style={{
            border: "1px solid var(--border)",
            background: "color-mix(in srgb, var(--muted) 55%, transparent)",
          }}
        >
          <div className="flex items-center gap-2 justify-center">
            <LogOut size={14} />
            {!collapsed && <span>Sign out</span>}
          </div>
        </button>

        {!collapsed && (
          <div
            className="rounded-xl p-3 text-xs opacity-70"
            style={{
              border:
                "1px solid color-mix(in srgb, var(--border) 70%, transparent)",
              background: "color-mix(in srgb, var(--muted) 55%, transparent)",
              backdropFilter: "blur(12px)",
            }}
          >
            Public pages: Home / Pricing / Tutorial <br />
            App pages: /app/*
          </div>
        )}
      </div>
    </aside>
  );
}
