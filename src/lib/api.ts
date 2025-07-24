const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? ''

function getCSRFToken() {
  if (typeof document === 'undefined') return ''
  const match = document.cookie.match(/csrftoken=([^;]+)/)
  return match ? match[1] : ''
}

export async function apiFetch(
  path: string,
  options: RequestInit = {}
): Promise<Response> {
  const url = `${API_BASE_URL}${path}`
  const res = await fetch(url, {
    ...options,
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
  })
  return res
}

export async function getJSON<T>(path: string): Promise<T> {
  const res = await apiFetch(path)
  if (!res.ok) throw new Error(await res.text())
  return res.json() as Promise<T>
}

export async function postJSON<T>(path: string, data: any): Promise<T> {
  const res = await apiFetch(path, {
    method: 'POST',
    body: JSON.stringify(data),
    headers: {
      'X-CSRFToken': getCSRFToken(),
    },
  })
  if (!res.ok) {
    const text = await res.text()
    try {
      const json = JSON.parse(text)
      throw new Error(json.detail || JSON.stringify(json))
    } catch {
      throw new Error(text)
    }
  }
  return res.json() as Promise<T>
}
