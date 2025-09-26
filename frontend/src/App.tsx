import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import ChatInterface from './components/ChatInterface'
import ConversationList from './components/ConversationList'
import ModelSelector from './components/ModelSelector'
import CarbonTracker from './components/CarbonTracker'
import { Conversation, Message, Model } from './types'

function App() {
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [currentConversation, setCurrentConversation] = useState<Conversation | null>(null)
  const [availableModels, setAvailableModels] = useState<Model[]>([])
  const [selectedModel, setSelectedModel] = useState<string>('gpt-4')

  useEffect(() => {
    // Load available models
    fetchAvailableModels()
    // Load conversations
    fetchConversations()
  }, [])

  const fetchAvailableModels = async () => {
    try {
      const response = await fetch('/api/v1/models/')
      const models = await response.json()
      setAvailableModels(models)
    } catch (error) {
      console.error('Failed to fetch models:', error)
    }
  }

  const fetchConversations = async () => {
    try {
      const response = await fetch('/api/v1/conversations/')
      const conversations = await response.json()
      setConversations(conversations)
    } catch (error) {
      console.error('Failed to fetch conversations:', error)
    }
  }

  const createNewConversation = async () => {
    try {
      const response = await fetch('/api/v1/conversations/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: 'New Conversation',
          initial_model: selectedModel
        })
      })
      const conversation = await response.json()
      setCurrentConversation(conversation)
      setConversations([conversation, ...conversations])
    } catch (error) {
      console.error('Failed to create conversation:', error)
    }
  }

  const selectConversation = async (conversationId: number) => {
    try {
      const response = await fetch(`/api/v1/conversations/${conversationId}`)
      const conversation = await response.json()
      setCurrentConversation(conversation)
    } catch (error) {
      console.error('Failed to fetch conversation:', error)
    }
  }

  const sendMessage = async (content: string) => {
    if (!currentConversation) return

    try {
      const response = await fetch(`/api/v1/conversations/${currentConversation.id}/messages`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content,
          model: selectedModel
        })
      })
      const message = await response.json()
      
      // Update current conversation with new message
      setCurrentConversation(prev => {
        if (!prev) return null
        return {
          ...prev,
          messages: [...prev.messages, message]
        }
      })
    } catch (error) {
      console.error('Failed to send message:', error)
    }
  }

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <div className="flex items-center">
                <h1 className="text-xl font-bold text-gray-900">
                  🧩 ContextLink
                </h1>
                <span className="ml-2 text-sm text-gray-500">
                  Universal AI Memory Fabric
                </span>
              </div>
              <div className="flex items-center space-x-4">
                <ModelSelector
                  models={availableModels}
                  selectedModel={selectedModel}
                  onModelChange={setSelectedModel}
                />
                <CarbonTracker />
              </div>
            </div>
          </div>
        </header>

        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Routes>
            <Route
              path="/"
              element={
                <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
                  <div className="lg:col-span-1">
                    <ConversationList
                      conversations={conversations}
                      currentConversation={currentConversation}
                      onSelectConversation={selectConversation}
                      onCreateNew={createNewConversation}
                    />
                  </div>
                  <div className="lg:col-span-3">
                    {currentConversation ? (
                      <ChatInterface
                        conversation={currentConversation}
                        onSendMessage={sendMessage}
                        selectedModel={selectedModel}
                      />
                    ) : (
                      <div className="card text-center">
                        <h2 className="text-xl font-semibold text-gray-900 mb-4">
                          Welcome to ContextLink
                        </h2>
                        <p className="text-gray-600 mb-6">
                          Select a conversation or create a new one to get started.
                        </p>
                        <button
                          onClick={createNewConversation}
                          className="btn-primary"
                        >
                          Start New Conversation
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              }
            />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
