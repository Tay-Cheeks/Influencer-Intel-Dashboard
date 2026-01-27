export default function PublicLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div
      className="min-h-screen"
      style={{ background: "var(--bg)", color: "var(--fg)" }}
    >
      {children}
    </div>
  );
}
