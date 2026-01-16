"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

export default function LandingPage() {
  const router = useRouter();
  const [days, setDays] = useState(2);

  function handleGenerate() {
    router.push(`/hampi?days=${days}`);
  }

  return (
    <main className="relative min-h-screen bg-cover bg-center"
      style={{ backgroundImage: "url('/nature.jpg')" }}
    >
      <div className="absolute inset-0 bg-black/60" />

      <div className="relative z-10 max-w-4xl mx-auto px-6 py-24 text-white">
        <h1 className="text-5xl font-bold mb-4">
          Incredible India is waiting for you to explore
        </h1>

        <p className="text-lg mb-10 text-gray-200">
          Discover places like a local, not a tourist.
        </p>

        <div className="bg-white rounded-2xl p-6 flex gap-4 items-end text-black">
          <div>
            <label className="block text-sm mb-1">Destination</label>
            <select
              disabled
              className="border rounded px-3 py-2 bg-gray-100"
            >
              <option>Hampi</option>
            </select>
          </div>

          <div>
            <label className="block text-sm mb-1">Number of days</label>
            <input
              type="number"
              min={1}
              max={5}
              value={days}
              onChange={(e) => setDays(Number(e.target.value))}
              className="border rounded px-3 py-2 w-28"
            />
          </div>

          <button
            onClick={handleGenerate}
            className="bg-black text-white px-6 py-2 rounded"
          >
            Generate
          </button>
        </div>
      </div>
    </main>
  );
}
