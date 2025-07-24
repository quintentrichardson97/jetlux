import Link from 'next/link'

import { Container } from '@/components/Container'
import { NavLinks } from '@/components/NavLinks'

export function Footer() {
  return (
    <footer className="border-t border-gray-200">
      <Container>
        <div className="flex flex-col items-start justify-between gap-y-12 pt-16 pb-6 lg:flex-row lg:items-center lg:py-16">
          <div>
            <p className="text-xl font-semibold text-gray-900">JetLux</p>
            <p className="mt-1 text-sm text-gray-700">Luxury on the water starts here 🌊</p>
            <nav className="mt-6 flex gap-8">
              <NavLinks />
            </nav>
          </div>
        </div>
        <div className="flex flex-col items-center border-t border-gray-200 py-8">
          <p className="text-sm text-gray-500">
            © 2025 JetLux • Tampa, Florida
          </p>
        </div>
      </Container>
    </footer>
  )
}
