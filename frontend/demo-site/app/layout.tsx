import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Atlas para Rosa Pistacho",
  description: "Demo temporal de conversacion para validar Atlas v0.1.",
  icons: {
    icon: "/favicon.svg",
    shortcut: "/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
