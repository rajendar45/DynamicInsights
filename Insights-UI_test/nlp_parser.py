import spacy as sp
def convert_to_query(question):
    # Load the English language model
    nlp = sp.load('en_core_web_sm')

    # Parse the question using the language model
    doc = nlp(question)
    print("Parsed text - ") 
    print(doc)
    print("-----------")
    # Define a list of keywords to search for in the question
    keywords = ['find', 'what', 'when', 'where', 'how', 'give', 'list', 'fetch', 'get', 'show', 'display', 'retrieve', 'count', 'sum', 'average', 'maximum', 'minimum']

    special_keys = ['sysdate', 'dual', 'time']
    # Initialize an empty query string
    query = ''
    # Iterate over each token in the parsed question
    for token in doc:
        token_text1 = token.text
        token_pos1 = token.pos_
        # This is for formatting only
        print(f"{token_text1:<12}{token_pos1:<8}")  
        # Check if the token is a keyword
        if token.text.lower() in keywords:
            # Add the keyword to the query string
            query += token.text + ' '
        if token.text.lower() in keywords:
            query = 'select sysdate from dual'
       # Add the table name to the query
    print("Interpreted query is..."   + query)  

    # Return the final query string
    return query.strip()