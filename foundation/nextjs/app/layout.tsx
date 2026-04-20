export const metadata = {
  title: "ENVR Quantum Hub",
  description: "Theoretical and applied quantum computations with cluster prototype tooling.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
