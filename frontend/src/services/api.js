import axios from 'axios'

const API_BASE_URL = 'http://localhost:7860'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const verifyText = async (text, context, date) => {
  const formData = new FormData()
  formData.append('text_input', text)
  formData.append('claim_context', context || 'Unknown context')
  formData.append('claim_date', date || 'Unknown date')
  
  const response = await api.post('/verify/text', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  return response.data
}

export const verifyImage = async (file, context, date) => {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('claim_context', context || 'Unknown context')
  formData.append('claim_date', date || 'Unknown date')
  
  const response = await api.post('/verify/image', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  return response.data
}

export const getRecentPosts = async (limit = 5) => {
  const response = await api.get(`/mongodb/recent-posts?limit=${limit}`)
  return response.data
}

export default api