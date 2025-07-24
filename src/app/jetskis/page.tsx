import { type Metadata } from 'next'
import { getJSON } from '@/lib/api'
import Image from 'next/image'

export const metadata: Metadata = {
  title: 'Jet Skis – Charlies Rentals',
}

interface Vehicle {
  id: number
  name: string
  image?: string
  available: boolean
  rate_per_hour?: string
  top_speed?: string
  max_riders?: number
  weight_limit?: string
}

export default async function JetSkisPage() {
  const skis = await getJSON<Vehicle[]>('/api/vehicles/')

  return (
    <div className="mx-auto max-w-4xl px-4 py-16">
      <h1 className="text-3xl font-semibold">Jet Skis</h1>
      <ul className="mt-8 grid gap-8 sm:grid-cols-2">
        {skis.map((ski) => (
          <li key={ski.id} className="rounded-lg border p-4">
            {ski.image ? (
              <Image
                src={ski.image}
                alt=""
                width={320}
                height={160}
                className="mb-4 h-40 w-full object-cover"
              />
            ) : (
              <div className="mb-4 h-40 bg-gray-200" />
            )}
            <h2 className="text-xl font-medium">{ski.name}</h2>
            {ski.rate_per_hour && <p className="mt-1 text-sm">Rate: {ski.rate_per_hour}</p>}
            {ski.top_speed && <p className="text-sm">Top Speed: {ski.top_speed}</p>}
            {typeof ski.max_riders !== 'undefined' && (
              <p className="text-sm">Max Riders: {ski.max_riders}</p>
            )}
            {ski.weight_limit && <p className="text-sm">Weight Limit: {ski.weight_limit}</p>}
            <p className="mt-2 text-sm font-semibold">
              {ski.available ? 'Available' : 'Currently Unavailable'}
            </p>
          </li>
        ))}
      </ul>
    </div>
  )
}
