# Parisodan-research-app
We tried to create a tool that is essential for many researchers and accelerate research. The research papers and documents are very long so finding something important becomes extremely difficult. So, we tried to automate that using deep learning. Our model can search the answers for your question in long text and papers within a short time. It doesn’t give the direct words in the text. The language model we used is powerful to understand the text, capture multiple sentences and it is highly parallelizable and computes efficiently. We are using an excellent transformer model in deep learning which avoids recursion by processing sentences as a whole using attention mechanisms and positional embeddings. So, given a paragraph and question our model can produce the best possible answer compared to humans.

## Service Provided
The first one requires user to input paragraphs and ask questions.

The second one requires user to upload a book or a pdf, apply OCR (optical character recognition) and extract the text. These will be long texts, so we divide them into pages and create a map of words and pages. So given a question we search only those pages which have relevant words and not the entire pdf. We also remove punctuations and extra spaces.

The third one requires user to give the question and we automatically surf Wikipedia to find the best possible answer. We use web scrapping to get the relevant wiki pages and use that text to find the answer with maximum score and return it.
