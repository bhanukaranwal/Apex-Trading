import { useEffect, useRef } from 'react'

interface VolatilitySurfaceProps {
  symbol: string
}

export function VolatilitySurface({ symbol }: VolatilitySurfaceProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    canvas.width = canvas.offsetWidth
    canvas.height = canvas.offsetHeight

    ctx.fillStyle = '#0f172a'
    ctx.fillRect(0, 0, canvas.width, canvas.height)

    ctx.strokeStyle = '#475569'
    ctx.lineWidth = 1

    for (let i = 0; i <= 10; i++) {
      const x = (canvas.width / 10) * i
      ctx.beginPath()
      ctx.moveTo(x, 0)
      ctx.lineTo(x, canvas.height)
      ctx.stroke()

      const y = (canvas.height / 10) * i
      ctx.beginPath()
      ctx.moveTo(0, y)
      ctx.lineTo(canvas.width, y)
      ctx.stroke()
    }

    ctx.strokeStyle = '#3b82f6'
    ctx.lineWidth = 2

    for (let strike = 0; strike <= 10; strike++) {
      ctx.beginPath()
      for (let dte = 0; dte <= canvas.width; dte += 10) {
        const x = dte
        const baseIV = 0.25
        const skew = (strike - 5) * 0.02
        const termStructure = Math.sqrt(dte / canvas.width) * 0.1
        const iv = baseIV + skew + termStructure
        const y = canvas.height - (iv * canvas.height * 2)
        
        if (dte === 0) {
          ctx.moveTo(x, y)
        } else {
          ctx.lineTo(x, y)
        }
      }
      ctx.stroke()
    }

    ctx.fillStyle = '#cbd5e1'
    ctx.font = '12px monospace'
    ctx.fillText('Strike →', canvas.width - 60, 20)
    ctx.fillText('DTE →', 10, canvas.height - 10)
    ctx.fillText('IV ↑', 10, 20)

  }, [symbol])

  return (
    <div className="workspace-panel bg-slate-900 h-[calc(100vh-200px)]">
      <div className="p-3 border-b border-slate-800">
        <h3 className="font-semibold text-slate-300">Implied Volatility Surface</h3>
        <p className="text-xs text-slate-500 mt-1">3D visualization of IV across strikes and expirations</p>
      </div>
      <div className="p-4 h-[calc(100%-60px)]">
        <canvas ref={canvasRef} className="w-full h-full" />
      </div>
    </div>
  )
}
