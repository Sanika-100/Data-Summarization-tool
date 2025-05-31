from transformers import pipeline

# Text to summarize
text1 = """
Abstractive text summarization is the process of generating a concise and coherent version of a longer text while preserving its meaning.
Unlike extractive summarization, which selects and copies the most important sentences from the original text,
abstractive summarization aims to create entirely new sentences that convey the most critical information.
This technique requires advanced natural language processing capabilities, as it needs to capture the essence of the original content
and express it in a different way.Abstractive summarization is a technique in natural language processing (NLP) that involves generating a concise and coherent summary of a text by creating new sentences that capture the key ideas of the original content. Rather than extracting exact phrases or sentences from the source text (as in extractive summarization), abstractive summarization seeks to rewrite the information, often using different words or sentence structures.
Recent advancements in deep learning, particularly with models like BART, T5, and Pegasus, have significantly improved the quality of
abstractive summarization. These models are pre-trained on large datasets and can be fine-tuned for specific summarization tasks.
"""
text2 = """
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
def getSummary_FaceBookDS(text="NA"):
    # Initialize the summarization pipeline
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    # Generate summary
    summary = summarizer(text, max_length=100, min_length=30, do_sample=False)

    # Print the summary
    print("Summary:")
    print(summary)
    #print(summary[0]['summary_text'])
    return summary[0]['summary_text']
#getSummary_FaceBookDS(text2)
