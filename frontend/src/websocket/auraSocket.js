export function connectAura(callback) {
    const socket = new WebSocket("ws://localhost:8000/live");
    
    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        callback(data);
    };
    
    socket.onopen = () => console.log("Connected to AURA");
    socket.onclose = () => console.log("Disconnected from AURA");
    
    return socket;
}
