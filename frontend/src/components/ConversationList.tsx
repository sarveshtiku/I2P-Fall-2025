import React from 'react'
import { Plus, MessageSquare, Clock, Zap, DollarSign } from 'lucide-react'
import { Conversation } from '../types'

interface ConversationListProps {
  conversations: Conversation[]
  currentConversation: Conversation | null
  onSelectConversation: (id: number) => void
  onCreateNew: () => void
}

const ConversationList: React.FC<ConversationListProps> = ({
  conversations,
  currentConversation,
  onSelectConversation,
  onCreateNew
}) => {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    const now = new Date()
    const diffInHours = (now.getTime() - date.getTime()) / (1000 * 60 * 60)
    
    if (diffInHours < 24) {
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    } else if (diffInHours < 168) { // 7 days
      return date.toLocaleDateString([], { weekday: 'short' })
    } else {
      return date.toLocaleDateString([], { month: 'short', day: 'numeric' })
    }
  }

  const formatCost = (cost: string) => {
    const num = parseFloat(cost)
    return num < 0.01 ? '<$0.01' : `$${num.toFixed(2)}`
  }

  const formatCarbon = (carbon: string) => {
    const num = parseFloat(carbon)
    return num < 0.001 ? '<0.001g' : `${num.toFixed(2)}g`
  }

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold text-gray-900">Conversations</h2>
        <button
          onClick={onCreateNew}
          className="btn-primary text-sm py-1.5 px-3"
        >
          <Plus className="w-4 h-4 mr-1" />
          New
        </button>
      </div>

      {/* Conversations List */}
      <div className="space-y-2">
        {conversations.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <MessageSquare className="w-12 h-12 mx-auto mb-4 text-gray-300" />
            <p>No conversations yet</p>
            <p className="text-sm">Create your first conversation to get started</p>
          </div>
        ) : (
          conversations.map((conversation) => (
            <div
              key={conversation.id}
              onClick={() => onSelectConversation(conversation.id)}
              className={`p-3 rounded-lg cursor-pointer transition-colors ${
                currentConversation?.id === conversation.id
                  ? 'bg-primary-50 border border-primary-200'
                  : 'bg-white border border-gray-200 hover:bg-gray-50'
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1 min-w-0">
                  <h3 className="text-sm font-medium text-gray-900 truncate">
                    {conversation.title || 'Untitled Conversation'}
                  </h3>
                  <p className="text-xs text-gray-500 mt-1">
                    {conversation.message_count} messages • {conversation.total_tokens} tokens
                  </p>
                </div>
                <div className="flex items-center text-xs text-gray-400 ml-2">
                  <Clock className="w-3 h-3 mr-1" />
                  {formatDate(conversation.created_at)}
                </div>
              </div>
              
              <div className="flex items-center justify-between mt-2">
                <div className="flex items-center space-x-3 text-xs text-gray-500">
                  <div className="flex items-center space-x-1">
                    <Zap className="w-3 h-3" />
                    <span>{formatCarbon(conversation.estimated_carbon)}</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <DollarSign className="w-3 h-3" />
                    <span>{formatCost(conversation.estimated_cost)}</span>
                  </div>
                </div>
                <div className="text-xs text-gray-400">
                  {conversation.current_model}
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default ConversationList
