import { Suspense } from "react";
import HampiClient from "./HampiClient";

export default function HampiPage() {
  return (
    <Suspense fallback={<Loading />}>
      <HampiClient />
    </Suspense>
  );
}

function Loading() {
  return (
    <div className="min-h-screen flex items-center justify-center text-white">
      Loading itinerary...
    </div>
  );
}
