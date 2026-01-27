"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import { useTheme } from "next-themes";

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

  // Persist collapse state
  useEffect(() => {
    const saved = localStorage.getItem("ii.sidebar.collapsed");
    if (saved === "1") setCollapsed(true);
  }, []);

  useEffect(() => {
    localStorage.setItem("ii.sidebar.collapsed", collapsed ? "1" : "0");
  }, [collapsed]);

  const widthClass = collapsed ? "w-[72px]" : "w-64";

  return (
    <aside
      className={cn(
        "h-screen shrink-0 border-r p-3 md:p-4 transition-[width] duration-200",
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

      {/* Footer */}
      <div className="mt-auto pt-4">
        <div
          className={cn(
            "rounded-xl p-3 text-xs opacity-70",
            collapsed && "hidden",
          )}
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
      </div>
    </aside>
  );
}
