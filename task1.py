def chatbot():
    print("Chatbot: Hello! I am your simple rule-based chatbot.")
    print("Type 'bye' to exit.\n")
    
    while True:
        user_input = input("You: ").lower()
        
        if "hello" in user_input or "hi" in user_input:
            print("Chatbot: Hi there! How can I help you?")
        
        elif "how are you" in user_input:
            print("Chatbot: I am just a program, but I'm doing great!")
        
        elif "your name" in user_input:
            print("Chatbot: I am a Rule-Based Chatbot.")
        
        elif "bye" in user_input:
            print("Chatbot: Goodbye! Have a nice day!")
            break
        
        else:
            print("Chatbot: Sorry, I don't understand that.")

# Run chatbot
chatbot()
