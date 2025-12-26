"use client";

import { useState } from "react";
import { motion } from "framer-motion";

export default function Home() {
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  async function generate() {
    if (!prompt.trim()) return;

    setLoading(true);
    setResponse("");

    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/generate`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ prompt }),
        }
      );

      const data = await res.json();
      setResponse(data.response);
    } catch {
      setResponse("Backend error. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-black text-gray-200 flex justify-center">
      <motion.div
        className="w-full max-w-4xl px-10 py-16"
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, ease: "easeOut" }}
      >
        {/* Header */}
        <header className="mb-12">
          <h1 className="text-3xl font-medium tracking-tight">
            Sarcastic LLM
          </h1>

          <p className="mt-3 text-sm text-gray-500 max-w-xl">
            An instruction-tuned language model designed to respond with
            unnecessary confidence and dry sarcasm.
          </p>

          <div className="mt-6 h-px w-24 bg-neutral-800" />
        </header>

        {/* Prompt Card */}
        <section className="bg-neutral-950 border border-neutral-800 rounded-xl p-6 shadow-sm">
          <div className="mb-3 text-xs uppercase tracking-wide text-gray-500">
            Prompt
          </div>

          <textarea
            className="w-full h-36 bg-neutral-900 border border-neutral-800 rounded-lg p-4 resize-none focus:outline-none focus:ring-1 focus:ring-neutral-600 text-sm"
            placeholder="Ask something obvious."
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
          />

          <div className="mt-4 flex items-center justify-between">
            <button
              onClick={generate}
              disabled={loading}
              className="px-6 py-2 bg-neutral-800 hover:bg-neutral-700 disabled:opacity-50 rounded-lg transition-colors text-sm"
            >
              {loading ? "Generating…" : "Generate"}
            </button>

            {loading && (
              <span className="text-xs text-gray-500">
                Running inference
              </span>
            )}
          </div>
        </section>

        {/* Spacing */}
        {(response || loading) && <div className="h-8" />}

        {/* Response Card */}
        {response && (
          <motion.section
            className="bg-neutral-950 border border-neutral-800 rounded-xl p-6 shadow-sm"
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.25 }}
          >
            <div className="mb-3 text-xs uppercase tracking-wide text-gray-500">
              Model Response
            </div>

            <div className="whitespace-pre-wrap text-sm leading-relaxed text-gray-200">
              {response}
            </div>
          </motion.section>
        )}
      </motion.div>
    </main>
  );
}
