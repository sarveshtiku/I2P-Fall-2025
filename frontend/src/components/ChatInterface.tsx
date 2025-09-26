import React, { useState, useRef, useEffect } from 'react'
import { Send, Bot, User, Zap, DollarSign } from 'lucide-react'
import { Conversation, Message } from '../types'

interface ChatInterfaceProps {
  conversation: Conversation
  onSendMessage: (content: string) => void
  selectedModel: string
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({
  conversation,
  onSendMessage,
  selectedModel
}) => {
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [conversation.messages])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!inputValue.trim() || isLoading) return

    setIsLoading(true)
    await onSendMessage(inputValue.trim())
    setInputValue('')
    setIsLoading(false)
  }

  const formatCost = (cost: string) => {
    const num = parseFloat(cost)
    return num < 0.01 ? '<$0.01' : `$${num.toFixed(4)}`
  }

  const formatCarbon = (carbon: string) => {
    const num = parseFloat(carbon)
    return num < 0.001 ? '<0.001g' : `${num.toFixed(3)}g`
  }

  return (
    <div className="flex flex-col h-[600px] bg-white rounded-lg shadow-sm border border-gray-200">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200">
        <div>
          <h2 className="text-lg font-semibold text-gray-900">
            {conversation.title || 'Untitled Conversation'}
          </h2>
          <p className="text-sm text-gray-500">
            {conversation.message_count} messages • {conversation.total_tokens} tokens
          </p>
        </div>
        <div className="flex items-center space-x-4 text-sm text-gray-500">
          <div className="flex items-center space-x-1">
            <Zap className="w-4 h-4" />
            <span>{formatCarbon(conversation.estimated_carbon)} CO₂</span>
          </div>
          <div className="flex items-center space-x-1">
            <DollarSign className="w-4 h-4" />
            <span>{formatCost(conversation.estimated_cost)}</span>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {conversation.messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`flex max-w-[80%] ${
                message.role === 'user' ? 'flex-row-reverse' : 'flex-row'
              }`}
            >
              <div
                className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                  message.role === 'user'
                    ? 'bg-primary-600 text-white ml-2'
                    : 'bg-gray-200 text-gray-600 mr-2'
                }`}
              >
                {message.role === 'user' ? (
                  <User className="w-4 h-4" />
                ) : (
                  <Bot className="w-4 h-4" />
                )}
              </div>
              <div
                className={`px-4 py-2 rounded-lg ${
                  message.role === 'user'
                    ? 'bg-primary-600 text-white'
                    : 'bg-gray-100 text-gray-900'
                }`}
              >
                <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                <div className="flex items-center justify-between mt-2 text-xs opacity-70">
                  <span>{message.model_used}</span>
                  <div className="flex items-center space-x-2">
                    <span>{formatCost(message.cost)}</span>
                    <span>•</span>
                    <span>{formatCarbon(message.carbon_footprint)}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="flex">
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-200 text-gray-600 mr-2 flex items-center justify-center">
                <Bot className="w-4 h-4" />
              </div>
              <div className="px-4 py-2 rounded-lg bg-gray-100 text-gray-900">
                <div className="flex items-center space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="p-4 border-t border-gray-200">
        <div className="flex space-x-2">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder={`Message ${selectedModel}...`}
            className="flex-1 input-field"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={!inputValue.trim() || isLoading}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </form>
    </div>
  )
}

export default ChatInterface
