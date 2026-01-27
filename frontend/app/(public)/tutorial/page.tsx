import Link from "next/link";
import LiquidEtherBackground from "@/components/LiquidEtherBackground";

export default function TutorialPage() {
  return (
    <main
      className="relative min-h-screen px-6 py-12"
      style={{ background: "var(--bg)", color: "var(--fg)" }}
    >
      <LiquidEtherBackground />

      <div className="relative mx-auto max-w-4xl space-y-8">
        <div className="flex items-center justify-between">
          <Link
            href="/"
            className="rounded-md px-3 py-1.5 text-xs transition"
            style={{
              background: "transparent",
              border: "1px solid var(--border)",
            }}
          >
            ← Back home
          </Link>

          <Link
            href="/app/analyse"
            className="rounded-md px-4 py-2 text-sm font-medium transition"
            style={{ background: "var(--primary)", color: "#0E1114" }}
          >
            Open the app
          </Link>
        </div>

        <div className="space-y-3">
          <div
            className="inline-flex rounded-full px-3 py-1 text-xs"
            style={{
              background: "var(--muted)",
              border: "1px solid var(--border)",
            }}
          >
            Tutorial
          </div>

          <h1 className="text-3xl font-semibold md:text-4xl">
            Quick walkthrough
          </h1>

          <p className="max-w-2xl text-sm opacity-80">
            A short demo showing how to analyse a creator and interpret the
            report. Emma can swap the Loom link anytime.
          </p>
        </div>

        <section
          className="overflow-hidden rounded-2xl"
          style={{
            background: "rgba(255,255,255,0.03)",
            border: "1px solid var(--border)",
            backdropFilter: "blur(10px)",
          }}
        >
          <div className="p-4 md:p-5">
            <div className="text-sm font-semibold">Demo video</div>
            <div className="mt-1 text-sm opacity-70">
              Replace the embed URL below with your Loom share link.
            </div>
          </div>

          <div className="relative aspect-video w-full">
            <iframe
              className="absolute inset-0 h-full w-full"
              src="https://www.loom.com/embed/REPLACE_ME"
              title="Influencer Intel Tutorial"
              allow="autoplay; fullscreen; picture-in-picture"
              allowFullScreen
            />
          </div>
        </section>

        <section className="grid gap-4 md:grid-cols-3">
          {[
            {
              title: "What to paste",
              desc: "Channel URL, handle (@...), or a video URL.",
            },
            {
              title: "What to look for",
              desc: "Median vs average shows consistency vs spikes.",
            },
            {
              title: "Costing",
              desc: "Use the calculator to sanity-check CPMs against the quote.",
            },
          ].map((c) => (
            <div
              key={c.title}
              className="rounded-xl p-5 text-left"
              style={{
                background: "rgba(255,255,255,0.03)",
                border: "1px solid var(--border)",
                backdropFilter: "blur(10px)",
              }}
            >
              <div className="text-sm font-semibold">{c.title}</div>
              <div className="mt-1 text-sm opacity-80">{c.desc}</div>
            </div>
          ))}
        </section>
      </div>
    </main>
  );
}
