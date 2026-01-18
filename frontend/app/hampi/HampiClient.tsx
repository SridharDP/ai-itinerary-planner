"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";

export default function HampiClient() {
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
        const res = await fetch(
          `${process.env.NEXT_PUBLIC_API_BASE_URL}/itinerary/generate`,
          {
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
          }
        );

        if (!res.ok) {
          throw new Error("Failed to generate itinerary");
        }

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

  if (loading) return <p className="text-white">Planning your trip…</p>;
  if (error) return <p className="text-red-400">{error}</p>;

  return (
    <section className="max-w-5xl mx-auto px-6 pb-24 space-y-10">
      {result?.days?.map((day: any, idx: number) => (
        <div key={idx} className="bg-white rounded-2xl shadow-xl p-8">
          <h2 className="text-2xl font-bold mb-4">Day {idx + 1}</h2>
          <div className="grid md:grid-cols-3 gap-8">
            {["morning", "afternoon", "evening"].map((slot) => (
              <div key={slot}>
                <div className="font-semibold mb-2 capitalize">{slot}</div>
                <ul className="space-y-1">
                  {day.schedule[slot]?.map((item: string, i: number) => (
                    <li key={i}>• {item}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      ))}
    </section>
  );
}
