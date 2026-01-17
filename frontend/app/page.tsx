"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

export default function LandingPage() {
  const router = useRouter();
  const [destination, setDestination] = useState("hampi");
  const [days, setDays] = useState(2);
const MAX_DAYS = 7;
const MIN_DAYS = 1;

const [error, setError] = useState<string | null>(null);

function handleGenerate() {
  if (days < MIN_DAYS || days > MAX_DAYS) {
    setError(`Please select between ${MIN_DAYS} and ${MAX_DAYS} days.`);
    return;
  }

  setError(null);
  router.push(`/${destination}?days=${days}`);
}

  return (
    <main
      className="relative min-h-screen bg-cover bg-center"
      style={{ backgroundImage: "url('/nature.jpg')" }}
    >
      {/* Dark overlay */}
      <div className="absolute inset-0 bg-black/60" />

      {/* Content */}
      <div className="relative z-10 max-w-4xl mx-auto px-6 py-24 text-white">
        {/* Hero */}
        <h1 className="text-5xl font-bold mb-4 leading-tight">
          Incredible India is waiting for you to explore
        </h1>

        <p className="text-lg text-gray-200 mb-12">
          Discover places like a local, not a tourist.
        </p>

        {/* Planner Card */}
        <div className="bg-white text-gray-900 rounded-2xl shadow-2xl p-6 max-w-3xl">
          <h3 className="text-lg font-semibold mb-4">
            Plan your journey
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-end">
            {/* Destination */}
            <div>
              <label className="block text-sm font-medium mb-1">
                Destination
              </label>
              <select
                value={destination}
                onChange={(e) => setDestination(e.target.value)}
                className="w-full rounded-lg border border-gray-300 bg-white px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-black"
              >
                <option value="hampi">Hampi</option>
              </select>
            </div>

            {/* Days */}
            <div>
              <label className="block text-sm font-medium mb-1">
                Days
              </label>
              <input
                type="number"
                min={1}
                max={7}
                value={days}
                onChange={(e) => setDays(Number(e.target.value))}
                className="w-full rounded-lg border border-gray-300 px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-black"
              />
            </div>

            {/* Button */}
            <button
              onClick={handleGenerate}
              className="h-[42px] bg-black text-white rounded-lg hover:bg-gray-800 transition"
            >
              Generate
            </button>
            {error && (
              <p className="text-sm text-red-600 mt-2">
                {error}
              </p>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
