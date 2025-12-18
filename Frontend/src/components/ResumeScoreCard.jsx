import { X, Award, AlertCircle, CheckCircle, TrendingUp } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

export default function ResumeScoreCard({ score, onClose }) {
  if (!score) {
    return (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="bg-white rounded-2xl p-8 max-w-2xl w-full"
        >
          <div className="flex items-center justify-center">
            <div className="spinner" />
          </div>
          <p className="text-center mt-4 text-gray-600">
            Calculating ATS score...
          </p>
        </motion.div>
      </div>
    )
  }

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getScoreBgColor = (score) => {
    if (score >= 80) return 'bg-green-50 border-green-200'
    if (score >= 60) return 'bg-yellow-50 border-yellow-200'
    return 'bg-red-50 border-red-200'
  }

  return (
    <AnimatePresence>
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.9, opacity: 0 }}
          className="bg-white rounded-2xl shadow-2xl p-8 max-w-2xl w-full max-h-[90vh] overflow-y-auto"
        >
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-3">
              <Award className="w-8 h-8 text-primary-600" />
              <h2 className="text-2xl font-bold text-gray-900">
                ATS Compatibility Score
              </h2>
            </div>
            <button
              onClick={onClose}
              className="p-2 hover:bg-gray-100 rounded-full transition"
            >
              <X className="w-6 h-6" />
            </button>
          </div>

          {/* Score Display */}
          <div
            className={`rounded-xl p-8 border-2 ${getScoreBgColor(
              score.score
            )} mb-6`}
          >
            <div className="text-center">
              <div className={`text-6xl font-bold ${getScoreColor(score.score)} mb-2`}>
                {score.score}
                <span className="text-3xl">/100</span>
              </div>
              <p className="text-gray-600 text-lg">
                {score.score >= 80
                  ? '🎉 Excellent! Your resume is highly ATS-compatible'
                  : score.score >= 60
                  ? '👍 Good, but there\'s room for improvement'
                  : '⚠️ Needs improvement to pass ATS screening'}
              </p>
            </div>
          </div>

          {/* Feedback */}
          {score.feedback && (
            <div className="mb-6">
              <div className="flex items-center gap-2 mb-3">
                <CheckCircle className="w-5 h-5 text-green-600" />
                <h3 className="text-lg font-semibold text-gray-900">Feedback</h3>
              </div>
              <div className="bg-gray-50 rounded-lg p-4">
                <p className="text-gray-700 whitespace-pre-wrap">{score.feedback}</p>
              </div>
            </div>
          )}

          {/* Missing Keywords */}
          {score.missing_keywords && score.missing_keywords.length > 0 && (
            <div className="mb-6">
              <div className="flex items-center gap-2 mb-3">
                <AlertCircle className="w-5 h-5 text-orange-600" />
                <h3 className="text-lg font-semibold text-gray-900">
                  Missing Keywords
                </h3>
              </div>
              <div className="flex flex-wrap gap-2">
                {score.missing_keywords.map((keyword, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 bg-orange-100 text-orange-700 rounded-full text-sm font-medium"
                  >
                    {keyword}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Improvements */}
          {score.improvements && score.improvements.length > 0 && (
            <div>
              <div className="flex items-center gap-2 mb-3">
                <TrendingUp className="w-5 h-5 text-primary-600" />
                <h3 className="text-lg font-semibold text-gray-900">
                  Suggested Improvements
                </h3>
              </div>
              <ul className="space-y-2">
                {score.improvements.map((improvement, index) => (
                  <li
                    key={index}
                    className="flex items-start gap-2 bg-primary-50 rounded-lg p-3"
                  >
                    <span className="text-primary-600 font-bold">•</span>
                    <span className="text-gray-700">{improvement}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Close Button */}
          <div className="mt-6 flex justify-end">
            <button onClick={onClose} className="btn btn-primary">
              Close
            </button>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  )
}
