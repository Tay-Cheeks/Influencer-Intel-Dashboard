"use client";

import dynamic from "next/dynamic";
import { useEffect, useState } from "react";

/**
 * Loads LiquidEther client-side only (no SSR),
 * and falls back to a CSS background if WebGL isn't available.
 */
const LiquidEther = dynamic(() => import("./LiquidEther"), {
  ssr: false,
  loading: () => null,
});

function CssFallbackBackground() {
  return (
    <div className="absolute inset-0 z-0 overflow-hidden">
      <div
        className="absolute -top-32 left-1/2 h-[560px] w-[560px] -translate-x-1/2 rounded-full blur-3xl"
        style={{
          background:
            "radial-gradient(circle, rgba(79,106,255,0.60), transparent 70%)",
          animation: "pulseSlow 6s ease-in-out infinite",
        }}
      />
      <div
        className="absolute top-1/3 left-1/4 h-[440px] w-[440px] rounded-full blur-3xl"
        style={{
          background:
            "radial-gradient(circle, rgba(214,167,255,0.45), transparent 70%)",
          animation: "pulseSlow 7s ease-in-out infinite",
          animationDelay: "0.8s",
        }}
      />
      <div
        className="absolute bottom-20 right-1/4 h-[480px] w-[480px] rounded-full blur-3xl"
        style={{
          background:
            "radial-gradient(circle, rgba(191,215,255,0.45), transparent 70%)",
          animation: "pulseSlow 8s ease-in-out infinite",
          animationDelay: "1.4s",
        }}
      />
    </div>
  );
}

export default function LiquidEtherBackground() {
  const [canUseWebGL, setCanUseWebGL] = useState(true);

  useEffect(() => {
    try {
      const canvas = document.createElement("canvas");
      const gl =
        canvas.getContext("webgl") || canvas.getContext("experimental-webgl");
      if (!gl) setCanUseWebGL(false);
    } catch {
      setCanUseWebGL(false);
    }
  }, []);

  if (!canUseWebGL) {
    return (
      <div className="pointer-events-none absolute inset-0 z-0">
        <CssFallbackBackground />
      </div>
    );
  }

  return (
    <div className="pointer-events-none absolute inset-0 z-0">
      <LiquidEther
        // Cleaner, bolder palette
        colors={["#4F6AFF", "#D6A7FF", "#BFD7FF"]}
        // Stronger motion
        mouseForce={22}
        cursorSize={110}
        // Fluid feel
        isViscous
        viscous={24}
        iterationsViscous={28}
        iterationsPoisson={28}
        // Sharper rendering
        resolution={0.75}
        isBounce={false}
        // Auto motion
        autoDemo
        autoSpeed={0.65}
        autoIntensity={2.6}
        takeoverDuration={0.25}
        autoResumeDelay={1200}
        autoRampDuration={0.4}
        style={{ width: "100%", height: "100%" }}
        // Less washed out
        className="opacity-90"
      />
    </div>
  );
}

// "use client";

// import dynamic from "next/dynamic";
// import { useEffect, useState } from "react";

// const LiquidEther = dynamic(() => import("./LiquidEther"), {
//   ssr: false,
//   loading: () => null,
// });

// function CssFallbackBackground() {
//   return (
//     <div className="absolute inset-0 z-0 overflow-hidden">
//       <div
//         className="absolute -top-32 left-1/2 h-[560px] w-[560px] -translate-x-1/2 rounded-full blur-3xl"
//         style={{
//           background:
//             "radial-gradient(circle, rgba(126,143,201,0.55), transparent 70%)",
//           animation: "pulseSlow 6s ease-in-out infinite",
//         }}
//       />
//       <div
//         className="absolute top-1/3 left-1/4 h-[440px] w-[440px] rounded-full blur-3xl"
//         style={{
//           background:
//             "radial-gradient(circle, rgba(216,188,138,0.45), transparent 70%)",
//           animation: "pulseSlow 7s ease-in-out infinite",
//           animationDelay: "0.8s",
//         }}
//       />
//       <div
//         className="absolute bottom-20 right-1/4 h-[480px] w-[480px] rounded-full blur-3xl"
//         style={{
//           background:
//             "radial-gradient(circle, rgba(154,163,178,0.45), transparent 70%)",
//           animation: "pulseSlow 8s ease-in-out infinite",
//           animationDelay: "1.4s",
//         }}
//       />
//     </div>
//   );
// }

// export default function LiquidEtherBackground() {
//   const [canUseWebGL, setCanUseWebGL] = useState(true);

//   useEffect(() => {
//     try {
//       const canvas = document.createElement("canvas");
//       const gl =
//         canvas.getContext("webgl") || canvas.getContext("experimental-webgl");
//       if (!gl) setCanUseWebGL(false);
//     } catch {
//       setCanUseWebGL(false);
//     }
//   }, []);

//   // IMPORTANT: z-0, not negative. Also pointer-events-none so it doesn't block clicks.
//   if (!canUseWebGL) {
//     return (
//       <div className="pointer-events-none absolute inset-0 z-0">
//         <CssFallbackBackground />
//       </div>
//     );
//   }

//   return (
//     <div className="pointer-events-none absolute inset-0 z-0">
//       <LiquidEther
//         colors={["#7E8FC9", "#D8BC8A", "#9AA3B2"]}
//         mouseForce={16}
//         cursorSize={110}
//         isViscous
//         viscous={26}
//         iterationsViscous={24}
//         iterationsPoisson={24}
//         resolution={0.6}
//         isBounce={false}
//         autoDemo
//         autoSpeed={0.55}
//         autoIntensity={2.2}
//         takeoverDuration={0.25}
//         autoResumeDelay={0}
//         autoRampDuration={0.4}
//         style={{ width: "100%", height: "100%" }}
//         className="opacity-80"
//       />
//     </div>
//   );
// }
