"use client";

import { useState } from "react";
import { signIn } from "next-auth/react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import LiquidEtherBackground from "@/components/LiquidEtherBackground";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const result = await signIn("credentials", {
        email,
        password,
        redirect: false,
      });

      if (result?.error) {
        setError("Invalid email or password");
      } else {
        router.push("/app/analyse");
        router.refresh();
      }
    } catch (err) {
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main
      className="relative min-h-screen flex items-center justify-center px-6"
      style={{ background: "var(--bg)", color: "var(--fg)" }}
    >
      <LiquidEtherBackground />

      <div className="relative w-full max-w-md">
        {/* Back to home */}
        <Link
          href="/"
          className="absolute -top-12 left-0 text-sm opacity-70 hover:opacity-100 transition"
        >
          ← Back to home
        </Link>

        <div
          className="rounded-2xl p-8"
          style={{
            border: "1px solid var(--border)",
            background: "rgba(255,255,255,0.04)",
            backdropFilter: "blur(20px)",
          }}
        >
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-2xl font-semibold">Welcome back</h1>
            <p className="text-sm opacity-70 mt-2">
              Sign in to access your dashboard
            </p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
                required
                className="w-full rounded-xl px-4 py-3 text-sm outline-none transition"
                style={{
                  border: "1px solid var(--border)",
                  background: "transparent",
                }}
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
                minLength={6}
                className="w-full rounded-xl px-4 py-3 text-sm outline-none transition"
                style={{
                  border: "1px solid var(--border)",
                  background: "transparent",
                }}
              />
            </div>

            {error && (
              <div
                className="rounded-xl p-3 text-sm"
                style={{
                  border: "1px solid #ef4444",
                  background: "color-mix(in srgb, #ef4444 15%, transparent)",
                  color: "#ef4444",
                }}
              >
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-xl px-4 py-3 text-sm font-medium transition disabled:opacity-60"
              style={{ background: "var(--primary)", color: "#0E1114" }}
            >
              {loading ? "Signing in..." : "Sign in"}
            </button>
          </form>

          {/* Footer */}
          <div className="mt-6 text-center text-sm">
            <span className="opacity-70">Don't have an account? </span>
            <Link
              href="/signup"
              className="font-medium transition hover:opacity-80"
              style={{ color: "var(--primary)" }}
            >
              Sign up
            </Link>
          </div>
        </div>

        {/* Demo credentials */}
        <div
          className="mt-4 rounded-xl p-4 text-xs"
          style={{
            border: "1px solid var(--border)",
            background: "rgba(255,255,255,0.02)",
          }}
        >
          <div className="font-medium mb-2 opacity-80">Demo Mode</div>
          <div className="opacity-60">
            This is an MVP with in-memory storage. Create an account to test the
            flow. Data will be lost on server restart.
          </div>
        </div>
      </div>
    </main>
  );
}
