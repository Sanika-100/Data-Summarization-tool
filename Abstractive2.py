from transformers import pipeline, AutoTokenizer


# Text to summarize (you can change this to any text you'd like to summarize)
text1 = """
Artificial Intelligence (AI) has emerged as one of the most transformative technologies of 
the 21st century, impacting various aspects of human life and industries. 
AI refers to the simulation of human intelligence in machines that can perform tasks 
such as problem-solving, learning, reasoning, and decision-making. 
With advancements in machine learning and deep learning, 
AI-powered systems have become increasingly sophisticated, 
enabling them to analyze vast amounts of data, recognize patterns, 
and make predictions with high accuracy. Industries such as healthcare, 
finance, education, transportation, and entertainment have greatly benefited 
from AI-driven innovations. In healthcare, AI is used to diagnose diseases, 
recommend treatments, and assist in robotic surgeries, significantly improving patient outcomes. 
In finance, AI-driven algorithms analyze market trends, detect fraudulent activities, 
and optimize investment strategies. The education sector leverages 
AI to personalize learning experiences, automate administrative tasks,
and provide intelligent tutoring systems. In transportation, self-driving 
cars and AI-assisted traffic management systems aim to reduce accidents and 
enhance efficiency. AI also plays a significant role in entertainment, where 
recommendation algorithms enhance user experiences on platforms like Netflix, 
Spotify, and YouTube. Despite its numerous advantages, AI raises ethical concerns, 
including privacy risks, job displacement, and potential biases in decision-making algorithms. 
There is an ongoing debate about the responsible development and regulation of 
AI to ensure that it benefits humanity while minimizing risks. As AI continues to evolve, 
it is essential to balance technological advancements with ethical considerations to create
 a future where AI serves as a tool for societal progress and development.
"""
def getSummary_Google(text="NA"):
    # Load Pegasus tokenizer & summarization model
    model_name = "google/pegasus-xsum"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    summarizer = pipeline("summarization", model=model_name, tokenizer=tokenizer)

    max_tokens = 512  # Hard limit for Pegasus model
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        tokenized_word = tokenizer.encode(word, add_special_tokens=False)  # Get token count for word
        if current_length + len(tokenized_word) > max_tokens:
            chunks.append(" ".join(current_chunk))  # Save the chunk
            current_chunk = [word]  # Start a new chunk
            current_length = len(tokenized_word)  # Reset token counter
        else:
            current_chunk.append(word)
            current_length += len(tokenized_word)

    if current_chunk:  # Add last chunk if not empty
        chunks.append(" ".join(current_chunk))

    summaries = []
    for chunk_text in chunks:
        try:
            summary = summarizer(chunk_text, max_length=64, min_length=20, do_sample=False)
            summaries.append(summary[0]["summary_text"])
        except Exception as e:
            print(f"Error processing chunk: {str(e)}")

    final_summary = " ".join(summaries)
    return final_summary