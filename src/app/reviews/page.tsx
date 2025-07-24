import { Reviews, type Review } from '@/components/Reviews'
import { getJSON } from '@/lib/api'

export const metadata = {
  title: 'Reviews',
}

export default async function ReviewsPage() {
  const reviews = await getJSON<Review[]>('/api/reviews/')
  return <Reviews reviews={reviews} />
}
