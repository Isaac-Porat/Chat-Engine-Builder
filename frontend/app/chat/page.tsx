import ChatSection from "../components/chat-section";

const Chat = () => {
  return (
    <main className="h-screen w-full flex justify-center items-center background-gradient">
      <div className="w-full max-w-sm h-[60vh] flex flex-col">
        <div className="flex-grow overflow-hidden rounded-lg shadow-lg">
          <ChatSection />
        </div>
      </div>
    </main>
  )
}

export default Chat;