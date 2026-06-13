import React, { useEffect, useState } from 'react';

export default function RadioPanel({ data }) {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    if (data && data.radio) {
      setMessages(prev => {
        // Prevent duplicate consecutive messages
        if (prev.length > 0 && prev[0].text === data.radio) return prev;
        
        const newMsgs = [{
          time: new Date().toLocaleTimeString(),
          text: data.radio
        }, ...prev];
        
        return newMsgs.slice(0, 5); // Keep last 5
      });
    }
  }, [data]);

  return (
    <div className="mc-panel radio-panel">
      <h2 className="panel-title">AURA RADIO FEED</h2>
      
      <div style={{ flex: 1, overflowY: 'auto' }}>
        {messages.map((msg, i) => (
          <div key={i} className="radio-msg" style={{ opacity: i === 0 ? 1 : 0.6 }}>
            <div className="radio-time">▶ {msg.time}</div>
            <div className="radio-content">{msg.text}</div>
          </div>
        ))}
      </div>

      {data && data.decision && (
        <div className="strategy-override">
          {data.decision.action}
        </div>
      )}
    </div>
  );
}
