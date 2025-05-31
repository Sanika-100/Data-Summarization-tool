from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer

def getSelectiveSummary(text="NA"):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()  # Using LSA instead of TextRank
    summary_sentences = summarizer(parser.document, 1)  # Extract 1 important sentence
    
    return " ".join(str(sentence) for sentence in summary_sentences)
# Input text for summarization
text1 = """
Abstractive text summarization is the process of generating a concise and coherent version of a longer text while preserving its meaning.
Unlike extractive summarization, which selects and copies the most important sentences from the original text,
abstractive summarization aims to create entirely new sentences that convey the most critical information.
This technique requires advanced natural language processing capabilities, as it needs to capture the essence of the original content
and express it in a different way.
Recent advancements in deep learning, particularly with models like BART, T5, and Pegasus, have significantly improved the quality of
abstractive summarization. These models are pre-trained on large datasets and can be fine-tuned for specific summarization tasks.

def getSelectiveSummary(text="NA"):
    # Create a parser and tokenizer
    parser = PlaintextParser.from_string(text, Tokenizer("english"))

    # Initialize TextRank Summarizer
    summarizer = TextRankSummarizer()

    # Generate summary (set the number of sentences you want in the summary)
    summary_sentences = summarizer(parser.document, 2)  # Extracts 2 most important sentences
    paragraph = " ".join(str(sentence) for sentence in summary_sentences)
    # Print the summary
     
    print("Summary:")
    for sentence in summary_sentences:
        print(sentence)
     
    return paragraph"""
#print(getSelectiveSummary(text1))