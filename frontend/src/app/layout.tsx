import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "CareerPilot AI | AI Resume Analyzer & Job Matcher",
  description:
    "Upload a resume, match against job descriptions, pinpoint skill gaps, and practice tailored interview questions.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="antialiased font-sans bg-slate-50 text-slate-900 min-h-screen">
        <header className="border-b border-slate-200 bg-white/80 backdrop-blur sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-xl bg-indigo-600 flex items-center justify-center text-white font-bold text-xl shadow-md shadow-indigo-100">
                CP
              </div>
              <div>
                <span className="font-extrabold text-xl tracking-tight text-slate-900">CareerPilot</span>
                <span className="ml-1 px-1.5 py-0.5 text-xs font-semibold uppercase bg-indigo-100 text-indigo-700 rounded-md">
                  AI
                </span>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-xs font-medium text-slate-500 hidden sm:inline-block">
                Stack: Next.js • FastAPI • NLP • PostgreSQL
              </span>
              <a
                href="http://127.0.0.1:8000/docs"
                target="_blank"
                rel="noreferrer"
                className="text-xs font-semibold px-3 py-1.5 rounded-lg border border-slate-300 text-slate-700 hover:bg-slate-50 transition"
              >
                API Docs
              </a>
            </div>
          </div>
        </header>
        <main>{children}</main>
      </body>
    </html>
  );
}

