import { JetLuxHero } from '@/components/JetLuxHero'
import { Hosts } from '@/components/Hosts'
import { Reviews } from '@/components/Reviews'
import { ContactBanner } from '@/components/ContactBanner'

export default function Home() {
  return (
    <>
      <JetLuxHero />
      <Hosts />
      <Reviews />
      <ContactBanner />
    </>
  )
}
