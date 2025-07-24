"use client"

import { useEffect, useState } from 'react'
import { getJSON, postJSON } from '@/lib/api'

export const metadata = {
  title: 'Finalize Your Booking',
}

interface Vehicle { id: number; name: string }
interface Buddy { id: number; name: string }

export default function BookingPage() {
  const [vehicles, setVehicles] = useState<Vehicle[]>([])
  const [buddies, setBuddies] = useState<Buddy[]>([])
  const [form, setForm] = useState({
    vehicle: '',
    buddy: '',
    start_time: '',
    duration: '',
    promo_code: '',
  })
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)

  useEffect(() => {
    getJSON<Vehicle[]>('/api/vehicles/').then(setVehicles).catch(console.error)
    getJSON<Buddy[]>('/api/ski-buddies/').then(setBuddies).catch(console.error)
  }, [])

  const handleChange = (field: string) =>
    (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
      setForm({ ...form, [field]: e.target.value })
    }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setSuccess(false)
    try {
      await postJSON('/process-booking/', {
        vehicle: form.vehicle,
        buddy: form.buddy,
        start_time: form.start_time,
        duration: Number(form.duration),
        promo_code: form.promo_code || undefined,
      })
      setSuccess(true)
    } catch (err) {
      setError((err as Error).message)
    }
  }

  return (
    <div className="mx-auto max-w-2xl px-4 py-16">
      <h1 className="text-3xl font-semibold">Finalize Your Booking</h1>
      <form onSubmit={handleSubmit} className="mt-8 grid gap-4">
        <select
          className="border p-2"
          value={form.vehicle}
          onChange={handleChange('vehicle')}
          required
        >
          <option value="">Select Vehicle</option>
          {vehicles.map((v) => (
            <option key={v.id} value={v.id}>
              {v.name}
            </option>
          ))}
        </select>
        <select
          className="border p-2"
          value={form.buddy}
          onChange={handleChange('buddy')}
          required
        >
          <option value="">Select Buddy</option>
          {buddies.map((b) => (
            <option key={b.id} value={b.id}>
              {b.name}
            </option>
          ))}
        </select>
        <input
          type="datetime-local"
          className="border p-2"
          value={form.start_time}
          onChange={handleChange('start_time')}
          required
        />
        <input
          type="number"
          className="border p-2"
          placeholder="Duration (hrs)"
          value={form.duration}
          onChange={handleChange('duration')}
          required
        />
        <input
          className="border p-2"
          placeholder="Promo Code"
          value={form.promo_code}
          onChange={handleChange('promo_code')}
        />
        <button className="mt-4 rounded bg-cyan-600 p-2 text-white" type="submit">
          Book Now
        </button>
        {error && <p className="text-sm text-red-600">{error}</p>}
        {success && <p className="text-sm text-green-600">Booking successful!</p>}
      </form>
    </div>
  )
}
