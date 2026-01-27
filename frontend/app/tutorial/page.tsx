import Link from "next/link";

export default function TutorialPage() {
  return (
    <main
      className="min-h-screen px-6 py-12"
      style={{ background: "var(--bg)", color: "var(--fg)" }}
    >
      <div className="mx-auto max-w-4xl space-y-8">
        {/* Header */}
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
            A short, practical demo showing how to analyse a creator and
            interpret the report. (Emma can swap the Loom link anytime.)
          </p>

          <div className="flex flex-wrap gap-3 pt-2">
            <Link
              href="/app/analyse"
              className="rounded-md px-5 py-2 text-sm font-medium transition"
              style={{ background: "var(--primary)", color: "#0E1114" }}
            >
              Open the app
            </Link>

            <Link
              href="/"
              className="rounded-md px-5 py-2 text-sm transition"
              style={{
                background: "transparent",
                border: "1px solid var(--border)",
              }}
            >
              Back to home
            </Link>
          </div>
        </div>

        {/* Video embed */}
        <section
          className="overflow-hidden rounded-2xl"
          style={{
            border: "1px solid var(--border)",
            background: "var(--card)",
          }}
        >
          <div className="p-4 md:p-5">
            <div className="text-sm font-semibold">Demo video</div>
            <div className="mt-1 text-sm opacity-70">
              Replace the embed URL below with your Loom share link.
            </div>
          </div>

          {/* Responsive 16:9 */}
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

        {/* Notes / bullets */}
        <section className="grid gap-4 md:grid-cols-3">
          {[
            {
              title: "What to paste",
              desc: "Channel URL, handle (@...), or a video URL.",
            },
            {
              title: "What to look for",
              desc: "Median vs average views tells you how consistent the channel is.",
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
