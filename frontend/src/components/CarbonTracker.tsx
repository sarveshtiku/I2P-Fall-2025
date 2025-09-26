import React, { useState, useEffect } from 'react'
import { Leaf, TrendingUp, AlertTriangle } from 'lucide-react'

const CarbonTracker: React.FC = () => {
  const [carbonStats, setCarbonStats] = useState({
    total: 0,
    monthly: 1000,
    daily: 0
  })

  // Mock data - in real app, this would come from API
  useEffect(() => {
    setCarbonStats({
      total: 45.2,
      monthly: 1000,
      daily: 2.1
    })
  }, [])

  const percentage = (carbonStats.total / carbonStats.monthly) * 100
  const isOverBudget = percentage > 100

  return (
    <div className="flex items-center space-x-2">
      <div className="flex items-center space-x-1 text-sm">
        <Leaf className={`w-4 h-4 ${isOverBudget ? 'text-red-500' : 'text-green-500'}`} />
        <span className={`font-medium ${isOverBudget ? 'text-red-600' : 'text-green-600'}`}>
          {carbonStats.total.toFixed(1)}g
        </span>
        <span className="text-gray-400">/ {carbonStats.monthly}g</span>
      </div>
      
      <div className="w-16 h-2 bg-gray-200 rounded-full overflow-hidden">
        <div
          className={`h-full transition-all duration-300 ${
            isOverBudget ? 'bg-red-500' : 'bg-green-500'
          }`}
          style={{ width: `${Math.min(percentage, 100)}%` }}
        />
      </div>
      
      {isOverBudget && (
        <AlertTriangle className="w-4 h-4 text-red-500" />
      )}
    </div>
  )
}

export default CarbonTracker
