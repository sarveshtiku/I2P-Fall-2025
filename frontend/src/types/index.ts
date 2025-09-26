export interface Message {
  id: number
  role: string
  content: string
  model_used: string
  token_count: number
  cost: string
  carbon_footprint: string
  created_at: string
}

export interface Conversation {
  id: number
  title?: string
  current_model: string
  message_count: number
  total_tokens: number
  estimated_cost: string
  estimated_carbon: string
  created_at: string
  messages: Message[]
}

export interface Model {
  name: string
  info: {
    provider: string
    model: string
    max_tokens: number
    supports_functions: boolean
  }
}

export interface CarbonStats {
  total_carbon: number
  monthly_budget: number
  daily_average: number
}
