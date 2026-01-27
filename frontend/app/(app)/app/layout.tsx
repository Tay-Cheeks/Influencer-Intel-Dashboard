export default function InnerAppLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return children;
}

// import Sidebar from "@/components/Sidebar";

// export default function AppLayout({ children }: { children: React.ReactNode }) {
//   return (
//     <div
//       className="flex min-h-screen"
//       style={{ background: "var(--bg)", color: "var(--fg)" }}
//     >
//       <Sidebar />
//       <main className="flex-1 p-6">{children}</main>
//     </div>
//   );
// }
