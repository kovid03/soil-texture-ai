import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: "Soil Texture AI — Classify Soil from Images",
  description:
    "Upload a soil image and get AI-powered classification (Clay, Loam, Sandy, Loamy Sand, Sandy Loam) with crop and fertilizer recommendations.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${inter.variable}`}>
      <body className="font-sans">{children}</body>
    </html>
  );
}
