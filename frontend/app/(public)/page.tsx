import Link from "next/link";
import LiquidEtherBackground from "@/components/LiquidEtherBackground";

export default function HomePage() {
  return (
    <main
      className="relative min-h-screen overflow-hidden px-6"
      style={{ background: "var(--bg)", color: "var(--fg)" }}
    >
      <LiquidEtherBackground />

      {/* Content must be above the background */}
      <div className="relative z-10 mx-auto flex min-h-screen max-w-5xl flex-col items-center justify-center text-center">
        <div
          className="mb-4 inline-flex rounded-full px-3 py-1 text-xs"
          style={{
            background: "var(--muted)",
            border: "1px solid var(--border)",
          }}
        >
          Influencer Intel • MVP
        </div>

        <h1 className="max-w-3xl text-4xl font-semibold leading-tight md:text-5xl">
          YouTube creator analysis brands can actually trust.
        </h1>

        <p className="mt-4 max-w-2xl text-sm opacity-80">
          Paste a YouTube channel or video link and get a clear report — median
          vs average views, engagement quality, risk signals, and campaign
          costing.
        </p>

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
              desc: "CPM estimates, margins, and currency conversion.",
            },
          ].map((c) => (
            <div
              key={c.title}
              className="rounded-xl p-5 text-left"
              style={{
                background: "rgba(255,255,255,0.04)",
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

// import Link from "next/link";
// import LiquidEtherBackground from "@/components/LiquidEtherBackground";

// export default function HomePage() {
//   return (
//     <main
//       className="relative min-h-screen px-6"
//       style={{ background: "var(--bg)", color: "var(--fg)" }}
//     >
//       <LiquidEtherBackground />

//       <div className="relative mx-auto flex min-h-screen max-w-5xl flex-col items-center justify-center text-center">
//         <div
//           className="mb-4 inline-flex rounded-full px-3 py-1 text-xs"
//           style={{
//             background: "var(--muted)",
//             border: "1px solid var(--border)",
//           }}
//         >
//           Influencer Intel • MVP
//         </div>

//         <h1 className="max-w-3xl text-4xl font-semibold leading-tight md:text-5xl">
//           YouTube creator analysis brands can actually trust.
//         </h1>

//         <p className="mt-4 max-w-2xl text-sm opacity-80">
//           Paste a YouTube channel or video link and get a clear, structured
//           report — median vs average views, engagement quality, risk signals,
//           and campaign costing in one place.
//         </p>

//         <div className="mt-8 flex flex-wrap justify-center gap-3">
//           <Link
//             href="/app/analyse"
//             className="rounded-md px-5 py-2 text-sm font-medium transition"
//             style={{ background: "var(--primary)", color: "#0E1114" }}
//           >
//             Open the app
//           </Link>

//           <Link
//             href="/pricing"
//             className="rounded-md px-5 py-2 text-sm transition"
//             style={{
//               background: "var(--muted)",
//               border: "1px solid var(--border)",
//             }}
//           >
//             View plans
//           </Link>

//           <Link
//             href="/tutorial"
//             className="rounded-md px-5 py-2 text-sm transition"
//             style={{
//               background: "transparent",
//               border: "1px solid var(--border)",
//             }}
//           >
//             View tutorial
//           </Link>
//         </div>

//         <section className="mt-16 grid w-full gap-4 md:grid-cols-3">
//           {[
//             {
//               title: "Performance snapshot",
//               desc: "Median vs mean views, engagement rate, consistency, and risk signals.",
//             },
//             {
//               title: "Recent video breakdown",
//               desc: "See how the last uploads actually performed, not inflated averages.",
//             },
//             {
//               title: "Campaign costing",
//               desc: "CPM estimates, fee comparisons, margins, and live currency conversion.",
//             },
//           ].map((c) => (
//             <div
//               key={c.title}
//               className="rounded-xl p-5 text-left"
//               style={{
//                 background: "rgba(255,255,255,0.03)",
//                 border: "1px solid var(--border)",
//                 backdropFilter: "blur(8px)",
//               }}
//             >
//               <div className="text-sm font-semibold">{c.title}</div>
//               <div className="mt-1 text-sm opacity-80">{c.desc}</div>
//             </div>
//           ))}
//         </section>
//       </div>
//     </main>
//   );
// }
