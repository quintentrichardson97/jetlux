import { type Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Jet Skis – Charlies Rentals',
}

const skis = [
  {
    name: 'Yamaha EX Deluxe',
    image: '',
    available: true,
    rate: '$120/hr',
    speed: '50 mph',
    riders: 2,
    limit: '350 lbs',
  },
  {
    name: 'Sea-Doo Spark Trixx',
    image: '',
    available: false,
    rate: '$110/hr',
    speed: '48 mph',
    riders: 2,
    limit: '330 lbs',
  },
]

export default function JetSkisPage() {
  return (
    <div className="mx-auto max-w-4xl px-4 py-16">
      <h1 className="text-3xl font-semibold">Jet Skis</h1>
      <ul className="mt-8 grid gap-8 sm:grid-cols-2">
        {skis.map((ski) => (
          <li key={ski.name} className="rounded-lg border p-4">
            <div className="h-40 bg-gray-200 mb-4" />
            <h2 className="text-xl font-medium">{ski.name}</h2>
            <p className="mt-1 text-sm">Rate: {ski.rate}</p>
            <p className="text-sm">Top Speed: {ski.speed}</p>
            <p className="text-sm">Max Riders: {ski.riders}</p>
            <p className="text-sm">Weight Limit: {ski.limit}</p>
            <p className="mt-2 text-sm font-semibold">
              {ski.available ? 'Available' : 'Currently Unavailable'}
            </p>
          </li>
        ))}
      </ul>
    </div>
  )
}
