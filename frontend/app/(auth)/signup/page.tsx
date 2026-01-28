"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import LiquidEtherBackground from "@/components/LiquidEtherBackground";

export default function SignupPage() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const res = await fetch("/api/auth/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password }),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.error || "Something went wrong");
        setLoading(false);
        return;
      }

      // Redirect to login after successful signup
      router.push("/login?registered=true");
    } catch (err) {
      setError("Something went wrong. Please try again.");
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
            <h1 className="text-2xl font-semibold">Create your account</h1>
            <p className="text-sm opacity-70 mt-2">
              Start analysing YouTube creators today
            </p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">Full Name</label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="John Doe"
                required
                className="w-full rounded-xl px-4 py-3 text-sm outline-none transition"
                style={{
                  border: "1px solid var(--border)",
                  background: "transparent",
                }}
              />
            </div>

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
              <div className="mt-1 text-xs opacity-60">
                Must be at least 6 characters
              </div>
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
              {loading ? "Creating account..." : "Create account"}
            </button>
          </form>

          {/* Footer */}
          <div className="mt-6 text-center text-sm">
            <span className="opacity-70">Already have an account? </span>
            <Link
              href="/login"
              className="font-medium transition hover:opacity-80"
              style={{ color: "var(--primary)" }}
            >
              Sign in
            </Link>
          </div>
        </div>

        {/* Terms notice */}
        <div
          className="mt-4 rounded-xl p-4 text-xs text-center opacity-70"
          style={{
            border: "1px solid var(--border)",
            background: "rgba(255,255,255,0.02)",
          }}
        >
          By creating an account, you agree to our Terms of Service and Privacy
          Policy
        </div>
      </div>
    </main>
  );
}
