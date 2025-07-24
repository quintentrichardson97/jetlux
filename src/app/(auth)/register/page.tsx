'use client'

import { useState } from 'react'
import Link from 'next/link'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Register',
}

interface FormState {
  username: string
  password1: string
  password2: string
  email: string
  profile_picture: File | null
  is_ski_buddy: boolean
  is_affiliate: boolean
  business_name: string
  license_number: string
  availability: string
  experience_level: string
  buddy_bio: string
  rate_per_hour: string
}

export default function RegisterPage() {
  const [form, setForm] = useState<FormState>({
    username: '',
    password1: '',
    password2: '',
    email: '',
    profile_picture: null,
    is_ski_buddy: false,
    is_affiliate: false,
    business_name: '',
    license_number: '',
    availability: '',
    experience_level: '',
    buddy_bio: '',
    rate_per_hour: '',
  })
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)

  const handleChange = (field: keyof FormState) => (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const value =
      e.target.type === 'checkbox'
        ? (e.target as HTMLInputElement).checked
        : e.target.value
    setForm((f) => ({
      ...f,
      [field]: value,
    }))
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm((f) => ({ ...f, profile_picture: e.target.files?.[0] || null }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setSuccess(false)
    try {
      const formData = new FormData()
      formData.append('username', form.username)
      formData.append('password1', form.password1)
      formData.append('password2', form.password2)
      formData.append('email', form.email)
      if (form.profile_picture) {
        formData.append('profile_picture', form.profile_picture)
      }
      formData.append('is_ski_buddy', String(form.is_ski_buddy))
      formData.append('is_affiliate', String(form.is_affiliate))
      if (form.is_affiliate) {
        formData.append('business_name', form.business_name)
        formData.append('license_number', form.license_number)
      }
      if (form.is_ski_buddy) {
        formData.append('availability', form.availability)
        formData.append('experience_level', form.experience_level)
        formData.append('buddy_bio', form.buddy_bio)
        formData.append('rate_per_hour', form.rate_per_hour)
      }
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/register/`,
        {
          method: 'POST',
          credentials: 'include',
          body: formData,
        }
      )
      if (!res.ok) {
        const data = await res.json().catch(() => null)
        throw new Error(data?.detail || 'Registration failed')
      }
      setSuccess(true)
      setForm({
        username: '',
        password1: '',
        password2: '',
        email: '',
        profile_picture: null,
        is_ski_buddy: false,
        is_affiliate: false,
        business_name: '',
        license_number: '',
        availability: '',
        experience_level: '',
        buddy_bio: '',
        rate_per_hour: '',
      })
    } catch (err) {
      setError((err as Error).message)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-dark px-4 sm:px-6 lg:px-8 py-12">
      <div className="w-full max-w-md bg-charcoal text-mist rounded-xl shadow-xl p-6 sm:p-8 space-y-6">
        <h2 className="text-center text-3xl font-heading text-white">Create an Account</h2>
        <form onSubmit={handleSubmit} className="space-y-5" id="registrationForm" encType="multipart/form-data">
          <input
            type="text"
            className="block w-full rounded-md border-gray-300 text-gray-900 placeholder-gray-400 focus:border-gold focus:ring-gold"
            placeholder="Username"
            value={form.username}
            onChange={handleChange('username')}
            required
          />
          <input
            type="email"
            className="block w-full rounded-md border-gray-300 text-gray-900 placeholder-gray-400 focus:border-gold focus:ring-gold"
            placeholder="Email"
            value={form.email}
            onChange={handleChange('email')}
            required
          />
          <input
            type="password"
            className="block w-full rounded-md border-gray-300 text-gray-900 placeholder-gray-400 focus:border-gold focus:ring-gold"
            placeholder="Password"
            value={form.password1}
            onChange={handleChange('password1')}
            required
          />
          <input
            type="password"
            className="block w-full rounded-md border-gray-300 text-gray-900 placeholder-gray-400 focus:border-gold focus:ring-gold"
            placeholder="Confirm Password"
            value={form.password2}
            onChange={handleChange('password2')}
            required
          />
          <input
            type="file"
            className="block w-full text-sm text-gray-400"
            onChange={handleFileChange}
          />
          <label className="flex items-center space-x-2">
            <input
              type="checkbox"
              checked={form.is_ski_buddy}
              onChange={handleChange('is_ski_buddy')}
              className="rounded border-gray-300 text-gold focus:ring-gold"
            />
            <span>Register as Ski Buddy</span>
          </label>
          <label className="flex items-center space-x-2">
            <input
              type="checkbox"
              checked={form.is_affiliate}
              onChange={handleChange('is_affiliate')}
              className="rounded border-gray-300 text-gold focus:ring-gold"
            />
            <span>Register as Affiliate</span>
          </label>
          {form.is_affiliate && (
            <div className="space-y-4">
              <input
                type="text"
                className="block w-full rounded-md border-gray-300 text-gray-900 placeholder-gray-400 focus:border-gold focus:ring-gold"
                placeholder="Business Name"
                value={form.business_name}
                onChange={handleChange('business_name')}
              />
              <input
                type="text"
                className="block w-full rounded-md border-gray-300 text-gray-900 placeholder-gray-400 focus:border-gold focus:ring-gold"
                placeholder="License Number"
                value={form.license_number}
                onChange={handleChange('license_number')}
              />
            </div>
          )}
          {form.is_ski_buddy && (
            <div className="space-y-4">
              <input
                type="text"
                className="block w-full rounded-md border-gray-300 text-gray-900 placeholder-gray-400 focus:border-gold focus:ring-gold"
                placeholder="Availability"
                value={form.availability}
                onChange={handleChange('availability')}
              />
              <input
                type="text"
                className="block w-full rounded-md border-gray-300 text-gray-900 placeholder-gray-400 focus:border-gold focus:ring-gold"
                placeholder="Experience Level"
                value={form.experience_level}
                onChange={handleChange('experience_level')}
              />
              <textarea
                className="block w-full rounded-md border-gray-300 text-gray-900 placeholder-gray-400 focus:border-gold focus:ring-gold"
                placeholder="Buddy Bio"
                value={form.buddy_bio}
                onChange={handleChange('buddy_bio')}
              />
              <input
                type="text"
                className="block w-full rounded-md border-gray-300 text-gray-900 placeholder-gray-400 focus:border-gold focus:ring-gold"
                placeholder="Rate per Hour"
                value={form.rate_per_hour}
                onChange={handleChange('rate_per_hour')}
              />
            </div>
          )}
          <button
            type="submit"
            className="w-full rounded-md bg-gold py-2 text-dark hover:bg-gold-600"
          >
            Register
          </button>
          {error && <p className="text-sm text-red-400">{error}</p>}
          {success && <p className="text-sm text-green-400">Registration successful!</p>}
        </form>
        <p className="text-center text-sm text-gray-400">
          Already have an account?{' '}
          <Link href="/login" className="text-gold hover:underline">
            Login here
          </Link>
        </p>
      </div>
    </div>
  )
}
