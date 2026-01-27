export default function PublicBackground() {
  return (
    <div
      aria-hidden
      className="pointer-events-none absolute inset-0 overflow-hidden"
    >
      {/* soft animated blobs */}
      <div
        className="absolute -top-24 left-1/2 h-[520px] w-[520px] -translate-x-1/2 rounded-full blur-3xl"
        style={{
          background:
            "radial-gradient(circle, rgba(126,143,201,0.35), transparent 60%)",
          animation: "float1 10s ease-in-out infinite",
        }}
      />
      <div
        className="absolute bottom-[-140px] left-10 h-[520px] w-[520px] rounded-full blur-3xl"
        style={{
          background:
            "radial-gradient(circle, rgba(216,188,138,0.20), transparent 60%)",
          animation: "float2 12s ease-in-out infinite",
        }}
      />
      <div
        className="absolute top-24 right-[-140px] h-[520px] w-[520px] rounded-full blur-3xl"
        style={{
          background:
            "radial-gradient(circle, rgba(154,163,178,0.25), transparent 60%)",
          animation: "float3 14s ease-in-out infinite",
        }}
      />
    </div>
  );
}
