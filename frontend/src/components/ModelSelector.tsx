import React from 'react'
import { ChevronDown, Bot } from 'lucide-react'
import { Model } from '../types'

interface ModelSelectorProps {
  models: Model[]
  selectedModel: string
  onModelChange: (model: string) => void
}

const ModelSelector: React.FC<ModelSelectorProps> = ({
  models,
  selectedModel,
  onModelChange
}) => {
  const getModelIcon = (provider: string) => {
    switch (provider) {
      case 'openai':
        return '🤖'
      case 'anthropic':
        return '🧠'
      case 'google':
        return '💎'
      default:
        return '🤖'
    }
  }

  const getModelColor = (provider: string) => {
    switch (provider) {
      case 'openai':
        return 'text-green-600 bg-green-50'
      case 'anthropic':
        return 'text-orange-600 bg-orange-50'
      case 'google':
        return 'text-blue-600 bg-blue-50'
      default:
        return 'text-gray-600 bg-gray-50'
    }
  }

  return (
    <div className="relative">
      <select
        value={selectedModel}
        onChange={(e) => onModelChange(e.target.value)}
        className="appearance-none bg-white border border-gray-300 rounded-lg px-3 py-2 pr-8 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
      >
        {models.map((model) => (
          <option key={model.name} value={model.name}>
            {getModelIcon(model.info.provider)} {model.info.model}
          </option>
        ))}
      </select>
      <ChevronDown className="absolute right-2 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none" />
    </div>
  )
}

export default ModelSelector
