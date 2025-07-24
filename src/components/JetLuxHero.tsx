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
        <h1 className="text-4xl font-bold sm:text-5xl">
          <span>Rent. Ride. Host.</span><br />
          <span>Your Premium Water Adventure Starts Here.</span>
        </h1>
        <p className="mt-4 max-w-xl text-lg">
          Explore premium watercraft, ride with expert ski buddies, or earn by listing your own — all on one seamless platform.
        </p>
        <Button href="/booking" color="cyan" className="mt-6">
          Book Now
        </Button>
      </div>
    </section>
  )
}

