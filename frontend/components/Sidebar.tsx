"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useTheme } from "next-themes";
import { useEffect, useState } from "react";

const nav = [
  { href: "/analyse", label: "Analyse" },
  { href: "/saved", label: "Saved" },
  { href: "/pricing", label: "Pricing" },
];

function cn(...classes: Array<string | false | undefined>) {
  return classes.filter(Boolean).join(" ");
}

export default function Sidebar() {
  const pathname = usePathname();
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <aside
      className="h-screen w-64 border-r p-4"
      style={{
        background: "var(--bg)",
        borderColor: "var(--border)",
      }}
    >
      {/* Header */}
      <div className="mb-8 flex items-center justify-between">
        <div>
          <div className="text-lg font-semibold">Influencer Intel</div>
          <div className="text-xs opacity-70">MVP</div>
        </div>

        <button
          type="button"
          aria-label="Toggle theme"
          disabled={!mounted}
          onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
          className="rounded-md px-2 py-1 text-xs transition"
          style={{
            background: "var(--muted)",
            border: "1px solid var(--border)",
          }}
        >
          {mounted ? (theme === "dark" ? "Light" : "Dark") : "Theme"}
        </button>
      </div>

      {/* Navigation */}
      <nav className="space-y-1">
        {nav.map((item) => {
          const active = pathname === item.href;

          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "block rounded-md px-3 py-2 text-sm transition-colors",
              )}
              style={{
                background: active ? "var(--muted)" : "transparent",
                color: active ? "var(--fg)" : "var(--secondary)",
                fontWeight: active ? 500 : 400,
              }}
            >
              {item.label}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
