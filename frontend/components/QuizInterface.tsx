'use client';
import { useEffect, useState, useRef } from 'react';
import { QuestionData } from '../lib/types';

export default function QuizInterface({ userId, onComplete }: { userId: string, onComplete: () => void }) {
  const [question, setQuestion] = useState<QuestionData | null>(null);
  const [status, setStatus] = useState<string>('Connecting to assessment engine...');
  const [isTransitioning, setIsTransitioning] = useState<boolean>(false);
  
  const [textAnswer, setTextAnswer] = useState<string>('');
  const [latestMastery, setLatestMastery] = useState<number | null>(null);
  
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    ws.current = new WebSocket(`ws://localhost:8000/api/ws/quiz/${userId}`);

    ws.current.onmessage = (event) => {
      const payload = JSON.parse(event.data);

      if (payload.type === 'feedback') {
        // Quietly update the mastery score in the header
        setLatestMastery(payload.data.current_mastery);
      } else if (payload.type === 'question') {
        // Immediately show the next question
        setQuestion(payload.data);
        setTextAnswer('');
        setStatus('Active');
        setIsTransitioning(false);
      } else if (payload.type === 'complete') {
        setQuestion(null);
        setStatus(`Assessment Complete! Mastery Level: ${Math.round(payload.mastery_level * 100)}%`);
        setIsTransitioning(false);
      } else if (payload.type === 'error') {
        console.error("Backend error:", payload.message);
        setIsTransitioning(false);
      }
    };

    return () => {
      if (ws.current) ws.current.close();
    };
  }, [userId]);

  const submitAnswer = (answerText: string) => {
    if (ws.current && question && !isTransitioning) {
      setIsTransitioning(true);
      ws.current.send(JSON.stringify({
        type: 'answer',
        question_id: question.id,
        answer: answerText
      }));
    }
  };

  return (
    <div className="flex flex-col h-full max-w-2xl mx-auto p-4 md:p-6 text-gray-800">
      <div className="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden flex-1 flex flex-col">
        
        {/* Header Section */}
        <div className="bg-gray-50 border-b border-gray-200 p-4 flex justify-between items-center">
          <div>
            <h2 className="text-lg font-semibold text-gray-700">Skill Assessment</h2>
            {status === 'Active' ? (
              <div className="flex items-center mt-1">
                <span className="flex w-2 h-2 bg-green-500 rounded-full animate-pulse mr-2"></span>
                <p className="text-xs text-gray-500">Live Evaluation</p>
              </div>
            ) : (
              <p className="text-xs text-gray-500 mt-1">{status}</p>
            )}
          </div>
          {/* Real-time Mastery Indicator */}
          {latestMastery !== null && status === 'Active' && (
            <div className="text-sm font-medium text-blue-600 bg-blue-50 px-3 py-1 rounded-full">
              Current Mastery: {Math.round(latestMastery * 100)}%
            </div>
          )}
        </div>

        {/* Main Content Area */}
        <div className="p-6 flex-1 flex flex-col justify-center">
          {question ? (
            
            /* Question State */
            <div className={`transition-opacity duration-300 ${isTransitioning ? 'opacity-50 pointer-events-none' : 'opacity-100'}`}>
              <div className="flex items-center gap-2 mb-4">
                <span className="px-2 py-1 bg-gray-100 text-gray-600 text-xs font-semibold rounded uppercase tracking-wider">
                  {question.question_type.replace('_', ' ')}
                </span>
              </div>
              
              <h3 className="text-xl font-medium mb-6 leading-relaxed">
                {question.text}
              </h3>
              
              {/* Render Inputs dynamically based on question_type */}
              {question.question_type === 'mcq' && question.options && (
                <div className="space-y-3">
                  {question.options.map((opt, idx) => (
                    <button
                      key={idx}
                      onClick={() => submitAnswer(opt)}
                      disabled={isTransitioning}
                      className="w-full text-left p-4 rounded-lg border border-gray-200 hover:border-blue-500 hover:bg-blue-50 transition-all duration-200 font-medium text-gray-700"
                    >
                      {opt}
                    </button>
                  ))}
                </div>
              )}

              {(question.question_type === 'two_liner' || question.question_type === 'paragraph') && (
                <div className="space-y-4 flex flex-col">
                  <textarea
                    value={textAnswer}
                    onChange={(e) => setTextAnswer(e.target.value)}
                    placeholder="Type your answer here..."
                    rows={question.question_type === 'paragraph' ? 6 : 3}
                    className="w-full p-4 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all resize-none outline-none text-gray-700"
                  />
                  <button
                    onClick={() => submitAnswer(textAnswer)}
                    disabled={!textAnswer.trim() || isTransitioning}
                    className="self-end px-6 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition disabled:bg-gray-300 disabled:cursor-not-allowed"
                  >
                    {isTransitioning ? "Grading..." : "Submit Answer"}
                  </button>
                </div>
              )}
            </div>

          ) : (
            
            /* Loading or Complete State */
            <div className="text-center">
              {status.includes('Complete') ? (
                <div className="space-y-4">
                  <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-green-100 text-green-600 mb-2">
                    <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>
                  </div>
                  <h3 className="text-2xl font-bold text-gray-800">{status.split('!')[0]}!</h3>
                  <p className="text-gray-600">{status.split('!')[1]}</p>
                  
                  <button 
                    onClick={onComplete}
                    className="mt-6 px-6 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition"
                  >
                    View Learning Path
                  </button>
                </div>
              ) : (
                <div className="animate-pulse flex flex-col items-center">
                  <div className="h-4 bg-gray-200 rounded w-3/4 mb-4"></div>
                  <div className="h-10 bg-gray-200 rounded w-full mb-2"></div>
                  <div className="h-10 bg-gray-200 rounded w-full mb-2"></div>
                </div>
              )}
            </div>
          )}
        </div>

      </div>
    </div>
  );
}