export const metadata = {
  title: 'Finalize Your Booking',
}

export default function BookingPage() {
  return (
    <div className="mx-auto max-w-2xl px-4 py-16">
      <h1 className="text-3xl font-semibold">Finalize Your Booking</h1>
      <form className="mt-8 grid gap-4">
        <input className="border p-2" placeholder="Vehicle" />
        <input className="border p-2" placeholder="Buddy" />
        <input type="datetime-local" className="border p-2" placeholder="Start Time" />
        <input className="border p-2" placeholder="Duration" />
        <input type="datetime-local" className="border p-2" placeholder="End Time" />
        <input className="border p-2" placeholder="Promo Code" />
        <button className="mt-4 rounded bg-cyan-600 p-2 text-white" type="submit">Book Now</button>
      </form>
    </div>
  )
}
