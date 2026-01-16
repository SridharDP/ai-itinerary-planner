"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";

export default function HampiPage() {
  const searchParams = useSearchParams();
  const days = Number(searchParams.get("days") || 2);

  const [loading, setLoading] = useState(true);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchItinerary() {
      setLoading(true);
      setError(null);

      try {
        const res = await fetch("http://localhost:8000/itinerary/generate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            from_city: "Bangalore",
            destination: "hampi",
            days,
            pace: "balanced",
            interests: ["history", "local"],
            arrival_time: "06:00",
          }),
        });

        if (!res.ok) throw new Error("Failed to generate itinerary");

        const data = await res.json();
        setResult(data);
      } catch (e: any) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    }

    fetchItinerary();
  }, [days]);

  return (
    <main className="relative min-h-screen font-sans">
      {/* Fixed background */}
      <div
        className="fixed inset-0 bg-cover bg-center"
        style={{ backgroundImage: "url('/hampi_stone_chariot.jpg')" }}
      >
        <div className="absolute inset-0 bg-black/70" />
      </div>

      {/* Scrollable content */}
      <div className="relative z-10">
        {/* Hero */}
        <section className="max-w-5xl mx-auto px-6 pt-32 pb-24 text-white">
          <h1 className="text-5xl md:text-6xl font-serif font-bold mb-6 leading-tight">
            Discover Hampi’s Timeless Vijayanagara Legacy
          </h1>
          <p className="text-lg md:text-xl text-gray-200 max-w-2xl">
            Ancient ruins, river walks, bazaar life, and slow living —
            experience Hampi like a local.
          </p>
        </section>

        {/* Itinerary */}
        <section className="max-w-5xl mx-auto px-6 pb-24 space-y-10">
          {loading && (
            <p className="text-gray-200 text-lg">
              Planning your itinerary…
            </p>
          )}

          {error && (
            <p className="text-red-400 text-lg">
              {error}
            </p>
          )}

          {result?.days?.map((day: any, idx: number) => (
            <div
              key={idx}
              className="bg-white/95 backdrop-blur-md rounded-2xl shadow-2xl p-8"
            >
              {/* Day header */}
              <div className="flex justify-between items-center mb-8">
                <h2 className="text-2xl font-serif font-bold text-gray-900">
                  Day {idx + 1}
                </h2>
                <span className="text-sm text-gray-500">
                  Relaxed local pace
                </span>
              </div>

              {/* Schedule */}
              <div className="grid md:grid-cols-3 gap-8">
                {/* Morning */}
                <div>
                  <div className="font-semibold text-gray-800 mb-3">
                    🌅 Morning
                  </div>
                  <ul className="space-y-2 text-gray-900">
                    {day.schedule.morning?.map((item: string, i: number) => (
                      <li key={i}>• {item}</li>
                    ))}
                  </ul>
                </div>

                {/* Afternoon */}
                <div>
                  <div className="font-semibold text-gray-800 mb-3">
                    ☀️ Afternoon
                  </div>
                  <ul className="space-y-2 text-gray-900">
                    {day.schedule.afternoon?.map((item: string, i: number) => (
                      <li key={i}>• {item}</li>
                    ))}
                  </ul>
                </div>

                {/* Evening */}
                <div>
                  <div className="font-semibold text-gray-800 mb-3">
                    🌇 Evening
                  </div>
                  <ul className="space-y-2 text-gray-900">
                    {day.schedule.evening?.map((item: string, i: number) => (
                      <li key={i}>• {item}</li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Food */}
              {day.food?.length > 0 && (
                <div className="mt-8 pt-6 border-t">
                  <div className="font-semibold text-gray-800 mb-3">
                    🍽 Food highlights
                  </div>
                  <ul className="space-y-2 text-gray-900">
                    {day.food.map((f: string, i: number) => (
                      <li key={i}>• {f}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ))}
        </section>
      </div>
    </main>
  );
}
