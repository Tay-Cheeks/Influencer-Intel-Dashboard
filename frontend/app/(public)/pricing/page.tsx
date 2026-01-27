import Link from "next/link";
import LiquidEtherBackground from "@/components/LiquidEtherBackground";

const plans = [
  {
    name: "Starter",
    price: "R499",
    period: "/ month",
    desc: "For quick checks and small teams testing creator fit.",
    features: [
      "30 analyses / month",
      "Key metrics + charts",
      "Campaign costing",
      "Email support",
    ],
    cta: "Start Starter",
  },
  {
    name: "Pro",
    price: "R999",
    period: "/ month",
    desc: "For brands running campaigns monthly and saving reports.",
    features: [
      "Unlimited analyses",
      "Saved creators + notes",
      "Exports (PDF/CSV) — soon",
      "Priority support",
    ],
    cta: "Start Pro",
    highlight: true,
  },
  {
    name: "Team",
    price: "Custom",
    period: "",
    desc: "For teams who need shared access and workflows.",
    features: [
      "Multi-seat access",
      "Shared saved lists",
      "Usage controls",
      "SLA + onboarding",
    ],
    cta: "Contact us",
  },
];

export default function PricingPage() {
  return (
    <main
      className="relative min-h-screen px-6 py-10"
      style={{ background: "var(--bg)", color: "var(--fg)" }}
    >
      <LiquidEtherBackground />

      <div className="relative mx-auto max-w-5xl space-y-10">
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

        <header className="text-center space-y-3">
          <div
            className="mx-auto inline-flex rounded-full px-3 py-1 text-xs"
            style={{
              background: "var(--muted)",
              border: "1px solid var(--border)",
            }}
          >
            Plans
          </div>

          <h1 className="text-3xl font-semibold md:text-4xl">
            Simple pricing for a clear workflow
          </h1>

          <p className="mx-auto max-w-2xl text-sm opacity-80">
            Start with the MVP and upgrade when you’re ready. Analyse creators,
            compare consistency, and sanity-check CPMs fast.
          </p>

          <div className="pt-3 flex justify-center gap-3">
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
        </header>

        <section className="grid gap-4 md:grid-cols-3">
          {plans.map((p) => (
            <div
              key={p.name}
              className="rounded-2xl p-6 text-left"
              style={{
                background: "rgba(255,255,255,0.03)",
                border: p.highlight
                  ? "1px solid var(--primary)"
                  : "1px solid var(--border)",
                backdropFilter: "blur(10px)",
                boxShadow: p.highlight
                  ? "0 0 0 3px rgba(126,143,201,0.12)"
                  : "none",
              }}
            >
              <div className="flex items-start justify-between">
                <div>
                  <div className="text-sm font-semibold">{p.name}</div>
                  <div className="mt-2 flex items-baseline gap-1">
                    <div className="text-3xl font-semibold">{p.price}</div>
                    <div className="text-sm opacity-70">{p.period}</div>
                  </div>
                </div>

                {p.highlight ? (
                  <div
                    className="rounded-full px-2 py-1 text-[11px]"
                    style={{ background: "rgba(126,143,201,0.18)" }}
                  >
                    Recommended
                  </div>
                ) : null}
              </div>

              <p className="mt-3 text-sm opacity-80">{p.desc}</p>

              <ul className="mt-5 space-y-2 text-sm">
                {p.features.map((f) => (
                  <li key={f} className="flex gap-2">
                    <span style={{ color: "var(--primary)" }}>•</span>
                    <span className="opacity-85">{f}</span>
                  </li>
                ))}
              </ul>

              <div className="mt-6">
                <button
                  className="w-full rounded-md px-4 py-2 text-sm font-medium transition"
                  style={{
                    background: p.highlight ? "var(--primary)" : "var(--muted)",
                    color: p.highlight ? "#0E1114" : "var(--fg)",
                    border: p.highlight ? "none" : "1px solid var(--border)",
                  }}
                >
                  {p.cta}
                </button>

                <div className="mt-2 text-xs opacity-60">
                  Payments + login enabled at launch.
                </div>
              </div>
            </div>
          ))}
        </section>
      </div>
    </main>
  );
}
