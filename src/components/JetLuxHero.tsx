import { Button } from '@/components/Button'

export function JetLuxHero() {
  return (
    <section className="relative h-[60vh] w-full overflow-hidden bg-gray-900">
      <video
        className="absolute inset-0 h-full w-full object-cover"
        src="/videos/hero.mp4"
        autoPlay
        loop
        muted
      />
      <div className="absolute inset-0 bg-black/40" />
      <div className="relative z-10 flex h-full flex-col items-center justify-center text-center text-white px-4">
        <h1 className="text-4xl font-bold sm:text-5xl">Premium Water Vehicle Rentals</h1>
        <p className="mt-4 max-w-xl text-lg">
          Experience the thrill on the water with top-tier equipment and unbeatable views.
        </p>
        <Button href="/booking" color="cyan" className="mt-6">
          Book Now
        </Button>
      </div>
    </section>
  )
}
