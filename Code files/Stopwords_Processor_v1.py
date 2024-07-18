import nltk
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download necessary NLTK data files
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Function to read the text file
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

# Function to get part of speech tag for lemmatization
def get_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {
        'J': wordnet.ADJ,
        'N': wordnet.NOUN,
        'V': wordnet.VERB,
        'R': wordnet.ADV
    }
    return tag_dict.get(tag, wordnet.NOUN)

# Function to tokenize text, remove stop words, and perform lemmatization
def process_text(text):
    # Tokenize the text
    words = word_tokenize(text)
    
    # Convert to lower case
    words = [word.lower() for word in words]
    
    # Remove punctuation and non-alphabetic tokens
    words = [word for word in words if word.isalpha()]
    
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words]
    
    # Perform lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word, get_pos(word)) for word in filtered_words]
    
    return lemmatized_words

# Function to save the processed text to a file
def save_processed_text(processed_text, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(' '.join(processed_text))

# Main function to execute the processing
def main(input_file_path, output_file_path):
    text = read_file(input_file_path)
    processed_text = process_text(text)
    save_processed_text(processed_text, output_file_path)
    print("Process completed")

# Example usage
input_file_path = r'C:\path\to\your\text_file.txt'  # Replace with the actual path to your input text file
output_file_path = r'C:\path\to\your\output_file.txt'  # Replace with the actual path to your output text file

main(input_file_path, output_file_path)

-------------------------------------------------------------------------------------------------

#Python script that reads the processed output file, counts the frequency of each word, and prints the top 5 most repeated words:

from collections import Counter

# Function to read the processed text file
def read_processed_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

# Function to find the top 5 most repeated words
def find_top_words(text, top_n=5):
    # Split the text into words
    words = text.split()
    
    # Count the frequency of each word
    word_counts = Counter(words)
    
    # Find the top N most common words
    top_words = word_counts.most_common(top_n)
    
    return top_words

# Main function to execute the top word finding
def main(file_path):
    text = read_processed_file(file_path)
    top_words = find_top_words(text)
    return top_words

# Example usage
output_file_path = r'C:\path\to\your\output_file.txt'  # Replace with the actual path to your output text file

top_words = main(output_file_path)
print("Top 5 most repeated words:")
for word, count in top_words:
    print(f"{word}: {count}")

