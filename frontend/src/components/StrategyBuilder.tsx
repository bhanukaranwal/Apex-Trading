import { useState } from 'react'
import { strategiesAPI } from '@/lib/api'
import { X } from 'lucide-react'

interface StrategyBuilderProps {
  onClose: () => void
  onSave: () => void
}

export function StrategyBuilder({ onClose, onSave }: StrategyBuilderProps) {
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [code, setCode] = useState(`def strategy(data):
    # Your strategy logic here
    sma_fast = data['close'].rolling(20).mean()
    sma_slow = data['close'].rolling(50).mean()
    
    # Generate signals
    signals = []
    for i in range(len(data)):
        if sma_fast[i] > sma_slow[i]:
            signals.append('buy')
        elif sma_fast[i] < sma_slow[i]:
            signals.append('sell')
        else:
            signals.append('hold')
    
    return signals`)

  const handleSave = async () => {
    try {
      await strategiesAPI.createStrategy({
        name,
        description,
        code,
        parameters: {},
      })
      onSave()
    } catch (error) {
      console.error('Error creating strategy:', error)
    }
  }

  return (
    <div className="workspace-panel bg-slate-900 p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold text-white">Create New Strategy</h2>
        <button onClick={onClose} className="text-slate-400 hover:text-white">
          <X size={24} />
        </button>
      </div>

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-slate-300 mb-2">Strategy Name</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full px-4 py-2 bg-slate-800 border border-slate-700 rounded text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="My Awesome Strategy"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-300 mb-2">Description</label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full px-4 py-2 bg-slate-800 border border-slate-700 rounded text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={3}
            placeholder="Describe your strategy..."
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-300 mb-2">Strategy Code</label>
          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            className="w-full px-4 py-2 bg-slate-950 border border-slate-700 rounded text-green-400 font-mono text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={15}
          />
        </div>

        <div className="flex gap-3">
          <button
            onClick={handleSave}
            className="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded font-semibold transition-colors"
          >
            Save Strategy
          </button>
          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded font-semibold transition-colors"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  )
}
