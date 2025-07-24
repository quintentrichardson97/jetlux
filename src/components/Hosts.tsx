export function Hosts() {
  const hosts = [
    { name: 'Charlie', bio: 'Your go-to host for unforgettable jet ski adventures.' },
    { name: 'Danielle', bio: 'Knows every waterway around Tampa.' },
    { name: 'Max', bio: 'Ensures safety while you have fun on the waves.' },
  ]

  return (
    <section className="py-20" id="hosts">
      <div className="mx-auto max-w-4xl px-4 text-center">
        <h2 className="text-3xl font-semibold">Meet Our Hosts</h2>
        <p className="mt-2 text-lg text-gray-600">
          Trusted hosts who offer various rentals
        </p>
        <div className="mt-10 grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
          {hosts.map((host) => (
            <div key={host.name} className="rounded-lg bg-white p-6 shadow">
              <div className="h-40 bg-gray-200 mb-4" />
              <h3 className="text-xl font-medium">{host.name}</h3>
              <p className="mt-2 text-sm text-gray-600">{host.bio}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
