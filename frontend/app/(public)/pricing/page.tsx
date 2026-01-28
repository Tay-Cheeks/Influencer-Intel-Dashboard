"use client";

import Link from "next/link";
import { useSession } from "next-auth/react";
import { useRouter } from "next/navigation";
import LiquidEtherBackground from "@/components/LiquidEtherBackground";
import { PayPalScriptProvider, PayPalButtons } from "@paypal/react-paypal-js";

const plans = [
  {
    id: "starter",
    name: "Starter",
    price: "R499",
    priceUSD: "$29",
    period: "/ month",
    desc: "For quick checks and small teams testing creator fit.",
    features: [
      "30 analyses / month",
      "Key metrics + charts",
      "Campaign costing",
      "Email support",
    ],
    cta: "Start Starter",
    paypalPlanId: "P-STARTER-PLAN-ID", // Replace with actual PayPal plan ID
  },
  {
    id: "pro",
    name: "Pro",
    price: "R999",
    priceUSD: "$59",
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
    paypalPlanId: "P-PRO-PLAN-ID", // Replace with actual PayPal plan ID
  },
  {
    id: "team",
    name: "Team",
    price: "Custom",
    priceUSD: "Custom",
    period: "",
    desc: "For teams who need shared access and workflows.",
    features: [
      "Multi-seat access",
      "Shared saved lists",
      "Usage controls",
      "SLA + onboarding",
    ],
    cta: "Contact us",
    isCustom: true,
  },
];

function PlanCard({ plan }: { plan: typeof plans[0] }) {
  const { data: session } = useSession();
  const router = useRouter();

  const handleSubscribe = () => {
    if (!session) {
      router.push(`/signup?plan=${plan.id}`);
      return;
    }

    if (plan.isCustom) {
      window.location.href = "mailto:sales@influencerintel.com";
      return;
    }

    // For now, just redirect to app
    // In production, this would trigger PayPal subscription flow
    router.push("/app/analyse");
  };

  return (
    <div
      className="rounded-2xl p-6 text-left"
      style={{
        background: "rgba(255,255,255,0.03)",
        border: plan.highlight
          ? "1px solid var(--primary)"
          : "1px solid var(--border)",
        backdropFilter: "blur(10px)",
        boxShadow: plan.highlight
          ? "0 0 0 3px rgba(126,143,201,0.12)"
          : "none",
      }}
    >
      <div className="flex items-start justify-between">
        <div>
          <div className="text-sm font-semibold">{plan.name}</div>
          <div className="mt-2 flex items-baseline gap-1">
            <div className="text-3xl font-semibold">{plan.price}</div>
            <div className="text-sm opacity-70">{plan.period}</div>
          </div>
          {!plan.isCustom && (
            <div className="text-xs opacity-60 mt-1">{plan.priceUSD} USD</div>
          )}
        </div>

        {plan.highlight ? (
          <div
            className="rounded-full px-2 py-1 text-[11px]"
            style={{ background: "rgba(126,143,201,0.18)" }}
          >
            Recommended
          </div>
        ) : null}
      </div>

      <p className="mt-3 text-sm opacity-80">{plan.desc}</p>

      <ul className="mt-5 space-y-2 text-sm">
        {plan.features.map((f) => (
          <li key={f} className="flex gap-2">
            <span style={{ color: "var(--primary)" }}>•</span>
            <span className="opacity-85">{f}</span>
          </li>
        ))}
      </ul>

      <div className="mt-6">
        <button
          onClick={handleSubscribe}
          className="w-full rounded-md px-4 py-2 text-sm font-medium transition hover:opacity-90"
          style={{
            background: plan.highlight ? "var(--primary)" : "var(--muted)",
            color: plan.highlight ? "#0E1114" : "var(--fg)",
            border: plan.highlight ? "none" : "1px solid var(--border)",
          }}
        >
          {plan.cta}
        </button>

        <div className="mt-2 text-xs opacity-60 text-center">
          {session
            ? "Click to subscribe"
            : "Sign up required"}
        </div>
      </div>
    </div>
  );
}

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
            Start with the MVP and upgrade when you're ready. Analyse creators,
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
            <PlanCard key={p.name} plan={p} />
          ))}
        </section>

        {/* PayPal Notice */}
        <div
          className="rounded-2xl p-6 text-center"
          style={{
            border: "1px solid var(--border)",
            background: "rgba(255,255,255,0.02)",
          }}
        >
          <div className="text-sm font-medium mb-2">Secure Payments via PayPal</div>
          <div className="text-xs opacity-70">
            All subscriptions are processed securely through PayPal. You can cancel
            anytime from your account settings.
          </div>
          <div className="mt-4 text-xs opacity-60">
            <strong>Note:</strong> PayPal integration is currently in demo mode. To
            enable live payments, configure your PayPal Business account and add
            plan IDs to the pricing configuration.
          </div>
        </div>
      </div>
    </main>
  );
}
