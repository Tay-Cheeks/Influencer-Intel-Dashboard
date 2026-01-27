import Link from "next/link";

export default function HomePage() {
  return (
    <main
      className="relative min-h-screen px-6"
      style={{ background: "var(--bg)", color: "var(--fg)" }}
    >
      <div className="mx-auto flex min-h-screen max-w-5xl flex-col items-center justify-center text-center">
        {/* Badge */}
        <div
          className="mb-4 inline-flex rounded-full px-3 py-1 text-xs"
          style={{
            background: "var(--muted)",
            border: "1px solid var(--border)",
          }}
        >
          Influencer Intel • MVP
        </div>

        {/* Headline */}
        <h1 className="max-w-3xl text-4xl font-semibold leading-tight md:text-5xl">
          YouTube creator analysis brands can actually trust.
        </h1>

        {/* Subheading */}
        <p className="mt-4 max-w-2xl text-sm opacity-80">
          Paste a YouTube channel or video link and get a clear, structured
          report — median vs average views, engagement quality, risk signals,
          and campaign costing in one place.
        </p>

        {/* CTAs */}
        <div className="mt-8 flex flex-wrap justify-center gap-3">
          <Link
            href="/app/analyse"
            className="rounded-md px-5 py-2 text-sm font-medium transition"
            style={{ background: "var(--primary)", color: "#0E1114" }}
          >
            Open the app
          </Link>

          <Link
            href="/pricing"
            className="rounded-md px-5 py-2 text-sm transition"
            style={{
              background: "var(--muted)",
              border: "1px solid var(--border)",
            }}
          >
            View plans
          </Link>

          <Link
            href="/tutorial"
            className="rounded-md px-5 py-2 text-sm transition"
            style={{
              background: "transparent",
              border: "1px solid var(--border)",
            }}
          >
            View tutorial
          </Link>
        </div>

        {/* Feature cards */}
        <section className="mt-16 grid w-full gap-4 md:grid-cols-3">
          {[
            {
              title: "Performance snapshot",
              desc: "Median vs mean views, engagement rate, consistency, and risk signals.",
            },
            {
              title: "Recent video breakdown",
              desc: "See how the last uploads actually performed, not inflated averages.",
            },
            {
              title: "Campaign costing",
              desc: "CPM estimates, fee comparisons, margins, and live currency conversion.",
            },
          ].map((c) => (
            <div
              key={c.title}
              className="rounded-xl p-5 text-left"
              style={{
                background: "var(--card)",
                border: "1px solid var(--border)",
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
